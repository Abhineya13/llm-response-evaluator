import json
from pathlib import Path


def keyword_coverage(response: str, required_keywords: list[str]) -> float:
    """Calculate the proportion of required keywords found in a response."""
    if not required_keywords:
        return 1.0

    response = response.lower()

    matches = sum(
        keyword.lower() in response
        for keyword in required_keywords
    )

    return matches / len(required_keywords)


def valid_json(response: str) -> bool:
    """Check whether a response contains valid JSON."""
    try:
        json.loads(response)
        return True
    except json.JSONDecodeError:
        return False


def evaluate_case(case: dict) -> dict:
    """Evaluate one LLM response against its expected criteria."""
    response = case["response"]
    required_keywords = case.get("required_keywords", [])

    coverage = keyword_coverage(response, required_keywords)

    result = {
        "name": case["name"],
        "keyword_coverage": round(coverage, 2),
        "passed": coverage == 1.0,
    }

    if case.get("expect_json", False):
        json_passed = valid_json(response)
        result["valid_json"] = json_passed
        result["passed"] = result["passed"] and json_passed

    return result


def evaluate_dataset(cases: list[dict]) -> dict:
    """Evaluate multiple responses and generate an aggregate report."""
    results = [evaluate_case(case) for case in cases]

    passed = sum(result["passed"] for result in results)
    total = len(results)

    return {
        "total_cases": total,
        "passed_cases": passed,
        "pass_rate": round(passed / total, 2) if total else 0,
        "results": results,
    }


def load_cases(filename: str) -> list[dict]:
    """Load evaluation cases from a JSON file."""
    path = Path(filename)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    cases = load_cases("test_cases.json")
    report = evaluate_dataset(cases)

    print(json.dumps(report, indent=2))