---
name: aws
description: Query YourStake AWS accounts and infrastructure details. Use when the user mentions AWS, any AWS service, or infrastructure in general.
---

# Basic Usage
- Use the `aws` CLI v2, at `/usr/local/bin/aws`
- No `boto3`
- Use `--query` and `--output text|table` for simple filtering
- Pipe json output to `jq` for complex transforms
- Region is always `us-east-1`


## Accounts

| Name          | Account ID     | Contains                   | Usage                |
|---------------|----------------|----------------------------|----------------------|
| yourstake.org | `155606071632` | Production RDS database    | Use `--profile db`   |
| production    | `533882791422` | All other production infra | No  `--profile` flag |


## Account: yourstake.org
- Contains our production RDS database `yourstake-production-1`
- Also has our read replica `yourstake-production-replica-1` (not used much at the moment)


## Account: production
*Contains all other production infrastructure*

### ECS Main Services

| Nickname | Partial Service Name  | Purpose                          |
|----------|-----------------------|----------------------------------|
| Web      | FargateService        | Main app web server              |
| AI       | AiService             | AI chat and agent jobs features  |
| Flower   | FlowerService         | Tool for monitoring celery tasks |


### ECS Services for Background Jobs

| Nickname         | Partial Service Name  | Framework | Broker   | Queues                   |
|------------------|-----------------------|-----------|----------|--------------------------|
| Default          | StakeCelery           | Celery    | AmazonMQ | `default`, `celery`      |
| DocMaster        | DocmasterCelery       | Celery    | AmazonMQ | `docmaster`              |
| Optimizer        | OptimizationCelery    | RQ        | Redis    | `high`, `default`, `low` |
| Custom Optimizer | CustomOptimizerCelery | Celery    | AmazonMQ | `custom_optimizer`       |
| Data             | DataCelery            | Celery    | AmazonMQ | *See below*              |
| Batch            | BatchCelery           | Celery    | AmazonMQ | `batch`                  |
| AI               | AiCelery              | Celery    | AmazonMQ | `ai`                     |

*Data Queues: classify_company, resolve_company, update_symbols, zulip, figi, add_symbol, zulip_alert_invalid_numeric, merge_duplicate_figi*


### CDK Code
*All located in /code/aws/*

| File                          | Purpose         |
|-------------------------------|-----------------|
| `pipeline-stack.js`           | Deploy pipeline |
| `app-stack.js`                | Main app        |
| `app/scheduled-task-stack.js` | Cron jobs       |
