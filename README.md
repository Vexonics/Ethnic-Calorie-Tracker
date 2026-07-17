# Ethnic Calorie Tracker

A nutrition tracking and meal recommendation platform built for people whose diets aren't represented in mainstream calorie apps.

## The Problem

Most calorie trackers are built around Western foods. If you eat jollof rice, fufu, kontomire stew, or maqluba, you're either manually entering everything from scratch or getting inaccurate results. This app fixes that.

## Features

- **Personalized TDEE Calculator** — calculates your daily calorie target based on weight, height, age, sex, activity level, and goal (bulk, cut, maintain, recomp)
- **Macro Goal Calculator** — generates personalized protein, carbs, fiber, fat, and sodium targets
- **Ethnic Food Database** — 26+ foods across Ghanaian, Mexican, Palestinian, Korean, and Moroccan cuisines
- **Meal Logging** — log meals with serving sizes and track macros in real time
- **Recommendation Engine** — suggests foods based on remaining daily macros and calorie budget
- **Progress Tracking** — see how much of each macro you've eaten and what you have left

## Tech Stack

- Python
- SQLite
- Streamlit (coming)
- FastAPI (coming)

## How to Run

1. Clone the repo
2. Run database setup:
python3 setup.py
3. Populate food database:
python3 data/seed_foods.py
4. Run the app:
python3 main.py

## Roadmap

- [ ] Streamlit web UI
- [ ] FastAPI backend
- [ ] AI-powered food lookup
- [ ] Photo-based food recognition
- [ ] Expanded ethnic food database (West African, Caribbean, South Asian)
- [ ] Deployment

## Why I Built This

I noticed that the foods I actually eat — Ghanaian dishes, foods from other underrepresented cuisines — weren't in any nutrition app I tried. So I built one that includes them.