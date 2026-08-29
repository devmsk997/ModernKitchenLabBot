def create_topic_cluster(main_topic):

    clusters = {

        "Kitchen Organization": [
            "Best Kitchen Cabinet Organizers",
            "Small Kitchen Storage Ideas",
            "Pantry Organization Ideas",
            "Spice Organization Ideas",
            "Under Sink Storage Ideas",
            "Kitchen Drawer Organizer Ideas",
            "Countertop Organization Ideas"
        ],


        "Kitchen Gadgets": [
            "Best Kitchen Gadgets",
            "Smart Kitchen Tools",
            "Must Have Cooking Tools",
            "Kitchen Gadgets For Small Spaces",
            "Useful Amazon Kitchen Products"
        ],


        "Home Storage": [
            "Bedroom Storage Ideas",
            "Bathroom Organization Ideas",
            "Closet Organization Ideas",
            "Small Apartment Storage Ideas"
        ]

    }


    if main_topic in clusters:

        return {
            "main_topic": main_topic,
            "cluster_articles": clusters[main_topic]
        }


    return {
        "main_topic": main_topic,
        "cluster_articles": []
    }



if __name__ == "__main__":


    result = create_topic_cluster(
        "Kitchen Organization"
    )


    print("\n====== TOPIC CLUSTER ======")

    print("Main Topic:")
    print(result["main_topic"])


    print("\nRelated Articles:")

    for article in result["cluster_articles"]:
        print("-", article)