def analyze_intent(keyword):

    keyword = keyword.lower()


    buying_words = [
        "best",
        "review",
        "buy",
        "product",
        "top",
        "vs",
        "comparison",
        "for sale"
    ]


    informational_words = [
        "ideas",
        "how",
        "guide",
        "tips",
        "ways",
        "tutorial"
    ]


    for word in buying_words:
        if word in keyword:
            return {
                "intent": "commercial",
                "affiliate_value": "high"
            }


    for word in informational_words:
        if word in keyword:
            return {
                "intent": "informational",
                "affiliate_value": "medium"
            }


    return {
        "intent": "unknown",
        "affiliate_value": "low"
    }



if __name__ == "__main__":

    result = analyze_intent(
        "best spice organizer for kitchen"
    )


    print(result)