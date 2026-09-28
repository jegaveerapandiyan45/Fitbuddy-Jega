import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash")


def generate_nutrition_tip_with_flash(goal: str) -> str:
    fallback = ("Choose balanced meals with vegetables, a suitable protein source, whole grains "
                "and appropriate portions. Stay hydrated and remember that individual nutrition "
                "needs can vary.")
    if not API_KEY:
        return fallback
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        prompt = f"Give one concise practical nutrition or recovery tip for a fitness user whose goal is {goal}. Avoid medical treatment, extreme diets, or unsafe weight-loss advice."
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return (getattr(response, "text", None) or fallback).strip()
    except Exception:
        return fallback
