# ---------- Data ----------

CITIES = [
    "Haifa", "Yokneam", "Tel Aviv", "Beer Sheva", "Jerusalem", "Herzliya",
    "Ramat Gan", "Petah Tikva", "Omer", "Kfar Saba", "Caesarea", "Netanya",
    "Ra'anana", "Rehovot", "Ramat HaSharon",
]

# Order matters: the first type that matches wins
JOB_TYPE_KEYWORDS = {
    "STUDENT": ["student"],
    "INTERNSHIP": ["internship", "intern"],
    "PART_TIME": ["part time", "part-time"],
    "FULL_TIME": ["full time", "full-time"],
}

# Skills we look for in job postings
KNOWN_SKILLS = [
    "python", "c++", "java", "c#", "javascript", "typescript", "sql",
    "linux", "git", "docker", "bash", "networking", "tcp/ip",
    "multithreading", "oop", "rest", "django", "react", "verilog",
    "kubernetes", "aws", "machine learning", "embedded", "jenkins", "cmake",
]

# Skills I have
MY_SKILLS = [
    "python", "c++", "java", "typescript", "sql", "linux", "git", "docker",
    "bash", "networking", "tcp/ip", "multithreading", "oop", "rest", "django",
]


def find_location(text):
    """Return the first city from CITIES that appears in the text, or ""."""
    text_lower = text.lower()
    for city in CITIES:
        if city.lower() in text_lower:
            return city
    return ""


def find_job_type(text):
    """Return the first job type whose keywords appear in the text, or ""."""
    text_lower = text.lower()
    for key, words in JOB_TYPE_KEYWORDS.items():  
        for word in words:
            if word in text_lower:
                return key
    return ""


def find_skills(text):
    """Return a list of all KNOWN_SKILLS that appear in the text."""
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found.append(skill)
    return found


def fit_score(skills_found):
    """Return the percent (0-100) of skills_found that are in MY_SKILLS."""
    if len(skills_found) == 0:
        return 0
    count = 0
    for skill in MY_SKILLS:
        if skill in skills_found:
            count += 1
    return round(count / len(skills_found) * 100)

# ---------- Quick manual test ----------

if __name__ == "__main__":
    sample = """
    Software Engineering Student - Yokneam, Part time.
    Developing Linux user-space applications in C++.
    Knowledge in Python / Bash - advantage. Experience with Git and Verilog.
    """
    skills = find_skills(sample)
    print("Location:", find_location(sample))
    print("Job type:", find_job_type(sample))
    print("Skills:  ", skills)
    print("Fit:     ", fit_score(skills), "%")