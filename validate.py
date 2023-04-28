import requests
import json
import argparse

"""
https://www.offenesdatenportal.de/api/3/action/package_search?fq=organization:moers
"""


VALIDATION_API_URL = "https://www.itb.ec.europa.eu/shacl/dcat-ap.de/api/validate"


def severity_key(severity):
    if severity == "sh:Warning":
        return "warning"
    elif severity == "sh:Violation":
        return "error"
    elif severity == "sh:Info":
        return "info"


def get_package_list(url):
    api_path = "api/3/action/package_list"
    full_url = url + api_path

    response = requests.get(full_url)

    if response.status_code == 200:
        data = json.loads(response.content)
        result = data["result"]
        return result
    else:
        print(f"Error fetching data from {full_url}. Status code: {response.status_code}")


def generate_validation_url(url, package_name):
    return f"{url}dcatapde/dataset/{package_name}.xml"  # DKAN
    return f"{url}dataset/{package_name}.rdf"  # CKAN


def package_url(url, package_name):
    return f"{url}dataset/{package_name}"


def extract_validation_results(json_ld):
    result = { "valid": False, "results": [] , "warnings": 0, "errors": 0, "info": 0}

    for graph_item in json_ld.get("@graph", []):
        result_type =graph_item.get("@type", "")
        if result_type == "sh:ValidationReport":
            result["valid"] = graph_item["sh:conforms"]
        if result_type == "sh:ValidationResult":
            result_message = graph_item["resultMessage"]["@value"]
            result_path = graph_item["resultPath"]
            severity = graph_item["resultSeverity"]
            result[severity_key(severity)] += 1
            result["results"].append({"message": result_message, "path": result_path, "type": severity})

    return result


def validate_package(url):
    payload = {
        "contentToValidate": url,
        "validationType": "v20_de_spec_implr"
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "application/ld+json"
    }

    response = requests.post(VALIDATION_API_URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content)

        validation_results = extract_validation_results(data)

        if validation_results["valid"]:
            print(f"Package validated successfully: {url}")
        else:
            print(f"Validation failed for package {url}:")
            """
            for result in validation_results:
                print(f"- {result['message']} ({result['path']})")
            """
    else:
        print(f"Error validating package at {url}. Status code: {response.status_code}")

    return validation_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate packages from CKAN instance")
    parser.add_argument("url", type=str, help="URL of CKAN instance")
    args = parser.parse_args()

    package_list = get_package_list(args.url)
    results = []

    for package_name in package_list:
        validation_url = generate_validation_url(args.url, package_name)
        result = validate_package(validation_url)
        # count errors and warnings, successes
        results.append({"package": package_name, "url": package_url(args.url, package_name), "result": result})

    with open("validation.json", "w") as f:
        json.dump(results, f)
