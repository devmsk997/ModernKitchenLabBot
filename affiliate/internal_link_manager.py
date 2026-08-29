def find_internal_links(topic, existing_posts):

    """
    Internal Link Manager

    Finds related old articles
    for SEO internal linking
    """


    suggestions = []


    topic_words = topic.lower().split()


    for post in existing_posts:

        post_lower = post.lower()


        match = False


        for word in topic_words:

            if word in post_lower:
                match = True


        if match:

            suggestions.append(
                {
                    "anchor_text": post,
                    "target_post": post
                }
            )


    return suggestions



if __name__ == "__main__":


    old_posts = [

        "Best Kitchen Cabinet Organizers",

        "Small Kitchen Storage Ideas",

        "Pantry Organization Ideas",

        "Spice Organization Ideas"

    ]


    links = find_internal_links(
        "Kitchen Organization",
        old_posts
    )


    print("\n====== INTERNAL LINKS ======")


    for link in links:

        print(
            "- Anchor:",
            link["anchor_text"]
        )