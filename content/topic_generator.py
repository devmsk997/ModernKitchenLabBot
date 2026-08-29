def find_new_topics(existing_posts, topic_cluster):

    """
    Modern Kitchen Lab
    Content Gap Finder

    Avoid duplicate topics
    Generate new article ideas
    """


    new_topics = []


    for topic in topic_cluster:

        already_exists = False


        for post in existing_posts:

            if topic.lower() in post.lower():
                already_exists = True
                break


        if not already_exists:
            new_topics.append(topic)


    return new_topics



if __name__ == "__main__":


    # Existing Blogger posts
    existing_posts = [
        "Meal Prep Organization Ideas to Save Time",
        "Best Lazy Susan Organization Ideas for Kitchen Cabinets",
        "Spice Storage Ideas"
    ]


    # From topic cluster engine
    kitchen_cluster = [
        "Best Kitchen Cabinet Organizers",
        "Small Kitchen Storage Ideas",
        "Pantry Organization Ideas",
        "Spice Organization Ideas",
        "Under Sink Storage Ideas",
        "Kitchen Drawer Organizer Ideas",
        "Countertop Organization Ideas"
    ]


    suggestions = find_new_topics(
        existing_posts,
        kitchen_cluster
    )


    print("\n====== NEW CONTENT IDEAS ======")


    for topic in suggestions:
        print("-", topic)