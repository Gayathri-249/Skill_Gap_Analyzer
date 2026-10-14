import json
import logging
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None


def create_fallback_plan(missing_skills, target_role, weeks):
    """Create a roadmap locally when Gemini is unavailable."""

    skills = list(dict.fromkeys(missing_skills or []))
    weeks = max(1, int(weeks))

    learning_plan = []

    for index in range(weeks):
        start = index * len(skills) // weeks
        end = (index + 1) * len(skills) // weeks
        weekly_skills = skills[start:end]

        if not weekly_skills:
            weekly_skills = skills[-1:] if skills else ["Practice and revision"]

        focus = ", ".join(weekly_skills)

        learning_plan.append({
            "week": index + 1,
            "focus": focus,
            "skills": weekly_skills,
            "activities": [
                f"Study the fundamentals of {skill}."
                for skill in weekly_skills
            ] + [
                "Write small practice exercises and review your progress."
            ],
            "project": (
                f"Build a small {weekly_skills[0]} practice project "
                f"related to {target_role}."
            ),
            "outcome": (
                f"Understand the basics of {focus} and apply them "
                "in a practical exercise."
            ),
        })

    return {
        "summary": (
            f"Your {weeks}-week learning roadmap for {target_role} "
            "is ready. Gemini was unavailable, so this plan was created "
            "using your detected skill gaps."
        ),
        "learning_plan": learning_plan,
    }


def generate_learning_plan(
    missing_skills,
    target_role="AI Engineer",
    current_skills=None,
    weeks=4,
):
    """Generate a personalized roadmap, with a local fallback."""

    missing_skills = list(dict.fromkeys(missing_skills or []))
    current_skills = current_skills or []
    weeks = max(1, int(weeks))

    if not missing_skills:
        return {
            "summary": (
                "No skill gaps were detected by the current keyword matcher. "
                "Consider practicing your existing skills with a project."
            ),
            "learning_plan": [],
        }

    if client is None:
        logging.warning("GEMINI_API_KEY is not configured.")
        return create_fallback_plan(missing_skills, target_role, weeks)

    prompt = f"""
You are a career learning assistant.

Create a practical {weeks}-week learning plan for the role: {target_role}.

Current detected skills:
{json.dumps(current_skills)}

Missing skills:
{json.dumps(missing_skills)}

Return ONLY valid JSON with this structure:
{{
  "summary": "Short explanation of the learning priorities",
  "learning_plan": [
    {{
      "week": 1,
      "focus": "Learning topic",
      "skills": ["skill 1"],
      "activities": ["activity 1", "activity 2"],
      "project": "A small practical project",
      "outcome": "What the learner should be able to do"
    }}
  ]
}}

Requirements:
- Create exactly {weeks} weekly entries.
- Prioritize foundational skills before advanced skills.
- Include hands-on practice and a small project.
- Use beginner-friendly language.
- Focus on the supplied missing skills and relevant foundations.
- Do not claim proficiency merely because a skill appears in a resume.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        data = json.loads(response.text)
        plan = data.get("learning_plan")

        if not isinstance(plan, list) or len(plan) != weeks:
            raise ValueError("Gemini returned an invalid weekly plan.")

        for entry in plan:
            if not isinstance(entry, dict):
                raise ValueError("Invalid weekly plan entry.")

            for field in (
                "week", "focus", "skills", "activities", "project", "outcome"
            ):
                if field not in entry:
                    raise ValueError(f"Missing field in plan: {field}")

        if not isinstance(data.get("summary"), str):
            raise ValueError("Gemini returned no summary.")

        logging.info("Gemini learning roadmap generated successfully.")
        return data

    except Exception:
        logging.exception(
            "Gemini unavailable; generating a local fallback roadmap."
        )
        return create_fallback_plan(missing_skills, target_role, weeks)