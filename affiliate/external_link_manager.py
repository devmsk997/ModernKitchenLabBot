def get_external_links(topic):

    """
    Trusted External Link Manager

    Future:
    - AI based source selection
    - Authority checking
    - Link freshness checking
    """


    authority_links = {


        "kitchen": [

            {
                "name": "USDA Food Safety",
                "url": "https://www.fsis.usda.gov"
            },

            {
                "name": "ENERGY STAR Home Products",
                "url": "https://www.energystar.gov"
            }

        ],


        "home": [

            {
                "name": "EPA Indoor Air Quality",
                "url": "https://www.epa.gov/indoor-air-quality-iaq"
            }

        ]

    }



    selected = []


    topic = topic.lower()


    if "kitchen" in topic:

        selected.extend(
            authority_links["kitchen"]
        )


    if "home" in topic:

        selected.extend(
            authority_links["home"]
        )


    return selected



if __name__ == "__main__":


    links = get_external_links(
        "Kitchen Organization"
    )


    print("\n====== EXTERNAL LINKS ======")


    for link in links:

        print(
            "-",
            link["name"],
            ":",
            link["url"]
        )