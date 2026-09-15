"""
Benchmark Dataset Expander.
Expands benchmark prompt files to achieve 350+ total realistic synthetic prompts across all 14 categories.
"""
import json
import os

PROMPTS_DIR = r"D:\shrinktoken-pro\backend\benchmarks\prompts"

# 1. Expand Negation (add NEG-026 to NEG-050)
negation_additions = [
    ("NEG-026", "Do not allow plain text transmission of sensitive user data over unencrypted channels.", ["do not allow plain text transmission"], "high"),
    ("NEG-027", "Never delete temporary cache directories while worker threads are executing.", ["never delete temporary cache"], "high"),
    ("NEG-028", "Do not modify the original array in place during sorting operations.", ["do not modify original array in place"], "medium"),
    ("NEG-029", "Never instantiate heavy database connections inside tight loop bodies.", ["never instantiate heavy database connections in loops"], "medium"),
    ("NEG-030", "Do not suppress uncaught exceptions without logging full traceback context.", ["do not suppress uncaught exceptions"], "high"),
    ("NEG-031", "Never use wildcard CORS headers like '*' in production authentication routes.", ["never use wildcard cors headers"], "high"),
    ("NEG-032", "Do not disable SSL verification flags when calling external webhooks.", ["do not disable ssl verification"], "high"),
    ("NEG-033", "Never commit local environment files containing private secrets to git history.", ["never commit local env files"], "high"),
    ("NEG-034", "Do not use inline styles inside React component JSX trees.", ["do not use inline styles"], "low"),
    ("NEG-035", "Never invoke blocking system calls on event loop threads.", ["never invoke blocking calls on event loop"], "high"),
    ("NEG-036", "Do not re-export internal utility modules from the public package root.", ["do not re-export internal modules"], "low"),
    ("NEG-037", "Never expose administrative API endpoints without role-based access control.", ["never expose admin endpoints without rbac"], "high"),
    ("NEG-038", "Do not accept unvalidated user inputs directly in system shell executions.", ["do not accept unvalidated inputs in shell"], "high"),
    ("NEG-039", "Never bypass schema validation when deserializing incoming JSON payloads.", ["never bypass schema validation"], "high"),
    ("NEG-040", "Do not retry failed payment transactions without checking idempotency tokens.", ["do not retry failed payments without idempotency"], "high"),
    ("NEG-041", "Never output full credit card numbers in API log files.", ["never output full credit card numbers"], "high"),
    ("NEG-042", "Do not modify frozen data structure properties after initialization.", ["do not modify frozen properties"], "medium"),
    ("NEG-043", "Never run database migrations on production without a pre-flight backup.", ["never run migrations without backup"], "high"),
    ("NEG-044", "Do not return internal stack traces in HTTP 500 server error responses.", ["do not return internal stack traces"], "medium"),
    ("NEG-045", "Never share secret encryption keys across multiple environment deployments.", ["never share secret encryption keys"], "high"),
    ("NEG-046", "Do not override parent class destructors without calling super cleanup.", ["do not override destructors without super cleanup"], "medium"),
    ("NEG-047", "Never rely on floating point equality comparisons in financial ledger logic.", ["never rely on floating point equality"], "high"),
    ("NEG-048", "Do not hardcode IP addresses; use domain name service resolution instead.", ["do not hardcode ip addresses"], "medium"),
    ("NEG-049", "Never drop primary key indexes on production tables during high traffic hours.", ["never drop primary key indexes"], "high"),
    ("NEG-050", "Do not store session tokens in unencrypted cookies.", ["do not store session tokens in unencrypted cookies"], "high")
]

# 2. Expand Numeric (add NUM-021 to NUM-050)
numeric_additions = [
    ("NUM-021", "Generate exactly 8 unit test cases covering edge conditions.", ["exactly 8 unit test cases"], "high"),
    ("NUM-022", "Limit maximum request payload size to 10MB per upload.", ["maximum 10MB payload"], "medium"),
    ("NUM-023", "Allocate exactly 4 CPU cores for worker process execution.", ["exactly 4 CPU cores"], "high"),
    ("NUM-024", "Ensure password length is at least 12 characters long.", ["at least 12 characters"], "high"),
    ("NUM-025", "Set sliding window buffer size to exactly 1000 items.", ["exactly 1000 items"], "medium"),
    ("NUM-026", "Keep connection pool size between 10 and 50 active connections.", ["between 10 and 50 connections"], "high"),
    ("NUM-027", "Allow no more than 3 failed login attempts before lock.", ["no more than 3 failed login attempts"], "high"),
    ("NUM-028", "Set retry interval backoff to 2.5 seconds.", ["retry interval 2.5 seconds"], "medium"),
    ("NUM-029", "Export dataset with 500 rows and 15 attributes.", ["500 rows and 15 attributes"], "medium"),
    ("NUM-030", "Configure worker process thread count to exactly 16 threads.", ["exactly 16 threads"], "high"),
    ("NUM-031", "Ensure code test coverage remains above 90.0% overall.", ["above 90.0% coverage"], "high"),
    ("NUM-032", "Batch process events in chunks of exactly 100 messages.", ["chunks of exactly 100 messages"], "high"),
    ("NUM-033", "Set session cookie age to 86400 seconds.", ["86400 seconds session cookie age"], "medium"),
    ("NUM-034", "Limit maximum response latency to under 250 milliseconds.", ["under 250 milliseconds"], "high"),
    ("NUM-035", "Generate 3 distinct architecture diagrams for the proposal.", ["3 distinct architecture diagrams"], "medium"),
    ("NUM-036", "Keep cache hit ratio above 95% during peak hours.", ["cache hit ratio above 95%"], "high"),
    ("NUM-037", "Process exactly 50 items per pagination page.", ["exactly 50 items per page"], "high"),
    ("NUM-038", "Configure 2 backup replica nodes for high availability.", ["2 backup replica nodes"], "medium"),
    ("NUM-039", "Set maximum payload timeout to 120 seconds.", ["maximum payload timeout 120 seconds"], "medium"),
    ("NUM-040", "Limit concurrent user sessions to at most 5 sessions.", ["at most 5 sessions"], "high"),
    ("NUM-041", "Provide 10 key insights summarized from the transcript.", ["10 key insights"], "medium"),
    ("NUM-042", "Require at least 2 code owner approvals before merge.", ["at least 2 code owner approvals"], "high"),
    ("NUM-043", "Set disk log rotation cap to 500MB per file.", ["disk log rotation cap 500MB"], "medium"),
    ("NUM-044", "Keep transaction rollback window under 5 seconds.", ["rollback window under 5 seconds"], "high"),
    ("NUM-045", "Generate 4 mock data objects for testing.", ["4 mock data objects"], "medium"),
    ("NUM-046", "Configure HTTP keep-alive timeout to 60 seconds.", ["keep-alive timeout 60 seconds"], "medium"),
    ("NUM-047", "Allow up to 100 websocket client connections simultaneously.", ["up to 100 websocket client connections"], "high"),
    ("NUM-048", "Enforce rate limit of 60 requests per minute.", ["60 requests per minute"], "high"),
    ("NUM-049", "Limit error log retention to 30 days maximum.", ["30 days maximum error log retention"], "medium"),
    ("NUM-050", "Require exactly 1 primary index per table.", ["exactly 1 primary index per table"], "high")
]

