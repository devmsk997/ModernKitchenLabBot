import random


# Future: এখানে Google Keyword API / SEO API connect করা হবে
# এখন আমরা foundation তৈরি করছি


KITCHEN_KEYWORDS = [
    "small kitchen organization ideas",
    "best kitchen cabinet organizers",
    "kitchen storage ideas",
    "pantry organization ideas",
    "best spice organizer for kitchen",
    "under sink storage ideas",
    "kitchen drawer organizer ideas"
]


def get_keyword_candidates():

    """
    Return possible keywords
    """

    return KITCHEN_KEYWORDS



def select_keyword():

    keywords = get_keyword_candidates()

    keyword = random.choice(keywords)

    return keyword



if __name__ == "__main__":

    keyword = select_keyword()

    print("Selected Keyword:")
    print(keyword)