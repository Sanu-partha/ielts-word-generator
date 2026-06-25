# IELTS Word of the Day Generator

A simple Python script that picks a random Band 7+ IELTS vocabulary word, looks up its meaning, an example sentence, and synonyms using a free dictionary API, and prints it as a clean word card.

## How it works

1. Randomly selects a word from a curated list of 365 IELTS-appropriate vocabulary words (one for every day of the year)
2. Looks up the word using the [Free Dictionary API](https://dictionaryapi.dev), no API key required
3. Extracts the definition, an example sentence (if available), and up to 5 synonyms
4. If a word has no usable dictionary entry, it tries another word automatically (up to 10 attempts)
5. Prints the result as a formatted card in the terminal

## Why a curated word list instead of a random word generator

Random word generators (even ones with a "difficulty" or "rarity" filter) tend to surface obscure technical or scientific terms rather than genuine IELTS-style vocabulary. There's no reliable free API that distinguishes between "rare" and "IELTS-appropriate" — so this project uses a hand-picked list based on common IELTS Band 7–9 vocabulary resources (including terms from the Academic Word List) instead.

## Requirements

- Python 3.x
- An internet connection (the script calls a live API)

No external packages are needed, only Python's built-in `urllib`, `json`, and `random` modules.

## Usage

```bash
python ielts.py
```

Example output:

```
==================================================
  IELTS WORD OF THE DAY: METICULOUS
==================================================
Part of speech : adjective
Meaning        : showing great attention to detail; very careful and precise.
Example        : "her meticulous research"
Synonyms       : careful, scrupulous, conscientious, thorough, painstaking
==================================================
```

## Project structure

```
ielts365.py    — the full script (word list + API calls + output)
```

## Notes

- Some words may not have an example sentence available from the API — in that case, the script prompts you to write your own.
- If the dictionary API is temporarily unreachable, the script will print an error for that word and try again with a different one.

## Possible future improvements

- Save each day's word to a running log file to track vocabulary learned over time
- Add a flashcard/quiz mode to test recall of previously shown words
- Schedule the script to run automatically once a day
