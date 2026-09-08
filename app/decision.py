
from .search import search


# --------------------------------------------------
# Thresholds
# --------------------------------------------------

ANSWER_THRESHOLD = 0.42


# --------------------------------------------------
# Detect whether two passages discuss the same topic
# --------------------------------------------------

def same_topic(text1, text2):

    keywords = [
        "attendance",
        "examination",
        "exam",
        "medical",
        "absence",
        "registration",
        "fee",
        "hostel",
        "scholarship",
        "eligibility",
        "deadline",
        "extension",
        "appeal",
        "committee",
        "approval",
        "leave",
    ]

    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    common = words1.intersection(words2)

    topic_matches = sum(
        1 for keyword in keywords
        if keyword in words1 and keyword in words2
    )

    return len(common) >= 5 and topic_matches >= 1


# --------------------------------------------------
# Simple contradiction detection
# --------------------------------------------------

def contradicts(text1, text2):

    t1 = text1.lower()
    t2 = text2.lower()

    contradiction_pairs = [
        ("75%", "60%"),
        ("75%", "70%"),
        ("60%", "75%"),
        ("70%", "75%"),
        ("10:00 pm", "11:00 pm"),
        ("11:00 pm", "10:00 pm"),
        ("15 august", "20 august"),
        ("20 august", "15 august"),
        ("not permitted", "permitted"),
        ("not allowed", "allowed"),
        ("prohibited", "permitted"),
        ("no extension", "extension may"),
        ("not eligible", "eligible"),
    ]

    for a, b in contradiction_pairs:

        if a in t1 and b in t2:
            return True

        if b in t1 and a in t2:
            return True

    return False


# --------------------------------------------------
# Decide response type
# --------------------------------------------------

def decide(question):

    results = search(question, top_k=8)

    # --------------------------------------------------
    # NOT COVERED
    # --------------------------------------------------

    if not results:

        return {
            "status": "not_covered",
            "answer": (
                "The rulebook does not contain enough information "
                "to answer this question."
            ),
            "citations": []
        }

    strong_results = [
        result
        for result in results
        if result["similarity"] >= ANSWER_THRESHOLD
    ]

    if not strong_results:

        return {
            "status": "not_covered",
            "answer": (
                "The rulebook does not contain enough information "
                "to answer this question."
            ),
            "citations": []
        }

    # --------------------------------------------------
    # CONFLICT DETECTION
    # --------------------------------------------------

    for i in range(len(strong_results)):

        for j in range(i + 1, len(strong_results)):

            first = strong_results[i]
            second = strong_results[j]

            if same_topic(first["text"], second["text"]):

                if contradicts(
                    first["text"],
                    second["text"]
                ):

                    return {
                        "status": "conflict",
                        "answer": (
                            "The rulebook contains conflicting "
                            "provisions relevant to this question."
                        ),
                        "citations": [
                            first,
                            second
                        ]
                    }

    # --------------------------------------------------
    # ANSWERED
    # --------------------------------------------------

    best = strong_results[0]

    return {
        "status": "answered",
        "answer": best["text"],
        "citations": strong_results[:5]
    }


# --------------------------------------------------
# Manual test
# --------------------------------------------------

if __name__ == "__main__":

    question = input("\nAsk RuleGuard a question: ")

    result = decide(question)

    print("\n===================================")
    print("STATUS:", result["status"].upper())
    print("===================================\n")

    # --------------------------------------------------
    # ANSWERED
    # --------------------------------------------------

    if result["status"] == "answered":

        print("ANSWER:")
        print(result["answer"])

        if result["citations"]:

            citation = result["citations"][0]

            print("\nEVIDENCE:")
            print(citation["section"])

            print("\nSOURCE:")
            print(citation["source"])

            print(
                "\nSIMILARITY:",
                f"{citation['similarity']:.4f}"
            )

    # --------------------------------------------------
    # NOT COVERED
    # --------------------------------------------------

    elif result["status"] == "not_covered":

        print("ANSWER:")
        print(result["answer"])

    # --------------------------------------------------
    # CONFLICT
    # --------------------------------------------------

    elif result["status"] == "conflict":

        print("WARNING:")
        print(result["answer"])

        print("\nCONFLICTING PROVISIONS:")

        for i, citation in enumerate(
            result["citations"],
            start=1
        ):

            print(f"\nProvision {i}:")
            print("Section:", citation["section"])
            print("Source:", citation["source"])
            print("Text:", citation["text"])
            print(
                "Similarity:",
                f"{citation['similarity']:.4f}"
            )

    print("\n===================================")

