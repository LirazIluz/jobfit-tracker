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
- **Automated tests** – 13 tests with pytest (analyzer + API)
- **Web interface** – paste a job posting, see the fit analysis with colored skill tags, save it, and track all applications in a   table

## Tech Stack

Python · Django · Django REST Framework · SQLite · pytest · Git · Docker · GitHub Actions · HTML · CSS · JavaScript

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `/api/jobs/` | List all saved jobs / add a new job |
| GET, PUT, PATCH, DELETE | `/api/jobs/<id>/` | View, update or delete a job |
| POST | `/api/analyze/` | Analyze a job posting text |

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

To analyze a full job posting, open http://127.0.0.1:8000/api/analyze/
and paste the posting into the HTML form.

## Run with Docker

```bash
docker build -t jobfit-tracker .
docker run -p 8000:8000 jobfit-tracker
```

## Running Tests

```bash
pytest -v
```

## Interesting Problem: Skill Matching

Simple substring matching (`"git" in text`) produced false positives –
"git" was found inside "digital" and "rest" inside "interested".
I fixed it using regular expressions with lookarounds:

```python
pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9+#])"
```

I used lookarounds instead of `\b` because `\b` doesn't work for skills
that end with non-word characters, such as `c++` and `c#`.

Adding "c" as a skill revealed another bug: it was matched inside "c++".
The tests caught it, and I fixed it by also excluding "+" and "#" after a match.

## Roadmap

- [x] Web interface (HTML/CSS/JavaScript)
- [x] Docker and GitHub Actions CI
- [ ] AI-based posting analysis (LLM)