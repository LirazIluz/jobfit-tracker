import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from .analyzer import MY_SKILLS

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

MY_BACKGROUND = """Coursework: Data Structures, Algorithm Design, Operating Systems and
System Programming, Computer Architecture, Digital Systems, Principles of Programming Languages.
Projects: a Linux shell and ELF tools in C, a multi-threaded STOMP client-server
(Java, C++, Python) over TCP/IP, and a Django REST web app that integrates the Google Gemini LLM API with
prompt engineering, with pytest tests, Docker and CI with GitHub Actions."""

PROMPT = """You are helping a Computer Science student decide whether a job posting fits her.

Her skills: {my_skills}
Her background: {background}

Read the job posting below and return ONLY a JSON object with these keys:
- "location": the city of the job, or "" if not mentioned
- "job_type": one of "STUDENT", "INTERNSHIP", "PART_TIME", "FULL_TIME", or ""
- "required_skills": list of CONCRETE technical skills (short, lowercase),
  for example "python", "rest apis", "llm integration".
  Do NOT include vague words like "coding", "ai" or "technical".
  Do NOT include degrees, years of study, years of experience or availability.
  If the posting has no formal requirements, take the skills from the
  responsibilities ("What you'll do").
  If the posting lists alternatives (for example "Java, C++, or C#"),
  put them together as ONE item: "java / c++ / c#".
  Include required CS fundamentals too (for example "data structures", "algorithms",
  "operating systems").
- "nice_to_have": concrete technical skills marked as an advantage / nice to have
  (same rules as required_skills)
- "skills_missing": items from required_skills that she does NOT have.
  An item with alternatives is missing ONLY if she has NONE of them.
  Example: she has java, so "java / c++ / c#" is NOT missing.
  Treat related skills as the same skill. Examples: git = version control,
  pytest/junit = automated testing, oop = object-oriented programming.
- "nice_missing": items from nice_to_have that she does NOT have (same rules as skills_missing)
- Be STRICT when deciding what she has: a skill counts ONLY if it appears
  in her skills or background. Do not assume skills from related experience
  (for example, using an LLM API does NOT mean she built AI agents).
- "fit_score": a number 0-100, how well she fits the REQUIRED skills
- "summary": 1-2 sentences about the role and the fit. Mention ONLY experience
  that appears in her skills or background. Never invent experience.

Job posting:
{posting}
"""

VAGUE_WORDS = {"ai", "coding", "programming", "technical", "software", "code","professional development", "experience"}


def clean_skills(skills):
    """Remove vague words that are not real technical skills."""
    return [s for s in skills if s.strip().lower() not in VAGUE_WORDS]


def percent_have(skills, missing):
    """Return the percent (0-100) of skills that are not in missing."""
    have = len(skills) - len(missing)
    return round(have / len(skills) * 100)


def analyze_with_ai(text):
    client = genai.Client(http_options=types.HttpOptions(timeout=30000))
    prompt = PROMPT.format(
        my_skills=", ".join(MY_SKILLS),
        background=MY_BACKGROUND,
        posting=text,
    )
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0,
                ),
            )
            break
        except errors.ServerError:
            if attempt == 2:
                raise
            time.sleep(2)

    result = json.loads(response.text)
    for key in ["required_skills", "skills_missing", "nice_to_have", "nice_missing"]:
        result[key] = clean_skills(result.get(key, []))

    # Compute the score in code, so it always matches the tags on the screen.
    if result["required_skills"]:
        result["fit_score"] = percent_have(result["required_skills"], result["skills_missing"])
    elif result["nice_to_have"]:
        result["fit_score"] = percent_have(result["nice_to_have"], result["nice_missing"])
    return result