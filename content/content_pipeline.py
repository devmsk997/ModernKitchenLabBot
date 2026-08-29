from article_writer import generate_article
from seo_formatter import format_for_seo


def run_content_pipeline(topic, keyword):

    print("\n===== CONTENT PIPELINE START =====")


    # 1. Generate Article
    article = generate_article(
        topic,
        keyword
    )


    print("✓ Article Generated")


    # 2. SEO Optimization
    seo_data = format_for_seo(
        article["title"],
        keyword,
        article["content"]
    )


    print("✓ SEO Formatting Completed")


    final_post = {

        "title": article["title"],

        "meta_description":
            seo_data["meta_description"],

        "permalink":
            seo_data["permalink"],

        "labels":
            seo_data["label"],

        "image_alt":
            seo_data["image_alt"],

        "content":
            seo_data["optimized_content"]

    }


    return final_post



if __name__ == "__main__":


    result = run_content_pipeline(
        "Kitchen Organization",
        "best kitchen cabinet organizers"
    )


    print("\n====== FINAL BLOGGER POST ======")


    print("Title:")
    print(result["title"])


    print("\nMeta:")
    print(result["meta_description"])


    print("\nPermalink:")
    print(result["permalink"])


    print("\nLabels:")
    print(result["labels"])


    print("\nImage ALT:")
    print(result["image_alt"])


    print("\nContent Ready:")
    print("YES")