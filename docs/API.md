# API reference
- `GET /api` — API overview
- `GET /api/health` — checks database connectivity
- `GET /api/services` — list the latest 100 saved service records
- `POST /api/services` — save a record
- `GET /metrics` — Prometheus metrics endpoint

PowerShell example:
```powershell
$body = @{ name="Demo API"; category="Application"; environment="Development"; description="First saved record" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost/api/services" -Method Post -ContentType "application/json" -Body $body
Invoke-RestMethod -Uri "http://localhost/api/services"
```
