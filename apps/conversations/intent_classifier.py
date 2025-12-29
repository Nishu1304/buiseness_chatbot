def classify_intent(text: str, intents):
    text_lower = text.lower()
    best_intent = None
    best_score = 0

    for intent in intents:
        matches = sum(1 for kw in intent.keywords if kw in text_lower)

        if matches > 0:
            score = matches * intent.priority
            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent
