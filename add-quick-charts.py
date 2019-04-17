"""Enable Quick Charts on HDX resources, following a template resource
"""

import config
import ckanapi, ckancrawler, logging, re, sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("add-quickcharts")
"""Python logging object"""

if len(sys.argv) != 4:
    print("Usage: python add-quick-charts.py <model> <pattern> <org>")
    sys.exit(2)
    
model = sys.argv[1]
pattern = sys.argv[2]
org = sys.argv[3]

# Connect to CKAN
crawler = ckancrawler.Crawler(
    ckan_url=config.CONFIG.get("ckanurl"),
    apikey=config.CONFIG.get("apikey")
)

# Look up the model view
package = crawler.ckan.action.package_show(id=model)
resource_id = package["resources"][0]["id"]
views = crawler.ckan.action.resource_view_list(id=resource_id)
qc_configuration = None
for view in views:
    # Find the Quick Charts view
    if view["view_type"] == "hdx_hxl_preview":
        qc_configuration = view["hxl_preview_config"]
        logger.info("Loaded Quick Charts configuration")
        break
if qc_configuration is None:
    print("Failed to find Quick Charts configuration for {}".format(model))
    sys.exit(-1)

# Crawl matching packages
for package in crawler.packages(fq="organization:{}".format(org)):

    # skip if it's the model package
    if package["name"] == model:
        logger.info("Skipping model %s", model)
        continue

    # skip if it doesn't match the pattern
    if not re.match(pattern, package["name"]):
        logger.info("Skipping non-matching package %s", package["name"])
        continue

    # update the package for preview
    logger.info("Updating package %s", package["name"])
    package["dataset_preview"] = "first_resource",
    package["has_quickcharts"] = True
    crawler.ckan.call_action("package_update", package)

    resource_id = package["resources"][0]["id"]
    views = crawler.ckan.action.resource_view_list(id=resource_id)
    found_view = False
    for view in views:
        # Find the Quick Charts view and set the configuration
        if view["view_type"] == "hdx_hxl_preview":
            view["hxl_preview_config"] = qc_configuration
            crawler.ckan.call_action("resource_view_update", view)
            found_view = True
            break

    # If we get to here, then we need to add the view
    if not found_view:
        logger.warn("Missing Quick Charts view for %s (creating)", package["name"])
        view = {
            "description": "",
            "title": "Quick Charts",
            "resource_id": resource_id,
            "view_type": "hdx_hxl_preview",
            "hxl_preview_config": qc_configuration
        }
        crawler.ckan.call_action("resource_view_create", view)
    
sys.exit(0)
