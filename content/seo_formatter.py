def format_for_seo(
    title,
    keyword,
    content
):

    """
    Modern Kitchen Lab
    SEO Formatter Engine

    Handles:
    - Meta description
    - Permalink
    - Labels
    - Keyword placement
    - Image SEO
    """


    seo_data = {

        "seo_title": title,

        "meta_description":
            f"Learn about {keyword}. "
            f"Discover useful tips, ideas and buying guidance "
            f"to improve your kitchen organization.",


        "permalink":
            keyword.lower()
            .replace(" ", "-"),


        "label":
            [
                "Kitchen Organization",
                "Storage Ideas",
                "Home Improvement"
            ],


        "focus_keyword":
            keyword,


        "image_alt":
            f"{keyword} ideas for modern kitchen organization",


        "internal_link_needed":
            True,


        "external_link_needed":
            True,


        "keyword_density_target":
            "1% - 2% natural usage",


        "optimized_content":
            content

    }


    return seo_data



if __name__ == "__main__":


    result = format_for_seo(
        "Best Kitchen Cabinet Organizers Guide",
        "best kitchen cabinet organizers",
        "Sample article content"
    )


    print("\n====== SEO REPORT ======")

    print("Title:")
    print(result["seo_title"])


    print("\nMeta Description:")
    print(result["meta_description"])


    print("\nPermalink:")
    print(result["permalink"])


    print("\nLabel:")
    print(result["label"])


    print("\nImage ALT:")
    print(result["image_alt"])