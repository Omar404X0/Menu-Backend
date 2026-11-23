<div align="center">

<img src="assets/banner.svg" alt="Layali API" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=900&color=9DBB6B&center=true&vCenter=true&width=780&height=40&lines=POST+%2Fedit%2Flogin+%E2%86%92+bcrypt+%2B+Redis+session;Tokens+expire+automatically+after+1+hour;FastAPI+%C2%B7+SQLAlchemy+%C2%B7+PostgreSQL;Containerised+with+Docker+%C2%B7+Tested+with+pytest" alt="Typing animation" />
</a>

<br/>

<a href="https://menu-backend-grr7.onrender.com/docs"><img src="https://img.shields.io/badge/%F0%9F%93%9A%20%20SWAGGER%20DOCS-9dbb6b?style=for-the-badge&labelColor=2a1a12" alt="Swagger"/></a>
<a href="https://menu-backend-grr7.onrender.com/health"><img src="https://img.shields.io/badge/%F0%9F%92%9A%20%20HEALTH%20CHECK-dfc1d3?style=for-the-badge&labelColor=2a1a12" alt="Health"/></a>
<a href="https://github.com/Omar404X0/Menu-Frontend"><img src="https://img.shields.io/badge/%E2%98%95%20%20FRONTEND%20REPO-e0a878?style=for-the-badge&labelColor=2a1a12" alt="Frontend"/></a>

<br/><br/>

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,redis,docker,pytest,sqlalchemy&theme=dark" alt="stack"/>

<br/><br/>

