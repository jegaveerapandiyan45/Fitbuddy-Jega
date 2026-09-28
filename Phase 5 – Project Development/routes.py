from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from .database import save_user, save_plan, get_user, get_all_users, update_plan, delete_user

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

def _view(request, user, plan, tip, message=None):
    return templates.TemplateResponse("result.html", {"request": request, "user": user, "workout_plan": plan, "nutrition_tip": tip, "message": message})

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": None})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request, username: str = Form(...), user_id: str = Form(...), age: int = Form(...), weight: float = Form(...), goal: str = Form(...), intensity: str = Form(...)):
    if get_user(user_id):
        return templates.TemplateResponse("index.html", {"request": request, "error": "User ID already exists. Please use another User ID."})
    data = UserInput(user_id=user_id, username=username, age=age, weight=weight, goal=goal, intensity=intensity)
    plan = generate_workout_gemini(data.model_dump())
    tip = generate_nutrition_tip_with_flash(goal)
    save_user(user_id, username, age, weight, goal, intensity)
    save_plan(user_id, plan, tip)
    return _view(request, get_user(user_id), plan, tip)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    user = get_user(user_id)
    if not user:
        return templates.TemplateResponse("index.html", {"request": request, "error": "User ID not found."})
    data = FeedbackRequest(user_id=user_id, feedback=feedback)
    revised = update_workout_plan(user.original_plan, data.feedback)
    update_plan(user_id, revised, data.feedback)
    updated = get_user(user_id)
    return _view(request, updated, revised, updated.nutrition_tip, "Your plan has been updated based on your feedback!")

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    return templates.TemplateResponse("all_users.html", {"request": request, "users": get_all_users()})

@router.post("/delete-user/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)

@router.get("/health")
def health():
    return {"status": "ok", "application": "FitBuddy"}