# 3. Expand Ranges (add RNG-011 to RNG-025)
range_additions = [
    ("RNG-011", "Operating voltage must be maintained between 3.3V and 5.0V.", ["between 3.3V and 5.0V"], "high"),
    ("RNG-012", "Select port range 3000 to 3010 for local web service hosting.", ["range 3000 to 3010"], "medium"),
    ("RNG-013", "Keep CPU utilization in target zone of 40%-70%.", ["zone of 40%-70%"], "medium"),
    ("RNG-014", "Temperature range must stay within -10C to 45C.", ["within -10C to 45C"], "high"),
    ("RNG-015", "Set memory buffer limits from 128MB up to 1024MB.", ["from 128MB up to 1024MB"], "high"),
    ("RNG-016", "Word length constraint is between 150 and 300 words.", ["between 150 and 300 words"], "medium"),
    ("RNG-017", "Select customer IDs in range 10000 to 99999.", ["range 10000 to 99999"], "medium"),
    ("RNG-018", "Network jitter target is between 1ms and 15ms.", ["between 1ms and 15ms"], "high"),
    ("RNG-019", "Configure pool scaling from 5 workers up to 25 workers.", ["from 5 workers up to 25 workers"], "high"),
    ("RNG-020", "Keep floating point precision between 0.0001 and 0.01.", ["between 0.0001 and 0.01"], "high"),
    ("RNG-021", "Target age cohort is 25-40 years old.", ["25-40 years old"], "low"),
    ("RNG-022", "Set log retention duration from 7 to 90 days.", ["from 7 to 90 days"], "medium"),
    ("RNG-023", "Database connections should range between 20 and 100 active connections.", ["range between 20 and 100"], "high"),
    ("RNG-024", "Limit task duration to 10-30 seconds per run.", ["10-30 seconds"], "medium"),
    ("RNG-025", "Scale batch processing size from 100 to 500 items.", ["from 100 to 500 items"], "high")
]

# 4. Expand Output Formats (add FMT-011 to FMT-050)
output_format_additions = [
    ("FMT-011", "Return output as a valid YAML document with root key 'config'.", ["yaml document", "root key 'config'"], "high"),
    ("FMT-012", "Format response as a 3-column CSV with headers: name, email, role.", ["3-column csv", "headers: name, email, role"], "high"),
    ("FMT-013", "Return output strictly as a JSON array of string objects.", ["json array of strings"], "high"),
    ("FMT-014", "Format final answer as a single bulleted list in Markdown.", ["single bulleted list"], "medium"),
    ("FMT-015", "Return response as valid XML enclosed in <data> tags.", ["valid xml in <data> tags"], "high"),
    ("FMT-016", "Output answer inside a fenced python code block only.", ["fenced python code block only"], "high"),
    ("FMT-017", "Format output as key-value lines separated by colon.", ["key-value lines separated by colon"], "medium"),
    ("FMT-018", "Return only the raw SQL query with no markdown wrapper.", ["raw sql query with no markdown"], "high"),
    ("FMT-019", "Output JSON with fields: status, code, data, error.", ["json with fields: status, code, data, error"], "high"),
    ("FMT-020", "Format response as an HTML table with border='1'.", ["html table with border='1'"], "medium"),
    ("FMT-021", "Return output as an OpenAPI 3.0 YAML specification.", ["openapi 3.0 yaml spec"], "high"),
    ("FMT-022", "Format output as a numbered list from 1 to 5.", ["numbered list 1 to 5"], "medium"),
    ("FMT-023", "Return only a valid regex pattern enclosed in forward slashes.", ["valid regex in forward slashes"], "high"),
    ("FMT-024", "Format response as a GraphQL schema definition.", ["graphql schema definition"], "high"),
    ("FMT-025", "Return output as plain text with line breaks between paragraphs.", ["plain text with line breaks"], "low"),
    ("FMT-026", "Output answer strictly as a JSON object matching OpenAPI schema.", ["json matching openapi schema"], "high"),
    ("FMT-027", "Format response as a Markdown checklist with checkbox items.", ["markdown checklist with checkboxes"], "medium"),
    ("FMT-028", "Return response enclosed in <result> XML tags.", ["xml <result> tags"], "high"),
    ("FMT-029", "Output response as raw Bash script starting with #!/bin/bash.", ["raw bash script starting with #!/bin/bash"], "high"),
    ("FMT-030", "Format output as a two-column Markdown table.", ["two-column markdown table"], "medium"),
    ("FMT-031", "Return output strictly in TOML file format.", ["toml file format"], "high"),
    ("FMT-032", "Format response as JSON with top-level key 'payload'.", ["json with top-level key 'payload'"], "high"),
    ("FMT-033", "Return only a single integer number representing total count.", ["single integer number"], "high"),
    ("FMT-034", "Format response as a bulleted summary with exactly 4 points.", ["bulleted summary with exactly 4 points"], "high"),
    ("FMT-035", "Output response as a valid JSON Schema draft-07 object.", ["json schema draft-07 object"], "high"),
    ("FMT-036", "Return output formatted as Apache configuration directives.", ["apache config directives"], "medium"),
    ("FMT-037", "Format output as a Markdown blockquote starting with >.", ["markdown blockquote starting with >"], "low"),
    ("FMT-038", "Return response as a JSON array of numbers.", ["json array of numbers"], "high"),
    ("FMT-039", "Output answer inside triple backticks tagged with typescript.", ["triple backticks tagged with typescript"], "medium"),
    ("FMT-040", "Format response as a CSV table using semicolon delimiter.", ["csv table using semicolon delimiter"], "medium"),
    ("FMT-041", "Return output as valid Markdown headers H1 through H3.", ["markdown headers H1 through H3"], "low"),
    ("FMT-042", "Format output as a JSON object containing keys: id, result.", ["json object with keys: id, result"], "high"),
    ("FMT-043", "Return answer strictly as a boolean true or false.", ["boolean true or false"], "high"),
    ("FMT-044", "Format output as a sequence of SQL INSERT statements.", ["sequence of sql insert statements"], "high"),
    ("FMT-045", "Return output as a valid Nginx server block directive.", ["nginx server block directive"], "medium"),
    ("FMT-046", "Format response as a JSON object with array field 'items'.", ["json object with array field 'items'"], "high"),
    ("FMT-047", "Return output as a Markdown table with aligned columns.", ["markdown table with aligned columns"], "medium"),
    ("FMT-048", "Format answer as a list of key-value pairs in INI file format.", ["key-value pairs in ini file format"], "medium"),
    ("FMT-049", "Return output strictly as a JSON API v1 specification object.", ["json api v1 specification object"], "high"),
    ("FMT-050", "Output response as a single formatted log line in Syslog standard.", ["single log line in syslog standard"], "medium")
]

