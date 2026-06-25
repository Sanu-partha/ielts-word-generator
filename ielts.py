import random
import urllib.request
import json

IELTS_WORDS = [
    "eloquent", "ubiquitous", "meticulous", "ambiguous", "pragmatic",
    "resilient", "transparent", "tenacious", "feasible", "profound",
    "innovative", "substantial", "controversial", "detrimental", "viable",
    "scrutinize", "advocate", "consensus", "deteriorate", "facilitate",
    "implement", "inevitable", "mitigate", "notion", "subsequent",
    "comprehensive", "diminish", "exacerbate", "fluctuate", "intricate",
    "plausible", "rigorous", "skeptical", "stagnant", "unprecedented",
    "versatile", "vibrant", "volatile", "candid", "coherent",
]


def fetch_word_data(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Could not fetch '{word}': {e}")
        return None


def extract_details(data):
    entry = data[0]
    word = entry.get("word", "")

    meaning, example, synonyms = None, None, []

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


def get_daily_word(max_attempts: int = 5):
    attempted = set()
    for _ in range(max_attempts):
        candidates = [w for w in IELTS_WORDS if w not in attempted]
        if not candidates:
            break
        word = random.choice(candidates)
        attempted.add(word)

        data = fetch_word_data(word)
        if data:
            return extract_details(data)
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