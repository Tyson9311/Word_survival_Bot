import json, random

def load_categories():
    try:
        with open("categories.json", "r") as f:
            return json.load(f)
    except:
        return {"fruits": ["apple"], "animals": ["cat"]}

MODES = ["snake", "ladder", "category", "stopword"]

def get_random_mode():
    return random.choice(MODES)

def validate_word(mode, word, context):
    w = word.lower()
    if mode == "snake":
        return w.startswith(context["last_letter"])
    elif mode == "ladder":
        return len(w) > context["last_length"]
    elif mode == "category":
        return w in context["category_words"]
    elif mode == "stopword":
        return context["banned_letter"] not in w
    return False