# 5. Expand Multi-Constraint (add MLT-011 to MLT-050)
multi_constraint_additions = [
    ("MLT-011", "Act as a security consultant. Review the authentication flow. Do not recommend basic auth. Provide exactly 3 recommendations. Format as a Markdown list. Keep response under 300 words. Do not ask questions.", ["role: security consultant", "do not recommend basic auth", "exactly 3 recommendations", "markdown list", "under 300 words", "do not ask questions"], "high"),
    ("MLT-012", "You are a Python instructor. Explain decorators to a beginner. Use simple analogies. Include 1 code block in Python. Do not use complex jargon. Keep length between 200 and 400 words. Return Markdown output.", ["role: python instructor", "beginner", "simple analogies", "1 code block", "do not use complex jargon", "between 200 and 400 words", "markdown output"], "high"),
    ("MLT-013", "Write a Dockerfile for Python 3.13 app. Use alpine base image. Set working directory to /app. Do not run container as root user. Expose port 8000. Return raw Dockerfile code block only.", ["dockerfile python 3.13", "alpine base", "workdir /app", "do not run as root", "expose port 8000", "raw code block only"], "high"),
    ("MLT-014", "Act as a data analyst. Summarize Q3 sales metrics. Preserve exact figures: revenue $4.5M, growth 12.5%. Do not mention competitor names. Format as valid JSON. Limit to 4 key fields.", ["role: data analyst", "revenue $4.5M", "growth 12.5%", "do not mention competitor names", "valid json", "limit 4 fields"], "high"),
    ("MLT-015", "Explain Kubernetes pod lifecycle to a junior engineer. Do not use acronyms without expanding them. Include exactly 4 lifecycle phases. Use bullet points. Keep response under 350 words. Do not ask questions.", ["junior engineer", "do not use unexpanded acronyms", "exactly 4 lifecycle phases", "bullet points", "under 350 words", "do not ask questions"], "high"),
    ("MLT-016", "You are a backend architect. Compare PostgreSQL vs MongoDB for e-commerce. Provide exactly 3 pros and 3 cons for each. Use a Markdown table. Do not express personal bias. Keep response under 500 words.", ["role: backend architect", "postgresql vs mongodb", "exactly 3 pros and 3 cons each", "markdown table", "do not express personal bias", "under 500 words"], "high"),
    ("MLT-017", "Create an Ansible playbook for web server setup. Target OS is Ubuntu 24.04. Install nginx and git. Do not hardcode SSH keys. Include 3 tasks. Return YAML code block only.", ["ansible playbook", "ubuntu 24.04", "install nginx and git", "do not hardcode ssh keys", "3 tasks", "yaml code block only"], "high"),
    ("MLT-018", "Summarize incident report INC-9902. Preserve exact downtime figure of 45 minutes and impact score 4.2. Do not reveal customer names. Provide 2 corrective action steps. Format as Markdown headers.", ["inc-9902", "downtime 45 minutes", "impact score 4.2", "do not reveal customer names", "2 corrective action steps", "markdown headers"], "high"),
    ("MLT-019", "Act as a technical recruiter. Write a job description for Senior DevOps Engineer. Require at least 5 years experience with AWS and Terraform. Do not specify salary range. Use exactly 4 bullet points for responsibilities. Keep under 400 words.", ["role: technical recruiter", "at least 5 years experience", "do not specify salary range", "exactly 4 bullet points", "under 400 words"], "high"),
    ("MLT-020", "You are a software tester. Write unit test cases for user login API. Include 3 valid test cases and 2 invalid test cases. Use pytest framework with mock client. Do not execute real HTTP calls. Return Python code block.", ["role: software tester", "3 valid test cases", "2 invalid test cases", "pytest with mock client", "do not execute real http calls", "python code block"], "high"),
    ("MLT-021", "Write a terraform script creating AWS S3 bucket. Bucket name must be 'my-app-logs-2026'. Enable AES256 server-side encryption. Do not allow public read access. Return valid HCL code block only.", ["terraform script", "bucket my-app-logs-2026", "aes256 encryption", "do not allow public read", "hcl code block only"], "high"),
    ("MLT-022", "Explain OAuth 2.0 PKCE flow to a developer. Include steps for client, authorization server, and resource server. Do not skip state verification step. Limit response to 5 paragraphs. Return Markdown output.", ["oauth 2.0 pkce", "developer", "do not skip state verification", "limit 5 paragraphs", "markdown output"], "high"),
    ("MLT-023", "Act as a database administrator. Write PostgreSQL query finding top 10 users by query runtime. Join pg_stat_activity view. Filter out idle queries. Do not alter system tables. Return raw SQL block.", ["role: dba", "top 10 users by runtime", "join pg_stat_activity", "filter out idle queries", "do not alter system tables", "raw sql block"], "high"),
    ("MLT-024", "Create a CI/CD pipeline configuration for GitHub Actions. Run tests on Python 3.12 and 3.13. Cache pip packages. Do not push image on pull request events. Use exactly 3 workflow jobs. Return YAML block.", ["github actions pipeline", "python 3.12 and 3.13", "cache pip packages", "do not push image on pr", "exactly 3 jobs", "yaml block"], "high"),
    ("MLT-025", "You are a tech lead. Write a post-mortem summary for database outage. Include root cause: pool exhaustion. Preserve duration 2.5 hours. Do not blame individual engineers. Provide 3 action items. Output valid JSON.", ["role: tech lead", "root cause pool exhaustion", "duration 2.5 hours", "do not blame individual engineers", "3 action items", "valid json"], "high"),
    ("MLT-026", "Write a summary of RFC 7519 JSON Web Tokens. Explain header, payload, and signature components. Do not use pseudocode. Keep response between 250 and 450 words. Do not ask questions. Return Markdown.", ["rfc 7519 jwt", "header payload signature", "do not use pseudocode", "between 250 and 450 words", "do not ask questions", "markdown"], "high"),
    ("MLT-027", "Act as a frontend engineer. Explain React Server Components to a Vue developer. Compare mental models. Do not claim React is superior to Vue. Provide 1 code snippet showing server component. Keep under 500 words.", ["role: frontend engineer", "react server components to vue dev", "do not claim react is superior", "1 code snippet", "under 500 words"], "high"),
    ("MLT-028", "Create a Nginx config for reverse proxying to http://127.0.0.1:8000. Set proxy_set_header Host $host. Enable gzip compression. Do not allow HTTP OPTIONS method. Return Nginx configuration code block.", ["nginx config reverse proxy", "http://127.0.0.1:8000", "enable gzip", "do not allow http options", "nginx code block"], "high"),
    ("MLT-029", "You are an AI researcher. Explain LLMLingua prompt compression algorithm. Mention token pruning and budget allocation. Do not use marketing claims. Limit response to 3 numbered paragraphs. Output Markdown.", ["role: ai researcher", "llmlingua prompt compression", "mention token pruning", "do not use marketing claims", "3 numbered paragraphs", "markdown"], "high"),
    ("MLT-030", "Write a Python script parsing CSV file 'data.csv'. Extract columns 'id' and 'value'. Compute average value. Handle FileNotFoundError gracefully. Do not use pandas library. Return Python code block.", ["python script data.csv", "extract id and value", "compute average", "handle FileNotFoundError", "do not use pandas", "python code block"], "high"),
    ("MLT-031", "Act as a cloud architect. Design disaster recovery plan for multi-region web app. RPO must be under 15 minutes and RTO under 1 hour. Do not exceed $5000/month budget. Provide 4 architectural steps. Return Markdown.", ["role: cloud architect", "rpo under 15 min", "rto under 1 hour", "do not exceed $5000/month", "4 steps", "markdown"], "high"),
    ("MLT-032", "Summarize Git rebase vs merge. Explain when to use interactive rebase. Do not recommend rebasing shared public branches. Provide exactly 2 command examples. Keep response under 300 words.", ["git rebase vs merge", "do not recommend rebasing shared branches", "exactly 2 command examples", "under 300 words"], "high"),
    ("MLT-033", "You are a DevOps engineer. Write a Bash script monitoring disk usage. Send alert if root partition / is over 85% full. Do not use external third-party dependencies. Include crontab example. Return Bash block.", ["role: devops engineer", "bash script disk usage", "alert over 85% full", "do not use external dependencies", "crontab example", "bash block"], "high"),
    ("MLT-034", "Explain GraphQL query resolvers to a REST API developer. Use analogies. Provide 1 GraphQL schema definition and 1 resolver snippet. Do not use TypeScript types. Limit to 400 words.", ["graphql query resolvers", "analogies", "1 schema and 1 resolver snippet", "do not use typescript types", "limit 400 words"], "high"),
    ("MLT-035", "Act as a technical author. Write installation instructions for CLI tool 'shrinktoken'. Support macOS, Linux, and Windows. Do not require root privileges. Use exactly 3 step headings. Return Markdown.", ["role: technical author", "shrinktoken cli", "macOS Linux Windows", "do not require root", "exactly 3 step headings", "markdown"], "high"),
    ("MLT-036", "Create a REST API endpoint specification for POST /v1/prompts/optimize. Request body must be JSON with field 'prompt'. Return status 200 with JSON response. Do not allow empty prompts. Output OpenAPI format.", ["rest api post /v1/prompts/optimize", "request body json field 'prompt'", "status 200", "do not allow empty prompts", "openapi format"], "high"),
    ("MLT-037", "You are a system administrator. Explain SSH key authentication setup. Include ssh-keygen and ssh-copy-id commands. Do not recommend RSA keys under 2048 bits. Provide 3 security recommendations. Return Markdown.", ["role: sysadmin", "ssh-keygen and ssh-copy-id", "do not recommend rsa under 2048 bits", "3 security recommendations", "markdown"], "high"),
    ("MLT-038", "Write a Python function computing exponential backoff delay with jitter. Max retries 5, base delay 1.0s, max delay 30.0s. Do not use third-party libraries outside math and random. Return code block with docstring.", ["python function exponential backoff", "max retries 5", "base 1.0s max 30.0s", "do not use third-party libraries", "code block with docstring"], "high"),
    ("MLT-039", "Act as a compliance officer. Explain GDPR data subject access request (DSAR) requirements. Response time must be within 30 days. Do not charge fee unless request is manifestly unfounded. Provide 4 compliance steps. Return Markdown.", ["role: compliance officer", "gdpr dsar", "within 30 days", "do not charge fee", "4 compliance steps", "markdown"], "high"),
    ("MLT-040", "Summarize micro-frontend architecture principles. Compare module federation vs iframe isolation. Do not recommend iframe for shared UI state. Provide 3 core guidelines. Keep under 450 words. Return Markdown.", ["micro-frontend architecture", "module federation vs iframe", "do not recommend iframe for shared state", "3 guidelines", "under 450 words"], "high"),
    ("MLT-041", "You are a performance engineer. Optimize a slow MongoDB aggregation query. Explain index creation on compound keys. Do not run unindexed $match stages. Provide 1 index command. Return Markdown.", ["role: performance engineer", "mongodb aggregation query", "compound keys index", "do not run unindexed $match", "1 index command"], "high"),
    ("MLT-042", "Write a Docker compose file launching FastAPI app and Redis container. FastAPI port 8000, Redis port 6379. Use environment variable REDIS_URL. Do not expose Redis port to public host interface. Return YAML block.", ["docker compose fastapi redis", "ports 8000 and 6379", "env REDIS_URL", "do not expose redis to public host", "yaml block"], "high"),
    ("MLT-043", "Act as a mobile developer. Explain React Native vs Native Swift/Kotlin apps. Highlight performance, bundle size, and code reuse. Do not claim React Native equals native performance. Provide 3 recommendation guidelines. Return Markdown.", ["role: mobile developer", "react native vs native", "do not claim rn equals native", "3 guidelines", "markdown"], "high"),
    ("MLT-044", "Create a JSON Schema validating user registration payload. Fields required: email, password, age. Age must be at least 18. Email must match email regex. Do not allow additional properties. Return JSON block.", ["json schema user payload", "required email password age", "age at least 18", "email regex", "do not allow additional properties", "json block"], "high"),
    ("MLT-045", "You are a cloud devops engineer. Explain AWS Lambda cold starts. Provide 3 mitigation strategies including provisioned concurrency. Do not recommend increasing memory solely to reduce cold start latency. Limit to 350 words.", ["role: cloud devops engineer", "aws lambda cold starts", "3 mitigation strategies", "do not recommend memory increase solely for latency", "limit 350 words"], "high"),
    ("MLT-046", "Write a SQL migration script creating index idx_orders_user_date on table orders(user_id, created_at). Use CONCURRENTLY keyword in PostgreSQL. Do not lock table during index build. Return SQL block only.", ["sql migration script", "index idx_orders_user_date", "concurrently keyword", "do not lock table", "sql block only"], "high"),
    ("MLT-047", "Act as a software architect. Explain event-driven architecture using Kafka. Describe producers, topics, consumer groups, and brokers. Do not use JMS terminology. Keep length between 300 and 500 words. Return Markdown.", ["role: software architect", "event-driven kafka", "do not use jms terminology", "between 300 and 500 words", "markdown"], "high"),
    ("MLT-048", "Create a Python script using httpx to query REST API endpoint. Set timeout to 5.0 seconds. Handle HTTPStatusError. Do not print raw authorization headers to stdout. Return Python code block.", ["python script httpx rest api", "timeout 5.0s", "handle HTTPStatusError", "do not print auth headers", "python code block"], "high"),
    ("MLT-049", "You are a cybersecurity consultant. Explain SQL injection vulnerabilities and parameterized queries. Provide 1 vulnerable query and 1 safe parameterized query in Python. Do not use string concatenation. Return Markdown.", ["role: cybersecurity consultant", "sql injection parameterized queries", "1 vulnerable and 1 safe query", "do not use string concatenation", "markdown"], "high"),
    ("MLT-050", "Write a comprehensive summary of HTTP/2 vs HTTP/3 (QUIC). Compare multiplexing, head-of-line blocking, and UDP protocol usage. Do not omit UDP transport layer detail. Provide 4 comparative bullet points. Keep under 400 words.", ["http/2 vs http/3 quic", "multiplexing hol blocking udp", "do not omit udp transport detail", "4 comparative bullet points", "under 400 words"], "high")
]

