# Ethnic Calorie Tracker

A nutrition tracking app built to close a real gap in mainstream calorie trackers like MyFitnessPal: reliable support for ethnic and regional dishes that most nutrition databases don't cover well.

**Live app:** [ethnic-calorie-tracker.streamlit.app](https://ethnic-calorie-tracker.streamlit.app)

## Why this exists

Most calorie tracking apps are built around Western, packaged, barcode-scannable foods. Home-cooked and regional dishes — kontomire stew, bibimbap, tagine, maqluba — are often missing entirely, or so poorly matched that the returned nutrition data is meaningless. This project treats that gap as the core problem to solve, not an edge case to ignore.

## How it works

**Search pipeline (in order):**
1. **Local SQLite cache** — checked first for instant, zero-latency lookups
2. **USDA FoodData Central API — generic foods** (`Foundation`, `SR Legacy` data types) — tried first for common/whole foods, since these categories are cleaner and less noisy than packaged-food data
3. **USDA FoodData Central API — branded foods** (`Branded` data type) — tried only if the generic search fails, catching common packaged foods (e.g. name-brand cookies) that don't exist in the generic categories
4. **Manual entry fallback** — if nothing is found anywhere (typically true for regional/home-cooked dishes with no API coverage), the user can input nutrition values directly, which are saved to the local database and instantly searchable from then on

Every result that comes from the API is cached locally under the exact term the user searched — not the API's own product name — so repeat searches for the same food never hit the API twice and stay consistent regardless of how a given API happens to label a product.

**Data integrity:** API responses are validated before being cached — entries with missing or zero calorie data (which USDA occasionally returns for sparse records) are rejected rather than silently logged, so bad data never pollutes the local database.

**Seed data:** the app ships with 25 hand-curated dishes across five cuisines (Ghanaian, Mexican, Palestinian, Korean, Moroccan) with real macro data, so common regional dishes work out of the box without needing an API call at all.

## Features

- Profile creation with TDEE calculation (Mifflin-St Jeor equation) and macro goal targets based on user-selected goal (cut / bulk / maintain / recomposition)
- Meal logging with automatic macro tracking against daily goals
- Meal recommendation engine that ranks available foods by how well they fit remaining daily macro targets
- Persistent local storage — profile and meal history persist across sessions via SQLite
- Manual food entry for dishes not covered by any data source

## Tech stack

- **Python** — core application logic
- **SQLite** — local persistent storage (food database, meal logs, user profile)
- **Streamlit** — web UI and deployment
- **USDA FoodData Central API** — external nutrition data source

## Known limitations

- Branded/packaged food coverage depends on USDA's `Branded` category, which is US-centric and won't have international packaged products
- Manual entries rely on user-provided accuracy — there's no verification step
- The recommendation engine currently ranks from the full food table rather than a personalized history

## Local setup

```bash
git clone https://github.com/Vexonics/Ethnic-Calorie-Tracker.git
cd Ethnic-Calorie-Tracker
pip install -r requirements.txt
streamlit run app.py
```

You'll need a free USDA FoodData Central API key ([sign up here](https://fdc.nal.usda.gov/api-key-signup/)) set in `src/api.py`.