from keyword_researcher import select_keyword
from keyword_scorer import calculate_keyword_score, keyword_quality
from intent_analyzer import analyze_intent
from keyword_decision_engine import decide_keyword



def run_keyword_pipeline():

    # Step 1: Get keyword
    keyword = select_keyword()


    # Step 2: Analyze search intent
    intent_data = analyze_intent(keyword)


    # Step 3: Temporary SEO metrics
    # Later real API data will come here
    search_volume = 15000
    keyword_difficulty = 10
    traffic_potential = 1.0
    buyer_intent = 0.8
    trend_growth = 0.9


    # Step 4: Calculate score
    score = calculate_keyword_score(
        search_volume,
        keyword_difficulty,
        traffic_potential,
        buyer_intent,
        trend_growth
    )


    # Step 5: Final decision
    decision = decide_keyword(
        keyword,
        score,
        intent_data["intent"]
    )


    print("\n========== KEYWORD REPORT ==========")

    print("Keyword:", keyword)

    print("Intent:", intent_data)

    print("SEO Score:", score)

    print("Quality:", keyword_quality(score))

    print("Decision:", decision)

    print("====================================")



if __name__ == "__main__":

    run_keyword_pipeline()