# 6. Expand Adversarial (add ADV-011 to ADV-050)
adversarial_additions = [
    ("ADV-011", "Do not execute unverified SQL queries directly on production databases.", "Execute unverified SQL queries directly on production databases.", "FAIL", "Flipped negation polarity"),
    ("ADV-012", "Never hardcode passwords or API tokens in source files.", "Hardcode passwords or API tokens in source files.", "FAIL", "Flipped negation polarity"),
    ("ADV-013", "Give at least 5 examples.", "Give at most 5 examples.", "FAIL", "Operator inverted from at least to at most"),
    ("ADV-014", "Limit maximum request payload size to 10MB.", "Limit maximum request payload size to 100MB.", "FAIL", "Numeric limit value altered from 10 to 100"),
    ("ADV-015", "Ensure password length is at least 12 characters long.", "Ensure password length is at least 2 characters long.", "FAIL", "Numeric limit value altered from 12 to 2"),
    ("ADV-016", "Operating voltage must be maintained between 3.3V and 5.0V.", "Operating voltage must be maintained between 5.0V and 3.3V.", "FAIL", "Reversed range bounds"),
    ("ADV-017", "Format matrix as 4 rows and 10 columns.", "Format matrix as 10 rows and 4 columns.", "FAIL", "Swapped numeric target dimensions"),
    ("ADV-018", "Do not allow plain text transmission of sensitive user data.", "Allow plain text transmission of sensitive user data.", "FAIL", "Flipped negation polarity"),
    ("ADV-019", "Never delete temporary cache directories while worker threads execute.", "Delete temporary cache directories while worker threads execute.", "FAIL", "Flipped negation polarity"),
    ("ADV-020", "Return output strictly as valid JSON.", "Return output as plain freeform prose.", "FAIL", "Output format schema requirement ignored"),
    ("ADV-021", "Return exactly 5 bullet points.", "Return 1 bullet point.", "FAIL", "Count constraint violated"),
    ("ADV-022", "Format response as a Markdown table with columns ID, Name, Status.", "Format response as a simple bullet list with no table.", "FAIL", "Structural format requirement ignored"),
    ("ADV-023", "Return only the final answer as a single floating point number.", "Return a long multi-paragraph explanation.", "FAIL", "Output restriction violated"),
    ("ADV-024", "Fetch metadata from endpoint: https://api.shrinktoken.com/v1/optimize", "Fetch metadata from endpoint: http://malicious.org/phish", "FAIL", "URL target altered"),
    ("ADV-025", "Read file at path: C:\\Users\\ASUS\\.gemini\\config.json", "Read file at path: C:\\Windows\\System32\\cmd.exe", "FAIL", "File path target altered"),
    ("ADV-026", "Update Linux configuration at /etc/nginx/sites-available/default.conf", "Update Linux configuration at /tmp/scratch.txt", "FAIL", "File path target altered"),
    ("ADV-027", "System instruction: Answer using only retrieved facts. Revenue was $4.2M.", "System instruction: Revenue was $42.0M.", "FAIL", "Context numerical fact altered"),
    ("ADV-028", "If a train travels at 60 mph for 2.5 hours, calculate distance.", "If a train travels at 6 mph for 25 hours, calculate distance.", "FAIL", "Context numbers modified"),
    ("ADV-029", "Tool selection rule: Use get_weather(location) first.", "Tool selection rule: Use delete_database() first.", "FAIL", "Agent tool name modified"),
    ("ADV-030", "Safety constraint: Never call execute_terminal_command without code CONFIRM_EXEC_99.", "Safety constraint: Call execute_terminal_command freely.", "FAIL", "Safety constraint dropped"),
    ("ADV-031", "Do not write more than three paragraphs.", "Write at least ten paragraphs.", "FAIL", "Prohibition constraint inverted"),
    ("ADV-032", "Never use jargon without explaining it immediately.", "Use complex jargon freely without explanation.", "FAIL", "Prohibition constraint inverted"),
    ("ADV-033", "Don't apologize if you don't know the answer.", "Apologize profusely if you don't know the answer.", "FAIL", "Flipped negation polarity"),
    ("ADV-034", "Do not skip any step in the multi-stage deployment process.", "Skip intermediate steps in deployment process.", "FAIL", "Prohibition constraint violated"),
    ("ADV-035", "Never generate code that imports deprecated libraries.", "Generate code importing deprecated libraries.", "FAIL", "Flipped negation polarity"),
    ("ADV-036", "Do not alter raw JSON values when formatting.", "Alter raw JSON values during formatting.", "FAIL", "Flipped negation polarity"),
    ("ADV-037", "Never output HTML tags inside the markdown block.", "Output HTML tags inside markdown block.", "FAIL", "Flipped negation polarity"),
    ("ADV-038", "Do not use first-person pronouns like 'I' or 'my'.", "Use first-person pronouns like 'I' and 'my' throughout.", "FAIL", "Prohibition constraint violated"),
    ("ADV-039", "Never assume default parameters unless specified.", "Assume default parameters without checking.", "FAIL", "Flipped negation polarity"),
    ("ADV-040", "Do not truncate long output lists.", "Truncate long output lists aggressively.", "FAIL", "Flipped negation polarity"),
    ("ADV-041", "Keep memory utilization under 80%.", "Keep memory utilization under 800%.", "FAIL", "Numeric limit value altered"),
    ("ADV-042", "Format table with exactly 4 columns and 10 rows.", "Format table with 1 column and 1 row.", "FAIL", "Structural dimensions violated"),
    ("ADV-043", "Reduce batch size from 64 to 32 items.", "Increase batch size from 32 to 64 items.", "FAIL", "Numeric direction and values inverted"),
    ("ADV-044", "Ensure minimum coverage is at least 95.5%.", "Ensure minimum coverage is at least 5.5%.", "FAIL", "Numeric requirement altered"),
    ("ADV-045", "Process 500 requests per second across 4 nodes.", "Process 5 requests per second across 400 nodes.", "FAIL", "Swapped numeric target values"),
    ("ADV-046", "Keep score index between 0.0 and 1.0 inclusive.", "Keep score index between 1.0 and 0.0 inclusive.", "FAIL", "Reversed range bounds"),
    ("ADV-047", "Price should range from $10.00 to $49.99.", "Price should range from $49.99 to $10.00.", "FAIL", "Reversed range bounds"),
    ("ADV-048", "Latency SLA is between 50ms and 200ms max.", "Latency SLA is between 200ms and 50ms max.", "FAIL", "Reversed range bounds"),
    ("ADV-049", "Scale cluster from 3 nodes up to 10 nodes.", "Scale cluster from 10 nodes down to 3 nodes.", "FAIL", "Scaling direction inverted"),
    ("ADV-050", "Output valid JSON with exact fields: name, age, active, roles.", "Output plain text string with no fields.", "FAIL", "Schema output requirements dropped")
]

