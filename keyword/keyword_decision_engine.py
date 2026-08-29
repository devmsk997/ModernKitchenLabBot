def decide_keyword(
    keyword,
    score,
    intent
):

    decision = {
        "keyword": keyword,
        "score": score,
        "intent": intent,
        "status": "",
        "priority": ""
    }


    # Visitor first strategy

    if score >= 70 and intent == "commercial":
        decision["status"] = "approved"
        decision["priority"] = "high"


    elif score >= 60:
        decision["status"] = "approved"
        decision["priority"] = "medium"


    else:
        decision["status"] = "rejected"
        decision["priority"] = "low"


    return decision



if __name__ == "__main__":


    result = decide_keyword(
        keyword="best spice organizer for kitchen",
        score=69,
        intent="commercial"
    )


    print(result)