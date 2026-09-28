from .gemini_generator import _client, MODEL


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    fallback = original_plan + f"\n\nUpdated according to user feedback: {user_feedback}"
    client = _client()
    if client is None:
        return fallback
    prompt = f"""You are FitBuddy. Revise the following 7-day workout plan according to the user's feedback. Keep the 7-day structure and preserve useful parts unless the feedback asks for a change.\n\nORIGINAL PLAN:\n{original_plan}\n\nUSER FEEDBACK:\n{user_feedback}"""
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return (getattr(response, "text", None) or fallback).strip()
    except Exception:
        return fallback