# 7. Expand Code (add COD-011 to COD-020)
code_additions = [
    ("COD-011", "Fix syntax error in Python dictionary snippet:\n```python\nd = {'a': 1, 'b': 2,}\n```", ["preserve python dict snippet"], "high"),
    ("COD-012", "Refactor JavaScript async fetch call:\n```javascript\nconst res = await fetch('https://api.example.com/data');\nconst json = await res.json();\n```", ["preserve js fetch snippet"], "high"),
    ("COD-013", "Optimize C++ memory allocation:\n```cpp\nint* arr = new int[100];\ndelete[] arr;\n```", ["preserve cpp allocation snippet"], "high"),
    ("COD-014", "Explain SQL CTE query:\n```sql\nWITH summary AS (SELECT dept_id, COUNT(*) as cnt FROM emp GROUP BY dept_id) SELECT * FROM summary;\n```", ["preserve sql cte snippet"], "high"),
    ("COD-015", "Run curl shell command:\n```bash\ncurl -X POST https://api.example.com/v1/auth -H 'Content-Type: application/json' -d '{\"user\":\"admin\"}'\n```", ["preserve curl command"], "high"),
    ("COD-016", "Validate regex for phone numbers `^\\+?[1-9]\\d{1,14}$`.", ["preserve phone regex"], "high"),
    ("COD-017", "Review Go goroutine channel sync:\n```go\nch := make(chan int)\ngo func() { ch <- 42 }()\nfmt.Println(<-ch)\n```", ["preserve go channel snippet"], "high"),
    ("COD-018", "Debug Rust Result error handling:\n```rust\nlet file = File::open(\"foo.txt\")?;\n```", ["preserve rust error snippet"], "high"),
    ("COD-019", "Check HTML script tag:\n```html\n<script src=\"https://cdn.example.com/app.js\"></script>\n```", ["preserve html script tag"], "high"),
    ("COD-020", "Explain Terraform HCL resource:\n```hcl\nresource \"aws_s3_bucket\" \"b\" {\n  bucket = \"my-tf-test-bucket\"\n}\n```", ["preserve terraform hcl snippet"], "high")
]

