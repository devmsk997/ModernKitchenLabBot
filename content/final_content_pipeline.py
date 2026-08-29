import sys
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

sys.path.append(BASE_DIR)



from content.article_writer import generate_article
from content.seo_formatter import format_for_seo

from affiliate.external_link_manager import (
    get_external_links
)

from affiliate.internal_link_manager import (
    find_internal_links
)


from ai.gemini_image_creator import (
    generate_feature_image
)




def create_final_blog_post(topic, keyword):


    print("\n===== FINAL CONTENT PIPELINE =====")



    # Article

    article = generate_article(
        topic,
        keyword
    )


    print("✅ Article Generated")



    # SEO

    seo = format_for_seo(

        article["title"],

        keyword,

        article["content"]

    )


    print("✅ SEO Completed")



    # Internal Links


    old_posts = [

        "Best Kitchen Cabinet Organizers",

        "Small Kitchen Storage Ideas",

        "Pantry Organization Ideas",

        "Spice Organization Ideas",

        "Kitchen Drawer Organizer Ideas",

        "Countertop Organization Ideas"

    ]



    internal_links = find_internal_links(

        topic,

        old_posts

    )


    print("✅ Internal Links Added")



    # External Links


    external_links = get_external_links(

        topic

    )


    print("✅ External Links Added")



    # Gemini Image


    feature_image = generate_feature_image(

        topic,

        keyword

    )


    print("✅ Gemini Feature Image Created")




    final_post = {



        "title":

            article["title"],



        "meta_description":

            seo["meta_description"],



        "permalink":

            seo["permalink"],



        "labels":

            seo["label"],



        "image_alt":

            seo["image_alt"],



        "feature_image":

            feature_image,



        "internal_links":

            internal_links,



        "external_links":

            external_links,



        "content":

            seo["optimized_content"]

    }



    return final_post






if __name__ == "__main__":



    post = create_final_blog_post(

        "Kitchen Organization",

        "best kitchen cabinet organizers"

    )



    print("\n====== BLOGGER READY ======")



    print("\nTitle:")

    print(post["title"])



    print("\nImage Provider:")

    print(

        post["feature_image"]["provider"]

    )



    print("\nImage Model:")

    print(

        post["feature_image"]["model"]

    )



    print("\nImage Size:")

    print(

        post["feature_image"]["size"]

    )



    print("\nImage ALT:")

    print(

        post["image_alt"]

    )



    print("\nSTATUS: READY FOR BLOGGER")