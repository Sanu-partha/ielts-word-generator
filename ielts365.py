import random
import urllib.request
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    "intrinsic", "invoke", "isolate", "justify", "linchpin", "lackluster", "lavish", "liable",
    "license", "luminous", "lucid", "luxuriant", "maintain", "mandate", "manipulate", "margin",
    "mature", "maximize", "mechanism", "mediate", "medium", "mental", "method", "migrate",
    "minimal", "minimize", "minor", "mode", "modify", "monitor", "motive", "mutual",
    "negate", "negligible", "network", "neutral", "nevertheless", "nonetheless", "norm", "notable",
    "notwithstanding", "nullify", "objective", "obtain", "occupy", "offset", "ongoing",
    "option", "outcome", "output", "overall", "overlap", "panel",
]

WORD_OVERRIDES = {
    "resilient": {
        "part_of_speech": "adjective",
        "meaning": "Able to recover quickly from difficulties; tough and adaptable.",
        "example": "She remained resilient despite the setbacks in her career.",
        "synonyms": ["tough", "adaptable", "hardy", "robust"],
    },
    "notion": {
        "part_of_speech": "noun",
        "meaning": "An idea, belief, or understanding of something.",
        "example": "He had a vague notion of how the system worked.",
        "synonyms": ["idea", "concept", "belief", "impression"],
    },
    "mechanism": {
        "part_of_speech": "noun",
        "meaning": "A process, system, or set of steps by which something is done or achieved.",
        "example": "The government introduced a new mechanism to resolve trade disputes.",
        "synonyms": ["process", "system", "method", "procedure"],
    },
}

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

    meanings = entry.get("meanings", [])

    pos_priority = {"verb": 0, "adjective": 1, "adverb": 2, "noun": 3}
    meanings = sorted(meanings, key=lambda m: pos_priority.get(m.get("partOfSpeech", ""), 4))

    meaning, part_of_speech = None, ""
    example = None
    synonyms = []

    fallback = None

    for meaning_block in meanings:
        block_pos = meaning_block.get("partOfSpeech", "")
        block_synonyms = meaning_block.get("synonyms", [])

        for definition in meaning_block.get("definitions", []):
            def_meaning = definition.get("definition")
            def_example = definition.get("example")
            def_synonyms = list(definition.get("synonyms", [])) or list(block_synonyms)

            if not def_meaning:
                continue

            if fallback is None:
                fallback = (def_meaning, block_pos, def_example, def_synonyms)

            if def_example or def_synonyms:
                meaning = def_meaning
                part_of_speech = block_pos
                example = def_example
                synonyms = def_synonyms
                break

        if meaning:
            break

    if meaning is None and fallback is not None:
        meaning, part_of_speech, example, synonyms = fallback

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

        if word in WORD_OVERRIDES:
            override = WORD_OVERRIDES[word]
            return {
                "word": word,
                "part_of_speech": override.get("part_of_speech", ""),
                "meaning": override["meaning"],
                "example": override.get("example"),
                "synonyms": override.get("synonyms", []),
            }

        data = fetch_word_data(word)
        if data:
            details = extract_details(data)
            if details["meaning"]:
                return details
    return None


def build_word_card_text(details):
    lines = []
    lines.append("=" * 50)
    lines.append(f"  IELTS WORD OF THE DAY: {details['word'].upper()}")
    lines.append("=" * 50)
    if details["part_of_speech"]:
        lines.append(f"Part of speech : {details['part_of_speech']}")
    lines.append(f"Meaning        : {details['meaning']}")
    if details["example"]:
        lines.append(f"Example        : \"{details['example']}\"")
    else:
        lines.append(f"Example        : Try using \"{details['word']}\" in your sentence today!")
    if details["synonyms"]:
        lines.append(f"Synonyms       : {', '.join(details['synonyms'])}")
    else:
        lines.append("Synonyms       : (none found)")
    lines.append("=" * 50)
    return "\n".join(lines)


def build_word_card_html(details):
    example_html = (
        f'<p style="margin:0 0 6px 0;"><strong>Example</strong><br>'
        f'<em>"{details["example"]}"</em></p>'
        if details["example"]
        else f'<p style="margin:0 0 6px 0; color:#888;"><strong>Example</strong><br>'
             f'Try using "{details["word"]}" in your sentence today!</p>'
    )

    synonyms_html = (
        f'<p style="margin:0;"><strong>Synonyms</strong><br>{", ".join(details["synonyms"])}</p>'
        if details["synonyms"]
        else '<p style="margin:0; color:#888;"><strong>Synonyms</strong><br>None found</p>'
    )

    pos_html = (
        f'<span style="display:inline-block; background:#eef2ff; color:#4338ca; '
        f'font-size:12px; font-weight:600; padding:4px 10px; border-radius:12px; '
        f'text-transform:uppercase; letter-spacing:0.5px;">{details["part_of_speech"]}</span>'
        if details["part_of_speech"]
        else ""
    )

    html = f"""
    <div style="font-family:'Segoe UI', Arial, sans-serif; max-width:480px; margin:0 auto;
                background:#ffffff; border-radius:16px; overflow:hidden;
                box-shadow:0 4px 16px rgba(0,0,0,0.08); border:1px solid #eee;">
      <div style="background:linear-gradient(135deg,#4f46e5,#7c3aed); padding:24px 28px;">
        <p style="margin:0; color:#e0e7ff; font-size:13px; letter-spacing:1px; text-transform:uppercase;">
          IELTS Word of the Day
        </p>
        <h1 style="margin:6px 0 0 0; color:#ffffff; font-size:32px; font-weight:700;">
          {details['word'].capitalize()}
        </h1>
        {pos_html}
      </div>
      <div style="padding:24px 28px;">
        <p style="margin:0 0 16px 0; font-size:15px; color:#1f2937; line-height:1.5;">
          <strong>Meaning</strong><br>{details['meaning']}
        </p>
        <div style="font-size:15px; color:#1f2937; line-height:1.5; margin-bottom:16px;">
          {example_html}
        </div>
        <div style="font-size:15px; color:#1f2937; line-height:1.5;">
          {synonyms_html}
        </div>
      </div>
      <div style="background:#f9fafb; padding:14px 28px; text-align:center;">
        <p style="margin:0; font-size:12px; color:#9ca3af;">
          One word a day, every day for a year &mdash; 365 words to go.
        </p>
      </div>
    </div>
    """
    return html


def send_email(subject: str, plain_body: str, html_body: str):
    sender_email = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient_raw = os.environ.get("RECIPIENT_EMAIL", sender_email)
    recipient_emails = [email.strip() for email in recipient_raw.split(",") if email.strip()]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = sender_email

    message.attach(MIMEText(plain_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))

    all_recipients = list(dict.fromkeys([sender_email] + recipient_emails))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, all_recipients, message.as_string())


def print_word_card(details):
    print(build_word_card_text(details))


if __name__ == "__main__":
    result = get_daily_word()
    if result:
        print_word_card(result)
        if "GMAIL_ADDRESS" in os.environ and "GMAIL_APP_PASSWORD" in os.environ:
            subject = f"IELTS Word of the Day: {result['word'].capitalize()}"
            plain_body = build_word_card_text(result)
            html_body = build_word_card_html(result)
            send_email(subject, plain_body, html_body)
            print("Email sent successfully.")
    else:
        print("Could not fetch a word today — check your internet connection and try again.")