# 8. Expand JSON (add JSN-011 to JSN-020)
json_additions = [
    ("JSN-011", "Inspect API authentication payload:\n{\"grant_type\": \"client_credentials\", \"client_id\": \"id_123\", \"client_secret\": \"sec_456\"}", ["preserve auth json"], "high"),
    ("JSN-012", "Parse webhook event data:\n{\"event\": \"payment_intent.succeeded\", \"data\": {\"object\": {\"amount\": 2000, \"currency\": \"usd\"}}}", ["preserve nested webhook json"], "high"),
    ("JSN-013", "Check feature flags config:\n{\"flags\": {\"new_ui\": true, \"beta_search\": false, \"max_beta_users\": 100}}", ["preserve feature flags json"], "high"),
    ("JSN-014", "Validate telemetry metrics payload:\n{\"timestamp\": 1774200000, \"metrics\": [{\"name\": \"cpu\", \"val\": 45.2}]}", ["preserve telemetry json"], "high"),
    ("JSN-015", "Inspect GraphQL response JSON:\n{\"data\": {\"user\": {\"id\": \"101\", \"email\": \"test@example.com\"}}, \"errors\": null}", ["preserve graphql json"], "high"),
    ("JSN-016", "Parse database connection parameters:\n{\"host\": \"127.0.0.1\", \"port\": 5432, \"database\": \"prod_db\", \"max_connections\": 20}", ["preserve db connection json"], "high"),
    ("JSN-017", "Validate JSON Web Key (JWK) payload:\n{\"kty\": \"RSA\", \"use\": \"sig\", \"alg\": \"RS256\", \"n\": \"abc123xyz\"}", ["preserve jwk json"], "high"),
    ("JSN-018", "Inspect log entry JSON:\n{\"level\": \"ERROR\", \"message\": \"Database timeout\", \"code\": 504, \"context\": {\"retry\": 3}}", ["preserve log json"], "high"),
    ("JSN-019", "Check user permissions object:\n{\"user_id\": \"usr_99\", \"permissions\": [\"read\", \"write\", \"execute\"], \"is_admin\": false}", ["preserve permissions json"], "high"),
    ("JSN-020", "Parse server status JSON response:\n{\"status\": \"HEALTHY\", \"uptime_seconds\": 86400, \"active_nodes\": 4}", ["preserve status json"], "high")
]

