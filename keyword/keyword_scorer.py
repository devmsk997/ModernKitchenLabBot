def calculate_keyword_score(
    search_volume,
    keyword_difficulty,
    traffic_potential,
    buyer_intent,
    trend_growth
):
    """
    Modern Kitchen Lab
    Traffic First SEO Scoring System
    """

    # Search demand (35%)
    volume_score = min(
        (search_volume / 1000) * 35,
        35
    )

    # Competition advantage (25%)
    difficulty_score = max(
        25 - keyword_difficulty,
        0
    )

    # Visitor potential (25%)
    traffic_score = traffic_potential * 25

    # Affiliate value (10%)
    intent_score = buyer_intent * 10

    # Trend (5%)
    trend_score = trend_growth * 5


    score = (
        volume_score
        + difficulty_score
        + traffic_score
        + intent_score
        + trend_score
    )


    return round(score, 2)



def keyword_quality(score):

    if score >= 90:
        return "🔥 High Priority Article"

    elif score >= 80:
        return "✅ Approved Article"

    elif score >= 70:
        return "🟡 Need More Analysis"

    else:
        return "❌ Reject"



if __name__ == "__main__":

    score = calculate_keyword_score(
        search_volume=15000,
        keyword_difficulty=10,
        traffic_potential=1.0,
        buyer_intent=0.8,
        trend_growth=0.9
    )


    print("SEO Opportunity Score:", score)
    print("Decision:", keyword_quality(score))