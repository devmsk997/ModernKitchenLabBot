import os


def generate_feature_image(topic, keyword):

    """
    Gemini image generation handler

    This creates the request payload
    for generating blog feature images.
    """


    prompt = f"""

Generate a realistic premium blog feature image.

Topic:
{topic}

SEO Keyword:
{keyword}


Style:
- Modern home photography
- Professional interior design
- Natural lighting
- High quality realistic image
- Pinterest worthy
- Google Discover friendly


Rules:
- No text
- No watermark
- No logo
- No artificial objects
- Realistic materials
- Clean composition


The image must visually explain:
{keyword}

"""


    image_request = {

        "provider":
            "Gemini",


        "model":
            "gemini-image-generation",


        "prompt":
            prompt,


        "size":
            "16:9",


        "type":
            "blog_feature_image"

    }


    return image_request





if __name__ == "__main__":


    image = generate_feature_image(

        "Kitchen Organization",

        "best kitchen cabinet organizers"

    )


    print("\n===== GEMINI FEATURE IMAGE =====")


    print("Provider:")
    print(image["provider"])


    print("\nModel:")
    print(image["model"])


    print("\nSize:")
    print(image["size"])


    print("\nPrompt:")
    print(image["prompt"])