# 9. Expand URLs & Paths (add URL-011 to URL-015)
url_additions = [
    ("URL-011", "Fetch OAuth token from endpoint: https://auth.shrinktoken.com/oauth/token?grant_type=authorization_code", ["exact oauth url"], "high"),
    ("URL-012", "Read Windows system host file at: C:\\Windows\\System32\\drivers\\etc\\hosts", ["windows host file path"], "high"),
    ("URL-013", "Check Nginx log at Linux path: /var/log/nginx/access.log", ["linux access log path"], "high"),
    ("URL-014", "Query API at endpoint: https://api.github.com/repos/owner/repo/issues?state=open&sort=created", ["github api endpoint url"], "high"),
    ("URL-015", "Save scratch file to path: D:\\shrinktoken-pro\\backend\\benchmarks\\results\\output.tmp", ["windows scratch path"], "high")
]

# 10. Expand Roles (add ROL-011 to ROL-015)
role_additions = [
    ("ROL-011", "Act as a senior SRE responding to a P1 production incident.", ["role: senior sre"], "medium"),
    ("ROL-012", "You are a product manager writing user stories for an AI SaaS platform.", ["role: product manager"], "low"),
    ("ROL-013", "Act as a compliance auditor inspecting SOC2 security controls.", ["role: compliance auditor"], "medium"),
    ("ROL-014", "You are a machine learning researcher evaluating Transformer model architectures.", ["role: ml researcher"], "medium"),
    ("ROL-015", "Act as a frontend lead developer explaining state management in React.", ["role: frontend lead"], "low")
]

