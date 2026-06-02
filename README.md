# GreekDesk

A full-stack options pricing platform built from scratch. The core pricing engine is written in C++ and exposed to a Python/FastAPI backend via pybind11. A React dashboard renders prices, Greeks, P&L heatmaps, and live volatility smiles.

![Dashboard - Greeks & Charts](screenshot1.png)
![Dashboard - P&L Heatmap & Volatility Smile](screenshot2.png)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  React Frontend  (Recharts + Plotly, dark OLED UI)  │
└────────────────────────┬────────────────────────────┘
                         │ HTTP (localhost:3000 → 8000)
┌────────────────────────▼────────────────────────────┐
│  FastAPI Backend  (Python)                          │
│  /price  /greeks  /greekgraphs  /pnl  /vol_smile   │
│  /quote  /implied_vol                               │
└──────────┬──────────────────────┬───────────────────┘
           │ pybind11             │ yfinance
┌──────────▼──────────┐  ┌───────▼──────────────────┐
│  C++ Pricing Engine │  │  PostgreSQL (SQLAlchemy)  │
│  Black-Scholes      │  │  pricing_history          │
│  Greeks (×5)        │  │  saved_positions          │
│  Newton-Raphson IV  │  └──────────────────────────┘
└─────────────────────┘
```

---

## Features

- **Options Pricing** — Black-Scholes for European calls and puts
- **Greeks** — Delta, Gamma, Vega, Theta, Rho computed analytically in C++
- **Implied Volatility** — Newton-Raphson solver; inverts the BS formula given a market price
- **Volatility Smile** — Fetches real options chain from yfinance, computes IV at each strike, plots IV vs K
- **P&L Heatmap** — P&L across a grid of spot prices × volatilities (Plotly heatmap)
- **Greeks Charts** — Each Greek plotted vs spot price over a range
- **Live Quote** — Auto-fills spot price (S) and historical volatility (σ) from ticker
- **Pricing History** — Every calculation logged to PostgreSQL

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Pricing engine | C++17, Black-Scholes, Newton-Raphson |
| Python bridge | pybind11 |
| Backend | FastAPI, SQLAlchemy, yfinance |
| Database | PostgreSQL |
| Frontend | React, Recharts, Plotly.js |
| Build | CMake, MinGW (Windows) |

---

## Project Structure

```
greekdesk/
├── engine/
│   ├── include/pricer.h       # C++ declarations
│   └── src/pricer.cpp         # Black-Scholes, Greeks, Newton-Raphson
├── backend/
│   ├── bindings.cpp           # pybind11 module definition
│   ├── main.py                # FastAPI app + all endpoints
│   ├── models.py              # SQLAlchemy ORM models
│   └── database.py            # DB engine + session factory
├── frontend/
│   └── src/
│       ├── App.js             # Main dashboard component
│       └── App.css            # Dark OLED design system
├── app/
│   └── main.cpp               # Standalone C++ test binary
└── CMakeLists.txt
```

---

## Local Setup

### Prerequisites

- Python 3.14
- Node.js 18+
- PostgreSQL
- CMake + MinGW (Windows) or GCC (Linux/Mac)
- pybind11

### 1. Build the C++ engine

```bash
cmake -S . -B build -G "MinGW Makefiles"
cmake --build build
copy build\greekdesk.cp314-win_amd64.pyd backend\
```

### 2. Configure the database

Create a `.env` file in the project root:

```
DB_PASSWORD=your_postgres_password
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE greekdesk;
```

Then create the tables:

```bash
cd backend
python -c "from database import Base, engine; from models import *; Base.metadata.create_all(engine)"
```

### 3. Run the backend

```bash
python -m uvicorn backend.main:app --reload
```

### 4. Run the frontend

```bash
cd frontend
npm install
npm start
```

The dashboard opens at `http://localhost:3000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/quote` | Fetch live spot price + historical vol for a ticker |
| POST | `/price` | Compute Black-Scholes option price |
| POST | `/greeks` | Compute all 5 Greeks |
| POST | `/greekgraphs` | Greeks vs spot over a range (for charts) |
| POST | `/pnl` | P&L grid across spot × volatility |
| POST | `/implied_vol` | Implied volatility from a single market price |
| POST | `/vol_smile` | IV at every strike for the nearest listed expiry |

---

## Notes

- American options raise a `NotImplementedError` — binomial tree implementation is planned (Phase 5)
- Volatility smile uses bid/ask midpoint for live pricing; filters strikes to ±30% of spot, removes contracts priced below intrinsic value, and drops IV readings outside [1%, 200%]
- The `.pyd` binary is platform-specific; recompilation is required on Linux/Mac
