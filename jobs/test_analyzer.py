from jobs.analyzer import find_location, find_job_type, find_skills, fit_score


def test_find_location():
    assert find_location("Student position in Haifa") == "Haifa"

def test_empty_location():
    assert find_location("Student position,Develop AI-based solutions to analyze logs") == ""

def test_find_job_type():
    assert find_job_type("Student position in Haifa") == "STUDENT"

def test_find_skills1():
    assert find_skills("Strong programming skills in Python. Experience with Git. Basic command of C++ and Linux.") == ["python", "c++","linux", "git"]

def test_find_skills2():
    assert find_skills("We are interested in digital systems and loops") == []

def test_fit_score_empty():
    skills = find_skills("We are interested in digital systems and loops") 
    assert fit_score(skills) == 0

def test_fit_score():
    skills = find_skills("Strong programming skills in Python. Experience with verilog.") 
    assert fit_score(skills) == 50
