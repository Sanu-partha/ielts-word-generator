import random
import urllib.request
import json

IELTS_WORDS = [
    "myriad", "plethora", "arid", "arduous", "ubiquitous", "meticulous", "ambiguous", "pragmatic",
    "resilient", "transparent", "tenacious", "feasible", "profound", "innovative", "substantial", "controversial",
    "detrimental", "viable", "scrutinize", "advocate", "consensus", "deteriorate", "facilitate", "implement",
    "inevitable", "mitigate", "notion", "subsequent", "comprehensive", "diminish", "exacerbate", "fluctuate",
    "intricate", "plausible", "rigorous", "skeptical", "stagnant", "unprecedented", "versatile", "vibrant",
    "volatile", "candid", "coherent", "paramount", "discernible", "augment", "constitute", "contemporary",
    "credible", "denote", "derive", "discrete", "divergent", "elicit", "empirical", "equivalent",
    "explicit", "hypothesis", "implicit", "incidence", "inherent", "integral", "interpret", "predominant",
    "prerequisite", "rational", "static", "tangible", "valid", "compelling", "discrepancy", "stringent",
    "ambivalent", "anomaly", "conducive", "deficit", "disseminate", "dwindle", "endeavor", "escalate",
    "formidable", "holistic", "imperative", "indispensable", "infer", "inhibit", "innate", "intervene",
    "lucrative", "manifest", "marginal", "obsolete", "optimal", "perpetuate", "precarious", "precedent",
    "proliferate", "prudent", "quantify", "rampant", "rectify", "reinforce", "rhetoric", "sustainable",
    "tentative", "underpin", "vested", "vindicate", "warrant", "albeit", "ascertain", "commensurate",
    "contentious", "demographic", "dichotomy", "ephemeral", "exemplify", "extrapolate", "facet", "impede",
    "juxtapose", "nuance", "ostensibly", "parameter", "pertinent", "polarize", "pragmatism", "preclude",
    "qualitative", "quantitative", "reciprocal", "spectrum", "subsidize", "synthesis", "tenable", "abate",
    "accentuate", "adverse", "aesthetic", "affluent", "aggregate", "align", "allege", "alleviate",
    "alternative", "ambivalence", "amplify", "analogous", "anticipate", "apparent", "appraisal", "apt",
    "arbitrary", "articulate", "artificial", "ascribe", "assert", "assess", "attain", "attribute",
    "autonomy", "benevolent", "bias", "bolster", "bureaucracy", "capacity", "catalyst", "chronic",
    "circumvent", "cogent", "collaborate", "collateral", "commodity", "compatible", "compensate", "complement",
    "comply", "component", "comprise", "conceive", "concession", "concurrent", "confine", "conform",
    "congruent", "conjecture", "connotation", "consequence", "considerable", "consolidate", "constraint", "contend",
    "convene", "converge", "correlate", "correspond", "counterpart", "credence", "criteria", "culminate",
    "cumulative", "curtail", "debilitate", "decisive", "decline", "deduce", "default", "deficient",
    "define", "delineate", "demonstrate", "denounce", "depict", "deplete", "depreciate", "derogatory",
    "deviate", "devise", "diagnose", "differentiate", "diffuse", "digress", "disclose", "discourse",
    "dispel", "disposition", "disproportionate", "distinct", "distort", "diversify", "document", "domain",
    "dominant", "downturn", "duration", "dynamic", "eccentric", "eclectic", "edifice", "elaborate",
    "eliminate", "eloquent", "embed", "encompass", "endorse", "enhance", "ensue", "entail",
    "equate", "equilibrium", "erode", "erratic", "establish", "estimate", "ethical", "evaluate",
    "evident", "evoke", "exceed", "exclude", "exhaustive", "expand", "expedite", "exploit",
    "expound", "extensive", "external", "factor", "federal", "flaw", "flexible", "focal",
    "forfeit", "format", "formulate", "fundamental", "furnish", "generate", "generic", "grant",
    "guarantee", "hence", "hierarchy", "hinder", "hypothetical", "identical", "identify", "ideology",
    "ignorance", "illustrate", "immense", "immune", "impact", "implicate", "inadequate", "incentive",
    "incline", "incompatible", "inconsistent", "incorporate", "index", "indicate", "infinite", "infrastructure",
    "initiate", "innovate", "insight", "insufficient", "integrate", "intermediate", "internal", "interval",
    "intrinsic", "invoke", "isolate", "justify", "labor", "layer", "legislate", "liable",
    "license", "likewise", "locate", "logic", "maintain", "mandate", "manipulate", "margin",
    "mature", "maximize", "mechanism", "mediate", "medium", "mental", "method", "migrate",
    "minimal", "minimize", "minor", "mode", "modify", "monitor", "motive", "mutual",
    "negate", "negligible", "network", "neutral", "nevertheless", "nonetheless", "norm", "notable",
    "notwithstanding", "nullify", "objective", "obtain", "occupy", "offset", "ongoing",
    "option", "outcome", "output", "overall", "overlap", "panel",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_word_data(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Could not fetch '{word}': {e}")
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


def get_daily_word(max_attempts: int = 10):
    attempted = set()
    for _ in range(max_attempts):
        candidates = [w for w in IELTS_WORDS if w not in attempted]
        if not candidates:
            break
        word = random.choice(candidates)
        attempted.add(word)

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