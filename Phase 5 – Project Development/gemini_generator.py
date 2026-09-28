import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-1.5-pro")


def _client():
    if not API_KEY:
        return None
    try:
        from google import genai
        return genai.Client(api_key=API_KEY)
    except Exception:
        return None


def _fallback(user_input: dict) -> str:
    goal = user_input["goal"]
    intensity = user_input["intensity"]
    name = user_input["username"]
    return f"""FitBuddy Demo 7-Day Workout Plan for {name}\n\nGoal: {goal}\nIntensity: {intensity}\n\nDay 1 - Full Body\nWarm-up: 5-10 minutes.\nMain workout: Squats 2 x 10, incline push-ups 2 x 8, glute bridges 2 x 10.\nCool-down: Gentle stretching.\n\nDay 2 - Cardio\nWarm-up: 5 minutes.\nMain workout: 20 minutes of comfortable walking or similar low-impact cardio.\nCool-down: 5 minutes easy walking and stretching.\n\nDay 3 - Lower Body\nWarm-up: 5-10 minutes.\nMain workout: Squats 2 x 10, reverse lunges 2 x 6 each side, calf raises 2 x 12.\nCool-down: Gentle stretching.\n\nDay 4 - Recovery\nEasy walking, mobility, breathing and light stretching.\n\nDay 5 - Upper Body\nWarm-up: 5-10 minutes.\nMain workout: Incline push-ups 2 x 8, light rows 2 x 10, shoulder mobility.\nCool-down: Gentle stretching.\n\nDay 6 - Full Body\nRepeat comfortable exercises from earlier days at an easy-to-moderate effort.\n\nDay 7 - Rest and Recovery\nRest, gentle mobility and normal daily activity.\n\nSafety note: General fitness information only. Stop if you feel pain, dizziness, chest discomfort or unusual shortness of breath and seek appropriate professional advice."""


def generate_workout_gemini(user_input: dict) -> str:
    prompt = f"""You are FitBuddy, an AI fitness planning assistant.\nCreate a personalized, beginner-friendly 7-day workout plan.\n\nUser: {user_input['username']}\nAge: {user_input['age']}\nWeight: {user_input['weight']} kg\nGoal: {user_input['goal']}\nIntensity: {user_input['intensity']}\n\nFor every day include focus, warm-up, main workout with exercises and sets/repetitions or duration, rest guidance, and cool-down/recovery. Include at least one recovery/rest day. Do not diagnose medical conditions or prescribe treatment."""
    client = _client()
    if client is None:
        return _fallback(user_input)
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return (getattr(response, "text", None) or _fallback(user_input)).strip()
    except Exception:
        return _fallback(user_input)
