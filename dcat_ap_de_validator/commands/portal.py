import json
from dcat_ap_de_validator.portals import Portal, CKAN, DKAN
from dcat_ap_de_validator.metadata.validate import validate


def execute(args):
    portal_type = str(args.portal_type)
    portal = Portal(args.url)
    if portal_type.lower() == "dkan":
        portal = DKAN(args.url)
    else:
        portal = CKAN(args.url)
    package_list = portal.packages()
    portal_title = portal.get_title()
    results = []

    for package_name in package_list:
        result = validate(portal.package_metadata_url(package_name))
        # count errors and warnings, successes
        results.append({"package": package_name, "url": portal.package_url(package_name), "result": result})

    with open(f"{portal_title}.json", "w") as f:
        json.dump(results, f)

    return results
