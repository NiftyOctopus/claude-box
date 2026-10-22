"""
GitHub Reverse Proxy
Step 2a and 2c: Repo check and safe path check

Not yet checked: HTTP method, specific endpoints (rules.toml)
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


TIMEOUT = 60
CHUNK_SIZE = 64 * 1024 # Bytes per read when streaming the response

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
            body = f'DENY:  {self.command} {host}{self.path}\n {reason}\n'
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(body.encode())
            return

        self.forward(host.split(':')[0].lower())

    # http.server calls do_<METHOD>
    # Route them all to one place
    do_GET    = handle_any
    do_POST   = handle_any
    do_PUT    = handle_any
    do_PATCH  = handle_any
    do_DELETE = handle_any

    def forward(self, proxy_host):
        upstream_host, auth = UPSTREAMS[proxy_host]

        # Copy Claude's headers, then set our own Host and login
        headers = {k: v for k, v in self.headers.items() if k.lower() not in SKIP_REQUEST_HEADERS}
        headers['Host']          = upstream_host
        headers['Authorization'] = auth

        conn = http.client.HTTPSConnection(upstream_host, timeout=TIMEOUT)
        conn.request(self.command, self.path, headers=headers)
        response = conn.getresponse()

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


if __name__ == '__main__':
    allowed = ', '.join(sorted(REPOS)) or 'None'
    print(f'Allowed Repos: {allowed}')

    server = ThreadingHTTPServer(('0.0.0.0', PORT), ProxyHandler)
    print(f'Listening on port {PORT}')
    server.serve_forever()
