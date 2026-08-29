import os


def generate_image_prompt(topic, keyword):

    prompt = f"""
Create a premium realistic feature image for a blog article.

Topic:
{topic}

Main SEO Keyword:
{keyword}


Image Style:
- Realistic interior photography
- Modern home design
- Professional Pinterest style
- High quality 4K look
- Natural lighting
- Clean composition
- Attractive for Google Discover


Requirements:
- Clearly show the topic visually
- No text inside image
- No watermark
- No brand logo
- No fake objects
- Realistic materials and details


The image should represent:
{keyword}
"""

    return prompt




def create_gemini_image_request(topic, keyword):

    prompt = generate_image_prompt(
        topic,
        keyword
    )


    request = {

        "model":
            "gemini-image-generation",


        "prompt":
            prompt,


        "aspect_ratio":
            "16:9",


        "purpose":
            "blog_feature_image"


    }


    return request





if __name__ == "__main__":


    result = create_gemini_image_request(

        "Kitchen Organization",

        "best kitchen cabinet organizers"

    )


    print("\n===== GEMINI IMAGE REQUEST =====")


    print("Model:")
    print(result["model"])


    print("\nAspect Ratio:")
    print(result["aspect_ratio"])


    print("\nPrompt:")
    print(result["prompt"])