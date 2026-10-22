"""
GitHub Reverse Proxy
- Checks requests against repos.txt whitelist (injects PAT if allowed)
- Personal Access Token never exposed to Claude container

Not yet checked: Methods and endpoints
"""

import os, base64, http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import rules

PORT = 8080

REPOS_PATH = os.environ.get('REPOS_PATH', '/config/repos.txt')
REPOS = rules.load_repos(REPOS_PATH)


# Load GH PAT (Personal Access Token)
TOKEN = os.environ.get('GITHUB_TOKEN')
if not TOKEN:
    raise SystemExit('GITHUB_TOKEN is not set. Add GH_PROXY_TOKEN to .env and restart.')

# Prepare auth headers
BASIC_AUTH = base64.b64encode(f'x-access-token:{TOKEN}'.encode()).decode()
UPSTREAMS  = {
    'git.github-proxy': ('github.com',     f'Basic {BASIC_AUTH}'),
    'api.github-proxy': ('api.github.com', f'token {TOKEN}'),
}


TIMEOUT = 60 # Timeout (seconds) for each network step (not entire request)
CHUNK_SIZE = 64 * 1024 # Bytes per read when streaming request bodies

# Drop these headers (don't forward with real request)
SKIP_REQUEST_HEADERS = {
    'host',
    'authorization',
    'connection',
    'keep-alive',
    'proxy-connection',
    'proxy-authorization',
    'te',
    'trailer',
    'transfer-encoding',
    'upgrade',
    'content-length',
    'expect'
}

SKIP_RESPONSE_HEADERS = {
    'connection',
    'keep-alive',
    'transfer-encoding'
}



class ProxyHandler(BaseHTTPRequestHandler):

    def handle_any(self):
        host = self.headers.get('Host', '')
        allowed, reason = rules.check(REPOS, host, self.path)
        
        if not allowed:
            self.log_message('DENY %s %s%s (%s)', self.command, host, self.path, reason)
            msg = f'DENY: {self.command} {host}{self.path}\n {reason}\n'
            self.send_text(403, msg)
            return

        self.forward(host.split(':')[0].lower())

    def send_text(self, status, text):
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(text.encode())

    def log_request(self, code='-', size='-'):
        pass # Skip default log since we log our own

    # http.server calls do_<METHOD>
    # Route them all to one place
    do_HEAD   = handle_any
    do_GET    = handle_any
    do_POST   = handle_any
    do_PUT    = handle_any
    do_PATCH  = handle_any
    do_DELETE = handle_any

    def forward(self, proxy_host):
        upstream_host, auth = UPSTREAMS[proxy_host]

        # Copy Claude's headers, then set our own Host and login
        headers = {k: v for k, v in self.headers.items() if k.lower() not in SKIP_REQUEST_HEADERS}
        headers['Host'] = upstream_host
        headers['Authorization'] = auth

        body = None

        chunked = 'chunked' in self.headers.get('Transfer-Encoding', '').lower()
        length  = int(self.headers.get('Content-Length', '0'))
        
        if chunked:
            body = self.read_chunked_body()

        elif length:
            body = self.read_fixed_body(length)
            headers['Content-Length'] = str(length)

        conn = http.client.HTTPSConnection(upstream_host, timeout=TIMEOUT)
        
        try:
            conn.request(self.command, self.path, headers=headers, body=body, encode_chunked=chunked)
            response = conn.getresponse()
            self.log_message('ALLOW %s %s%s → %d', self.command, upstream_host, self.path, response.status)
        
        except OSError as e:
            self.log_message('ERROR %s %s%s (%s)', self.command, upstream_host, self.path, e)
            msg = f'Unable to reach {upstream_host}\n Try again later\n Error: {e}\n'
            self.send_text(502, msg)
            return

        # Send GitHub's status and headers back to Claude
        self.send_response(response.status, response.reason)
        for key, value in response.getheaders():
            if key.lower() not in SKIP_RESPONSE_HEADERS:
                self.send_header(key, value)
        self.end_headers()

        # Stream the body back in pieces (large clones aren't held in memory)
        while chunk := response.read(CHUNK_SIZE):
            self.wfile.write(chunk)

        conn.close()

    def read_fixed_body(self, length):
        """Returns a generator that gives body data one chunk at at time: KNOWN SIZE"""
        remaining = length

        while remaining > 0:
            size = min(CHUNK_SIZE, remaining)

            # Read chunk from rfile, which is a stream.
            data = self.rfile.read(size)

            # Abort if connection closed early
            if len(data) == 0: break

            remaining -= len(data)
            yield data

    def read_chunked_body(self):
        """Generator that gives chunked data: UNKNOWN SIZE"""
        while True:
            line = self.rfile.readline()
            raw  = line.split(b';')[0]
            size = int(raw, 16)

            # Reached end of the body so we can stop here
            if size == 0:
                while True:
                    # Cleanup before we stop
                    # Throw away any trailers (checksums, etc)
                    # When we get to a blank line we can stop
                    line = self.rfile.readline()
                    if line in [b'\r\n', b'\n', b'']:
                        return

            data = self.rfile.read(size)
            yield data

            # Throw away trailing \r\n
            self.rfile.readline()


if __name__ == '__main__':
    allowed = ', '.join(sorted(REPOS)) or 'None'
    print(f'Allowed Repos: {allowed}')

    server = ThreadingHTTPServer(('0.0.0.0', PORT), ProxyHandler)
    print(f'Listening on port {PORT}')
    server.serve_forever()
