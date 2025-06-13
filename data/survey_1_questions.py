question_list = [
    {
        "type": "open",
        "question": "What do you like the most about our product?",
        "key": "like_most"
    },
    {
        "type": "single_choice",
        "question": "How did you hear about us?",
        "options": ["Social Media", "Search Engine", "Friend", "Other"],
        "key": "referral_source"
    },
    {
        "type": "multiple_choice",
        "question": "Which features are most useful to you? (Select all that apply)",
        "options": ["Price", "Ease of use", "Support", "Design", "Speed"],
        "key": "useful_features"
    },
    {
        "type": "rating",
        "question": "How likely are you to recommend us to a friend? (1 = Not likely, 10 = Very likely)",
        "min": 1,
        "max": 10,
        "key": "nps_score"
    }
]
