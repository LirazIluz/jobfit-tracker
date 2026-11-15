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


def test_c_is_not_found_inside_words():
    result = find_skills("We build computer science projects")
    assert "c" not in result


def test_c_is_found_as_a_word():
    result = find_skills("Knowledge in C/C++ and Python")
    assert "c" in result


def test_fit_score_never_above_100():
    assert fit_score(["c"]) == 100


def test_location_not_found_inside_words():
    assert find_location("We support our customers worldwide") == ""


def test_job_type_not_found_inside_words():
    assert find_job_type("Work with internal teams") == ""