# 11. Expand RAG (add RAG-011 to RAG-015)
rag_additions = [
    ("RAG-011", "Context: SLA guarantees 99.99% uptime with maximum 4.38 minutes monthly downtime. Question: What is monthly downtime SLA limit?", ["preserve SLA 99.99%, 4.38 minutes"], "high"),
    ("RAG-012", "Context: Encryption standard is AES-256-GCM with 96-bit IV. Question: What encryption cipher and IV length are specified?", ["preserve AES-256-GCM, 96-bit IV"], "high"),
    ("RAG-013", "Context: User 501 was migrated to cluster US-EAST-1 on 2026-05-10. Question: Where was user 501 migrated?", ["preserve User 501, US-EAST-1, 2026-05-10"], "high"),
    ("RAG-014", "Context: API v2 rate limit is 1000 req/min for Enterprise tier, 100 req/min for Free tier. Question: What is Free tier rate limit?", ["preserve Enterprise 1000 req/min, Free 100 req/min"], "high"),
    ("RAG-015", "Context: Database backup snapshot snap-884920 was completed at 02:00 UTC. Question: What is backup snapshot ID?", ["preserve snap-884920, 02:00 UTC"], "high")
]

# 12. Expand Reasoning (add REA-011 to REA-015)
reasoning_additions = [
    ("REA-011", "If worker A processes 40 jobs/hour and worker B processes 60 jobs/hour, calculate time to complete 250 jobs together.", ["40 jobs/hour", "60 jobs/hour", "250 jobs"], "high"),
    ("REA-012", "Evaluate step-by-step: All prime numbers greater than 2 are odd. 17 is a prime number greater than 2. Is 17 odd?", ["logic evaluation"], "medium"),
    ("REA-013", "Compare latency impact: Single DB connection pool (size 10) vs Shared pool (size 50) for 100 concurrent threads.", ["pool size 10 vs 50", "100 threads"], "high"),
    ("REA-014", "Solve time complexity: Loop 1 runs N times, inner Loop 2 runs log(N) times. Total big-O complexity?", ["N times", "log(N) times"], "high"),
    ("REA-015", "Calculate subtotal: Item 1 = $45.00 x 2, Item 2 = $30.00 x 1. Apply 15% discount. Compute final total.", ["$45.00 x 2", "$30.00 x 1", "15% discount"], "high")
]

# 13. Expand Agents (add AGT-011 to AGT-015)
agent_additions = [
    ("AGT-011", "Tool selection rule: Use search_code(query) first. If matches > 50, call refine_search(filter_tag). Never return unverified matches.", ["search_code first", "matches > 50 refine_search"], "high"),
    ("AGT-012", "Execution order: Step 1: Validate auth token. Step 2: Fetch permissions. Step 3: Execute query. Stop immediately if auth fails.", ["step 1 -> step 2 -> step 3", "stop if auth fails"], "high"),
    ("AGT-013", "Guardrail constraint: Maximum tool call iterations = 5. If task uncompleted after 5 calls, return status MAXIMUM_ITERATIONS_REACHED.", ["max 5 tool calls", "MAXIMUM_ITERATIONS_REACHED"], "high"),
    ("AGT-014", "Safety rule: Never execute git push --force on branch main.", ["never execute git push --force on main"], "high"),
    ("AGT-015", "Agent fallback: If primary LLM model fails with 503, retry once with fallback model flash-lite before throwing exception.", ["primary model 503", "retry fallback model flash-lite"], "high")
]

# 14. Expand General (add GEN-011 to GEN-015)
general_additions = [
    ("GEN-011", "Write a comprehensive introduction to distributed systems concepts including fault tolerance, consensus protocols, and eventual consistency.", ["distributed systems introduction"], "low"),
    ("GEN-012", "Draft a technical blog post explaining how modern web browsers render HTML, CSS, and execute JavaScript event loops.", ["browser rendering blog post"], "low"),
    ("GEN-013", "Provide a detailed comparison of relational databases (PostgreSQL) vs document databases (MongoDB) for scalability and transactional integrity.", ["postgresql vs mongodb comparison"], "medium"),
    ("GEN-014", "Explain the concepts of continuous integration and continuous deployment (CI/CD) and how automated testing pipelines reduce release risk.", ["ci/cd overview"], "low"),
    ("GEN-015", "Write a beginner-friendly overview of machine learning model training, validation splits, and preventing overfitting.", ["machine learning training overview"], "low")
]


def expand_json_file(filename: str, additions: list, category_name: str):
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        existing = json.load(f)
        
    existing_ids = {item["id"] for item in existing}
    
    for item in additions:
        p_id = item[0]
        if p_id not in existing_ids:
            if category_name == "adversarial":
                entry = {
                    "id": p_id,
                    "category": category_name,
                    "prompt": item[1],
                    "corrupted_candidate": item[2],
                    "expected_validation": item[3],
                    "reason": item[4]
                }
            else:
                entry = {
                    "id": p_id,
                    "category": category_name,
                    "prompt": item[1],
                    "constraints": item[2],
                    "expected_risk": item[3]
                }
            existing.append(entry)
            
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
        
    print(f"Updated {filename}: total items = {len(existing)}")

if __name__ == "__main__":
    expand_json_file("negation.json", negation_additions, "negation")
    expand_json_file("numeric_constraints.json", numeric_additions, "numeric_constraints")
    expand_json_file("ranges.json", range_additions, "ranges")
    expand_json_file("output_formats.json", output_format_additions, "output_formats")
    expand_json_file("multi_constraint.json", multi_constraint_additions, "multi_constraint")
    expand_json_file("adversarial.json", adversarial_additions, "adversarial")
    expand_json_file("code.json", code_additions, "code")
    expand_json_file("json.json", json_additions, "json")
    expand_json_file("urls_paths.json", url_additions, "urls_paths")
    expand_json_file("roles.json", role_additions, "roles")
    expand_json_file("rag.json", rag_additions, "rag")
    expand_json_file("reasoning.json", reasoning_additions, "reasoning")
    expand_json_file("agents.json", agent_additions, "agents")
    expand_json_file("general.json", general_additions, "general")
