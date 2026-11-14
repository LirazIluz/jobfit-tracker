# JobFit Tracker

![Tests](https://github.com/LirazIluz/jobfit-tracker/actions/workflows/tests.yml/badge.svg)

A REST API for tracking job applications and analyzing job postings.

I built this project while searching for a student position: every day I received
several job postings and had to check the location, whether it's a student role,
which skills it requires, and whether I had already applied. JobFit Tracker
automates this.

## Features

- **Job application tracking** – full CRUD REST API (company, title, status, CV version, notes, etc.)
- **Duplicate detection** – prevents saving the same job twice (case-insensitive)
- **Job posting analyzer** – extracts location, job type and required skills from the posting text
- **Fit score** – calculates how many of the required skills I already have
- **Auto-fill** – when a job is saved with a description, location, job type and fit score are filled automatically
- **Automated tests** – 11 tests with pytest (analyzer + API)

## Tech Stack

Python · Django · Django REST Framework · SQLite · pytest · Git

## Example

`POST /api/analyze/`

```json
{"text": "Software Engineering Student - Yokneam, Part time. Linux, C++, Python, Git and Verilog."}
```

Response:

```json
{
  "location": "Yokneam",
  "job_type": "STUDENT",
  "skills_found": ["python", "c++", "linux", "git", "verilog"],
  "skills_missing": ["verilog"],
  "fit_score": 80
}
```

## Getting Started

```bash
git clone https://github.com/LirazIluz/jobfit-tracker.git
cd jobfit-tracker
python -m venv venv
venv\Scripts\activate        # on Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/api/jobs/

## Running Tests

```bash
pytest -v
```

## Interesting Problem: Skill Matching

Simple substring matching (`"git" in text`) produced false positives –
"git" was found inside "digital" and "rest" inside "interested".
I fixed it using regular expressions with lookarounds:

```python
pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
```

I used lookarounds instead of `\b` because `\b` doesn't work for skills
that end with non-word characters, such as `c++` and `c#`.

## Roadmap

- [ ] Web interface (HTML/CSS/JavaScript)
- [ ] Docker and GitHub Actions CI
- [ ] AI-based posting analysis (LLM)