import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .analyzer import MY_SKILLS

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

MY_BACKGROUND = """Coursework: Data Structures, Algorithm Design, Operating Systems and
System Programming, Computer Architecture, Digital Systems, Principles of Programming Languages.
Projects: a Linux shell and ELF tools in C, a multi-threaded STOMP client-server
(Java, C++, Python) over TCP/IP, and a Django REST web app with pytest tests,
Docker and CI with GitHub Actions."""

PROMPT = """You are helping a Computer Science student decide whether a job posting fits her.

Her skills: {my_skills}
Her background: {background}

Read the job posting below and return ONLY a JSON object with these keys:
- "location": the city of the job, or "" if not mentioned
- "job_type": one of "STUDENT", "INTERNSHIP", "PART_TIME", "FULL_TIME", or ""
- "required_skills": list of required technical skills (short, lowercase).
  Do NOT include degrees, years of study or availability.
  If the posting lists alternatives (for example "Java, C++, or C#"),
  put them together as ONE item: "java / c++ / c#".
  Include required CS fundamentals too (for example "data structures", "algorithms",
  "operating systems").
- "nice_to_have": list of skills marked as an advantage / nice to have
- "skills_missing": items from required_skills that she does NOT have.
  An item with alternatives is missing ONLY if she has NONE of them.
  Example: she has java, so "java / c++ / c#" is NOT missing.
  Treat related skills as the same skill. Examples: git = version control,
  pytest/junit = automated testing, oop = object-oriented programming.
- "fit_score": a number 0-100, how well she fits the REQUIRED skills
- "summary": 1-2 sentences about the role and the fit

Job posting:
{posting}
"""


def analyze_with_ai(text):
    client = genai.Client(http_options=types.HttpOptions(timeout=30000))
    prompt = PROMPT.format(
        my_skills=", ".join(MY_SKILLS),
        background=MY_BACKGROUND,
        posting=text,
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,                                                      
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)                                                  