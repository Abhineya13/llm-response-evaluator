from evaluator import keyword_coverage, valid_json, evaluate_case


def test_keyword_coverage_all_present():
    response = "Python is useful for machine learning and data analysis."
    keywords = ["Python", "data"]

    assert keyword_coverage(response, keywords) == 1.0


def test_keyword_coverage_missing_keyword():
    response = "Python is a programming language."
    keywords = ["Python", "machine learning"]

    assert keyword_coverage(response, keywords) == 0.5


def test_valid_json():
    assert valid_json('{"language": "Python"}') is True


def test_invalid_json():
    assert valid_json("This is not JSON") is False


def test_case_failure():
    case = {
        "name": "Failure test",
        "response": "Python is useful.",
        "required_keywords": ["Python", "algorithms"]
    }

    result = evaluate_case(case)

    assert result["passed"] is False