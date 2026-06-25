import random
import urllib.request
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_url(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def get_random_candidate_words(count=5, difficulty=5):
    url = f"https://random-word-api.herokuapp.com/word?number={count}&diff={difficulty}"
    try:
        words = fetch_url(url)
        return [w.lower() for w in words if w.isalpha()]
    except Exception as e:
        print(f"Random word API unavailable ({e}), falling back to curated list.")
        return []


def fetch_word_data(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        return fetch_url(url)
    except Exception:
        return None


def extract_details(data):
    entry = data[0]
    word = entry.get("word", "")

    meaning, example, synonyms = None, None, []
    part_of_speech = ""

    for meaning_block in entry.get("meanings", []):
        part_of_speech = meaning_block.get("partOfSpeech", "")
        for definition in meaning_block.get("definitions", []):
            if meaning is None:
                meaning = definition.get("definition")
                example = definition.get("example")
            synonyms.extend(definition.get("synonyms", []))
        synonyms.extend(meaning_block.get("synonyms", []))
        if meaning:
            break

    synonyms = list(dict.fromkeys(synonyms))[:5]

    return {
        "word": word,
        "part_of_speech": part_of_speech if meaning else "",
        "meaning": meaning,
        "example": example,
        "synonyms": synonyms,
    }


def get_daily_word(max_attempts: int = 15):
    attempted = set()

    candidates = get_random_candidate_words(count=5, difficulty=5)
    candidates += get_random_candidate_words(count=5, difficulty=4)

    random.shuffle(candidates)

    attempts_made = 0
    index = 0
    while attempts_made < max_attempts:
        if index >= len(candidates):
            more = get_random_candidate_words(count=5, difficulty=5)
            more += get_random_candidate_words(count=5, difficulty=4)
            more = [w for w in more if w not in attempted and w not in candidates]
            if not more:
                break
            candidates += more

        word = candidates[index]
        index += 1
        if word in attempted:
            continue
        attempted.add(word)
        attempts_made += 1

        data = fetch_word_data(word)
        if data:
            details = extract_details(data)
            if details["meaning"]:
                return details

    return None


def print_word_card(details):
    print("=" * 50)
    print(f"  IELTS WORD OF THE DAY: {details['word'].upper()}")
    print("=" * 50)
    if details["part_of_speech"]:
        print(f"Part of speech : {details['part_of_speech']}")
    print(f"Meaning        : {details['meaning']}")
    if details["example"]:
        print(f"Example        : \"{details['example']}\"")
    else:
        print("Example        : (none provided by API — write your own IELTS sentence!)")
    if details["synonyms"]:
        print(f"Synonyms       : {', '.join(details['synonyms'])}")
    else:
        print("Synonyms       : (none found)")
    print("=" * 50)


if __name__ == "__main__":
    result = get_daily_word()
    if result:
        print_word_card(result)
    else:
        print("Could not fetch a word today — check your internet connection and try again.")