![Status](https://img.shields.io/badge/status-live-9dbb6b?style=flat-square&labelColor=2a1a12)
![Render](https://img.shields.io/badge/deployed_on-Render-46E3B7?style=flat-square&logo=render&logoColor=black)
![Neon](https://img.shields.io/badge/database-Neon-00E599?style=flat-square&logo=neon&logoColor=black)
![Redis](https://img.shields.io/badge/sessions-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Auth](https://img.shields.io/badge/passwords-bcrypt-dfc1d3?style=flat-square&labelColor=2a1a12)

</div>

<img src="assets/divider.svg" width="100%" alt=""/>

<table align="center">
  <tr>
    <td align="center" width="25%"><h1>7</h1><sub><b>REST ENDPOINTS</b><br/>3 protected</sub></td>
    <td align="center" width="25%"><h1>2</h1><sub><b>DB TABLES</b><br/>menu · admin</sub></td>
    <td align="center" width="25%"><h1>1h</h1><sub><b>SESSION TTL</b><br/>auto-expiring in Redis</sub></td>
    <td align="center" width="25%"><h1>16</h1><sub><b>SEEDED ITEMS</b><br/>hot · cold · cake</sub></td>
  </tr>
</table>

<img src="assets/divider.svg" width="100%" alt=""/>

## 📖 Table of Contents

<table>
  <tr>
    <td>

- [✨ Overview](#-overview)
- [🏗️ Architecture](#️-architecture)
- [🔐 Authentication Flow](#-authentication-flow)
- [📡 API Reference](#-api-reference)
- [🗄️ Data Model](#️-data-model)

</td>
    <td>

- [🛡️ Security](#️-security)
- [🔧 Environment Variables](#-environment-variables)
- [🚀 Run Locally](#-run-locally)
- [🐳 Docker](#-docker)
- [🧪 Testing](#-testing)
- [🗺️ Roadmap](#️-roadmap)

</td>
  </tr>
</table>

<img src="assets/divider.svg" width="100%" alt=""/>

## ✨ Overview

The backend of **Layali Menu**, a café menu with an admin dashboard. A small, fast REST API that:

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🍽️ Serves the menu</h3>
      Public endpoint returning every item with its price and category.
    </td>
    <td width="50%" valign="top">
      <h3>🔐 Authenticates the admin</h3>
      Credentials are checked against <b>bcrypt</b> hashes. Passwords are never stored in plain text.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>⏱️ Manages sessions in Redis</h3>
      Each login creates a random token with an automatic <b>1-hour expiry</b>. No cleanup jobs needed.
    </td>
    <td width="50%" valign="top">
      <h3>✏️ Edits the menu</h3>
      Authenticated add, edit and delete, persisted in <b>PostgreSQL (Neon)</b> with a SQLite fallback for local work.
    </td>
  </tr>
</table>

> [!NOTE]
> The frontend lives in [Menu-Frontend](https://github.com/Omar404X0/Menu-Frontend): a Next.js app with the animated public menu and the admin dashboard.

> [!TIP]
> The API runs on a free Render instance. If it has been idle, the **first request can take ~30–50 seconds**.

<img src="assets/divider.svg" width="100%" alt=""/>

## 🏗️ Architecture

```mermaid
flowchart TB
    FE[🖥️ Next.js Frontend<br/>Vercel] -- HTTPS / JSON --> CORS{CORS<br/>FRONTEND_URL}
    CORS --> API

    subgraph Render["☁️ Render: Docker container"]
      API[⚡ FastAPI]
      API --> ORM[SQLAlchemy ORM]
      API --> PW[passlib / bcrypt]
    end

    ORM --> DB[(🐘 Neon PostgreSQL<br/>menu · admin)]
    API -- "SET session:token EX 3600" --> R[(🔴 Redis)]

    style API fill:#3a2418,stroke:#9dbb6b,color:#fff
    style DB fill:#2a1a12,stroke:#e0a878,color:#fff
    style R fill:#2a1a12,stroke:#dc382d,color:#fff
```

<img src="assets/divider.svg" width="100%" alt=""/>

## 🔐 Authentication Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as FastAPI
    participant D as PostgreSQL
    participant R as Redis

    C->>A: POST /edit/login {email, password}
    A->>D: SELECT admin WHERE email = ?
    D-->>A: admin row (bcrypt hash)
    A->>A: verify_password(plain, hash)
    alt valid credentials
        A->>A: token = secrets.token_urlsafe(32)
        A->>R: SET session:{token} = admin.id  (EX 3600)
        A-->>C: 200 { token }
    else invalid
        A-->>C: 401 Wrong In email or password
    end

    Note over C,R: Every protected request sends the token

    C->>A: POST /edit/item { token, ... }
    A->>R: GET session:{token}
    alt exists
        A->>D: UPDATE menu
        A-->>C: { ok: true }
    else missing / expired
        A-->>C: 401 Token invalid or expired
    end
```

> [!NOTE]
> **Why Redis for sessions?** Sessions are short-lived key/value data, which is exactly what Redis is built for. `EX 3600` makes each session **self-destruct after an hour**, and the API stays stateless.

<img src="assets/divider.svg" width="100%" alt=""/>

## 📡 API Reference

Base URL: `https://menu-backend-grr7.onrender.com`

| Method | Endpoint | Auth | Description |
|:------:|----------|:----:|-------------|
| `GET` | `/health` | 🌍 | Liveness probe → `{"status": "ok"}` |
| `GET` | `/` | 🌍 | List all menu items |
| `GET` | `/edit/get` | 🌍 | List all items (admin view) |
| `POST` | `/edit/login` | 🌍 | Exchange credentials for a session token |
| `POST` | `/edit/item` | 🔒 | Update an item |
| `POST` | `/edit/delete` | 🔒 | Delete an item |
| `POST` | `/edit/add` | 🔒 | Create an item |

> 🌍 public · 🔒 requires a valid `token` in the request body

<details>
<summary><b>📥 GET /</b>: list the menu</summary>

<br/>

```bash
curl https://menu-backend-grr7.onrender.com/
```

```json
[
  { "id": 1, "name": "Cappuccino", "price": 112.0, "category": "hot" },
  { "id": 9, "name": "Iced Latte", "price": 112.0, "category": "cold" },
  { "id": 13, "name": "Carrot Cake", "price": 130.0, "category": "cake" }
]
```
</details>

<details>
<summary><b>🔑 POST /edit/login</b>: get a session token</summary>

<br/>

```bash
curl -X POST $API/edit/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "••••••••"}'
```

**200**
```json
{ "token": "k3J...secure-random-string" }
```
**401**
```json
{ "detail": "Wrong In email or password" }
```
</details>

<details>
<summary><b>➕ POST /edit/add</b>: create an item</summary>

<br/>

```bash
curl -X POST $API/edit/add \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN>", "name": "Mocha", "price": 120, "category": "hot"}'
```
```json
{ "ok": true }
```
</details>

<details>
<summary><b>✏️ POST /edit/item</b>: update an item</summary>

<br/>

```bash
curl -X POST $API/edit/item \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN>", "id": 1, "name": "Cappuccino", "price": 115, "category": "hot"}'
```
```json
{ "ok": true }
```
</details>

<details>
<summary><b>🗑️ POST /edit/delete</b>: remove an item</summary>

<br/>

```bash
curl -X POST $API/edit/delete \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN>", "id": 1}'
```
```json
{ "ok": true }
```
`404` is returned if the item doesn't exist.
</details>

<img src="assets/divider.svg" width="100%" alt=""/>

## 🗄️ Data Model

```mermaid
erDiagram
    MENU {
        int    id PK
        string name "unique, not null"
        string category "hot | cold | cake | custom"
        float  price "not null"
    }
    ADMIN {
        int    id PK
        string email "unique, not null"
        string password "bcrypt hash"
    }
```

Tables are created automatically on startup. Set `SEED_MENU=1` to seed the default 16-item menu, and `ADMIN_EMAIL` + `ADMIN_PASSWORD` to auto-create the admin account (stored as a bcrypt hash).

<img src="assets/divider.svg" width="100%" alt=""/>

## 🛡️ Security

<table>
  <tr>
    <td align="center" width="33%"><h3>🔑</h3><b>bcrypt hashing</b><br/><sub>via <code>passlib</code>, never plain text</sub></td>
    <td align="center" width="33%"><h3>🎲</h3><b>Random tokens</b><br/><sub><code>secrets.token_urlsafe(32)</code></sub></td>
    <td align="center" width="33%"><h3>⏳</h3><b>Auto-expiry</b><br/><sub>Redis TTL of 3600 s</sub></td>
  </tr>
  <tr>
    <td align="center"><h3>🌐</h3><b>Strict CORS</b><br/><sub>only the <code>FRONTEND_URL</code> origin</sub></td>
    <td align="center"><h3>🤐</h3><b>Secrets in env</b><br/><sub>no credentials in the code</sub></td>
    <td align="center"><h3>🔌</h3><b>Resilient DB link</b><br/><sub><code>pool_pre_ping</code> for serverless Postgres</sub></td>
  </tr>
</table>

<img src="assets/divider.svg" width="100%" alt=""/>

## 🔧 Environment Variables

| Variable | Required | Description | Example |
|----------|:--------:|-------------|---------|
| `DATABASE_URL` | prod | PostgreSQL URL (`postgres://` is auto-fixed). Falls back to local SQLite | `postgresql://user:pass@host/db` |
| `REDIS_URL` | ✅ | Redis connection string | `redis://localhost:6379/0` |
| `FRONTEND_URL` | ✅ | Allowed CORS origin | `https://menu-backend-fagr.vercel.app` |
| `ADMIN_EMAIL` | first run | Creates the admin if missing | `admin@layali.com` |
| `ADMIN_PASSWORD` | first run | Admin password (hashed on save) | `••••••••` |
| `SEED_MENU` | optional | `1` seeds the default menu when the table is empty | `1` |

<img src="assets/divider.svg" width="100%" alt=""/>

## 🚀 Run Locally

```bash
# 1. Clone
git clone https://github.com/Omar404X0/Menu-Backend.git
cd Menu-Backend

# 2. Virtual env
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Configure (Redis must be running, see the Docker section)
export REDIS_URL=redis://localhost:6379/0
export FRONTEND_URL=http://localhost:3000
export ADMIN_EMAIL=admin@layali.com
export ADMIN_PASSWORD=change-me
export SEED_MENU=1

# 5. Run
uvicorn main:app --reload
```

API → **http://localhost:8000** · Swagger → **http://localhost:8000/docs**

<img src="assets/divider.svg" width="100%" alt=""/>

## 🐳 Docker

```bash
# Redis only
docker run -d --name layali-redis -p 6379:6379 redis:7-alpine

# Build and run the API
docker build -t layali-api .
docker run -d -p 8000:8000 --env-file .env --name layali-api layali-api
```

<details>
<summary><b>🧩 docker-compose.yml (API + Redis)</b></summary>

<br/>

```yaml
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    environment:
      REDIS_URL: redis://redis:6379/0
    depends_on: [redis]
```

```bash
docker compose up --build
```
</details>

<img src="assets/divider.svg" width="100%" alt=""/>

## 🧪 Testing

```bash
pip install pytest httpx
pytest -v
```

What the suite covers:

- [x] `GET /health` returns `{"status": "ok"}`
- [x] `GET /` returns the list of items
- [x] Login with wrong credentials → `401`
- [x] Login with correct credentials → returns a `token`
- [x] Protected routes without a valid token → `401`
- [x] Add → Edit → Delete full lifecycle

<img src="assets/divider.svg" width="100%" alt=""/>

## 🧠 What I Learned

| | Tool | What I practised |
|---|------|------------------|
| 🔴 | **Redis** | Session storage with TTL-based expiry |
| 🐳 | **Docker** | Reproducible environments |
| 🧪 | **pytest** | Testing the API endpoints |
| 🔐 | **bcrypt + tokens** | Password hashing and token auth |
| 🌩️ | **Cloud** | Render · Neon · Vercel |

<img src="assets/divider.svg" width="100%" alt=""/>

## 🗺️ Roadmap

- [x] Public menu endpoint
- [x] bcrypt login + Redis sessions
- [x] Authenticated add / edit / delete
- [x] Docker image and pytest suite
- [ ] Send the token via an `Authorization: Bearer` header
- [ ] Protect `GET /edit/get` (or remove the duplicate route)
- [ ] Return `404` in `/edit/item` when the id doesn't exist
- [ ] Rate-limit `/edit/login`
- [ ] Logout endpoint (delete the Redis key)
- [ ] Alembic migrations
- [ ] GitHub Actions CI (pytest + Docker build)

<img src="assets/divider.svg" width="100%" alt=""/>

<div align="center">

### Enjoyed it? Drop a ⭐ and check the [frontend repo](https://github.com/Omar404X0/Menu-Frontend)

Made with ☕ and 🐍 by **[Omar Elmallah](https://github.com/Omar404X0)**

<img src="assets/divider.svg" width="100%" alt=""/>

</div>
