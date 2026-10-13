# CloudOps Insight Platform
A fresh 3-tier learning project: Nginx frontend, Flask REST API, and MySQL persistence. DevOps starter folders are included for GitLab CI, Docker, Kubernetes, Terraform, Argo CD, Prometheus, and Grafana.

## Run locally (Windows PowerShell)
1. Install and start Docker Desktop.
2. Copy `.env.example` to `.env`: `Copy-Item .env.example .env`
3. Run `docker compose up --build -d`
4. Open http://localhost
5. Check http://localhost/api/health
6. Stop with `docker compose down`. To also delete saved database data: `docker compose down -v`.

## Structure
- `frontend/`: HTML, CSS, JS and Nginx reverse proxy
- `backend/`: Flask REST API and MySQL connector
- `database/init/`: schema
- `k8s/`, `argocd/`, `terraform/`, `monitoring/`: deployment starters
- `.gitlab-ci.yml`: validation and image build/push pipeline starter
- `.env.example`: local environment template

## Important
The Compose app is the first milestone. Kubernetes/Argo CD/Terraform files are starter templates and require configuration before deployment. Change all example passwords. Never commit `.env`, AWS keys, PEM files, tokens, or real Kubernetes Secrets. Never expose MySQL publicly. Terraform state is local in this starter; configure remote state later.
