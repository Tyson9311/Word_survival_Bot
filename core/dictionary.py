DICTIONARY_FILE = "dictionary.txt"

def load_words():
    try:
        with open(DICTIONARY_FILE, "r") as f:
            return set(w.strip().lower() for w in f if w.strip())
    except FileNotFoundError:
        return set()

def save_word(word):
    w = word.strip().lower()
    words = load_words()
    if w in words:
        return False
    with open(DICTIONARY_FILE, "a") as f:
        f.write(f"{w}\n")
    return True

def remove_word(word):
    w = word.strip().lower()
    words = load_words()
    if w not in words:
        return False
    words.remove(w)
    with open(DICTIONARY_FILE, "w") as f:
        for x in sorted(words):
            f.write(f"{x}\n")
    return True

def is_valid_word(word):
    return word.strip().lower() in load_words()
