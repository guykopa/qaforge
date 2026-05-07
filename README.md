# qaforge

Complete QA automation framework for an e-commerce application covering cart, order, and payment domains.

**54 tests — all green.**

## Stack

| Layer | Outil | Tests |
|-------|-------|-------|
| Unit | pytest | 19 |
| API | pytest + httpx | 16 |
| E2E Selenium | selenium + Docker | 8 |
| E2E Cypress | cypress + Docker | 5 |
| Non-regression | pytest | 6 |
| App under test | FastAPI + Jinja2 | — |
| CI/CD | GitHub Actions | — |

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
# Produits  : http://localhost:8000/products
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

# HTML report
.venv/bin/pytest tests/unit/ tests/api/ tests/non_regression/ \
  --html=reports/report.html --self-contained-html
```

## E2E Selenium — via Docker

Les tests Selenium utilisent un conteneur Chrome.
Le navigateur est visible en live via noVNC.

```bash
# 1. Démarrer app + conteneur Selenium
docker compose -f docker/docker-compose.yml up app selenium-chrome -d

# 2. Regarder en live
#    Ouvrir http://localhost:7900  (mot de passe : secret)

# 3. Lancer les tests
.venv/bin/pytest tests/e2e/ -v
```

Configuration dans `.env` (chargé automatiquement) :
```env
SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
APP_BASE_URL=http://docker-app-1:8000
```

## E2E Cypress — via Docker

```bash
docker compose -f docker/docker-compose.yml run --rm cypress
```

## CI/CD

Le pipeline GitHub Actions tourne automatiquement sur chaque push :
1. `unit-and-api` — lint + tests + coverage ≥ 90% + rapport HTML
2. `e2e-selenium` — tests Selenium (dépend de unit-and-api)
3. `e2e-cypress` — tests Cypress (dépend de unit-and-api)

## Project structure

```
qaforge/
├── app/
│   ├── domain/             ← Cart, Order, Payment (logique métier)
│   ├── templates/          ← Frontend HTML (Jinja2)
│   └── main.py             ← Endpoints API + routes HTML
├── tests/
│   ├── conftest.py         ← Toutes les fixtures pytest
│   ├── unit/               ← 19 tests unitaires
│   ├── api/                ← 16 tests API
│   ├── e2e/                ← 8 tests Selenium + Page Object Model
│   └── non_regression/     ← 6 tests chemins critiques
├── cypress/                ← 5 tests Cypress (JavaScript)
├── test_plans/             ← US001, US002, US003
├── bug_reports/            ← BUG001, BUG002
├── docker/                 ← docker-compose.yml + Dockerfile
├── .github/workflows/      ← ci.yml
├── .env                    ← Config E2E (gitignored)
├── requirements.txt
└── package.json
```

## Coverage

Unit + API : **≥ 90%** sur `app/` (actuel : ~93%).
