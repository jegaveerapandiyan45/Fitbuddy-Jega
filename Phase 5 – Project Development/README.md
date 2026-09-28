# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a FastAPI-based web application that uses Google Gemini models to generate personalized 7-day workout plans and concise nutrition/recovery tips. Users can submit feedback to update an existing plan, while an admin page displays stored users and original/updated plans.

## Features
- User input: name, user ID, age, weight, goal and workout intensity
- Personalized 7-day workout plan
- Gemini workout generation module
- Gemini Flash nutrition/recovery tip module
- Feedback-based plan updating
- SQLite + SQLAlchemy persistence
- Jinja2 HTML frontend
- Admin view of users and plans
- Local demo fallback when a Gemini API key is not configured

## Project Structure
```text
FitBuddy/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── database.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── __init__.py
│   └── templates/
│       ├── index.html
│       ├── result.html
│       └── all_users.html
├── static/images/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run in VS Code (Windows)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

## Gemini API
The application runs in demo fallback mode without an API key. For live Gemini generation, copy `.env.example` to `.env` and add your own key. Never upload `.env` or API keys to GitHub.

## Main Routes
- `/` – Home/input page
- `/generate-workout` – Generate and save a plan
- `/submit-feedback` – Update a plan using feedback
- `/view-all-users` – Admin view
- `/docs` – FastAPI interactive documentation
- `/health` – Health check

## Source alignment
The module names and workflow follow the supplied FitBuddy project document: `routes.py`, `database.py`, `gemini_generator.py`, `gemini_flash_generator.py`, `updated_plan.py`, Jinja2 templates, SQLite/SQLAlchemy, and Gemini-based workout/nutrition/feedback functions.

> Note: This is a fitness-planning application and not a medical diagnosis or treatment system.
