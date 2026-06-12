# qaforge

Complete QA automation framework for an e-commerce application covering cart, order, and payment domains.

**54 tests — all green.**

## Live Allure report

[**View the Allure test report →**](https://guykopa.github.io/qaforge/allure-report/)

Generated automatically on every push to `main`.

---

## Stack

| Layer | Tool | Tests |
|-------|------|-------|
| Unit | pytest | 19 |
| API | pytest + httpx | 16 |
| E2E Selenium | selenium + Docker | 8 |
| E2E Cypress | cypress + Docker | 5 |
| Non-regression | pytest | 6 |
| App under test | FastAPI + Jinja2 | — |
| CI/CD | GitHub Actions | — |
| Test reporting | Allure | — |

## Test pyramid

```
        ▲
       /|\
      / | \     NON-REGRESSION (6)
     /──|──\
    /   |   \   E2E Selenium + Cypress (13)
   /────|────\
  /     |     \ API (16)
 /──────|──────\
/       |       \ UNIT (19)
/────────|────────\
```

---

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
.venv/bin/uvicorn app.main:app --reload
# API docs  : http://localhost:8000/docs
# Products  : http://localhost:8000/products
```

## Run tests

```bash
# Unit
.venv/bin/pytest tests/unit/ -v

# API
.venv/bin/pytest tests/api/ -v

# Non-regression
.venv/bin/pytest tests/non_regression/ -v

# All Python tests with coverage
.venv/bin/pytest tests/unit/ tests/api/ tests/non_regression/ \
  --cov=app --cov-fail-under=90

# All tests + Allure results
.venv/bin/pytest tests/unit/ tests/api/ tests/non_regression/ \
  --alluredir=allure-results
```

## E2E Selenium — via Docker

Selenium tests use a standalone Chrome container.
The browser is visible live via noVNC.

```bash
# 1. Start app + Selenium container
docker compose -f docker/docker-compose.yml up app selenium-chrome -d

# 2. Watch live
#    Open http://localhost:7900  (password: secret)

# 3. Run the tests
.venv/bin/pytest tests/e2e/ -v
```

`.env` configuration (loaded automatically):
```env
SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
APP_BASE_URL=http://docker-app-1:8000
```

## E2E Cypress — via Docker

```bash
docker compose -f docker/docker-compose.yml run --rm cypress
```

## Allure report — local

```bash
# Generate + open
npx allure-commandline generate allure-results -o allure-report --clean
npx allure-commandline open allure-report
```

## CI/CD

The GitHub Actions pipeline runs automatically on every push:

| Job | What it does |
|-----|-------------|
| `unit-and-api` | lint + unit + API + non-regression + coverage ≥ 90% |
| `e2e-selenium` | Selenium E2E tests (depends on unit-and-api) |
| `e2e-cypress` | Cypress E2E tests (depends on unit-and-api) |
| `allure-report` | merges all results → Allure report → GitHub Pages (main only) |

---

## Demo guide

**Suggested flow for a recruiter demo (15–20 min)**

1. **Test pyramid** — open `README.md`, explain the 4 levels and why each exists
2. **Live run** — `pytest tests/unit/ tests/api/ -v` → all green in seconds
3. **Test plan** — open `test_plans/US002_checkout_flow.md` → show User Story → test cases → automated test link
4. **Bug report** — open `bug_reports/BUG001_discount_rounding.md` → show severity, steps to reproduce, root cause
5. **CI/CD** — open GitHub Actions tab → last run, show the 4 jobs
6. **Allure report** — open [live report](https://guykopa.github.io/qaforge/allure-report/) → suites, timeline, behaviors
7. **E2E live** (optional, requires Docker) — `docker compose up app selenium-chrome -d` → open noVNC at `http://localhost:7900` → `pytest tests/e2e/ -v` → watch the browser

---

## Project structure

```
qaforge/
├── app/
│   ├── domain/             ← Cart, Order, Payment (business logic)
│   ├── templates/          ← Frontend HTML (Jinja2)
│   └── main.py             ← API endpoints + HTML routes
├── tests/
│   ├── conftest.py         ← All pytest fixtures
│   ├── unit/               ← 19 unit tests
│   ├── api/                ← 16 API tests
│   ├── e2e/                ← 8 Selenium tests + Page Object Model
│   └── non_regression/     ← 6 critical path tests
├── cypress/                ← 5 Cypress tests (JavaScript)
├── test_plans/             ← US001, US002, US003
├── bug_reports/            ← BUG001, BUG002
├── docker/                 ← docker-compose.yml + Dockerfile
├── .github/workflows/      ← ci.yml (4 jobs)
├── .env                    ← E2E config (gitignored)
├── requirements.txt
└── package.json
```

## Coverage

Unit + API: **≥ 90%** on `app/` (current: ~93%).
