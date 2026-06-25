# IELTS365: Daily IELTS Word Generator

A Python script that picks one Band 7+ IELTS vocabulary word per day, looks up its meaning, an example sentence, and synonyms using a free dictionary API, and emails it as a styled HTML card. Runs automatically every morning via GitHub Actions. No server, no hosting, no manual triggering required.

## What it does

1. Randomly picks a word from a curated list of **365 IELTS Band 7-9 vocabulary words** (one for every day of the year, no repeats within a full cycle)
2. Looks up the word using the [Free Dictionary API](https://dictionaryapi.dev), which requires no API key
3. Prioritises **verb/adjective senses** over noun senses when multiple definitions exist, to avoid surfacing obscure or irrelevant meanings (e.g. avoiding heraldry-specific definitions for everyday words)
4. Scans **all** available definitions for the word, not just the first one found, to pull the best available example sentence and combine all available synonyms
5. Checks a small **manual override list** first, for specific words where the dictionary API consistently returns the wrong sense or weak data
6. If a word has no usable dictionary entry at all, it tries another word automatically (up to 10 attempts)
7. Builds both a plain-text and a styled **HTML email card** (purple gradient header, part-of-speech badge, clean typography)
8. Sends the email via Gmail SMTP to one or more recipients, using **BCC** so recipients can't see each other's addresses
9. Runs automatically every day at **7:00 AM IST** via a scheduled **GitHub Actions** workflow

## Why a curated word list instead of a random word generator

Random word generators, even ones with a "difficulty" or "rarity" filter, tend to surface obscure technical or scientific terms (e.g. *hymenopterans*) rather than genuine IELTS-style vocabulary. There's no reliable free API that distinguishes "rare" from "IELTS-appropriate," so this project uses a hand-picked list instead, based on common IELTS Band 7-9 vocabulary resources and the Academic Word List.

## Why a manual override list

Free dictionary data is crowd-sourced (via Wiktionary) and isn't curated for relevance. Some words have multiple unrelated senses, and the "first" one returned by the API isn't always the useful one. For example, *resilient* initially returned its physical/elastic sense ("returning to original shape after force is applied") instead of the more IELTS-relevant character sense ("able to recover quickly from difficulties"). Rather than rewriting the whole extraction logic for edge cases like this, a small override dictionary lets specific problem words be hand-corrected as they're discovered.

## Requirements

- Python 3.x
- An internet connection (the script calls a live API and an SMTP server)
- No external packages. Only Python's built-in `urllib`, `json`, `random`, `os`, `smtplib`, and `email` modules

## Local usage

```bash
python ielts365.py
```

If run without email environment variables set, it simply prints the word card to the terminal. If `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` are set as environment variables, it also sends the email.

## Automated daily email (GitHub Actions)

The repository includes `.github/workflows/daily.yml`, which runs the script automatically every day at 7:00 AM IST (1:30 AM UTC) using GitHub's free Actions infrastructure. No need to keep a computer running.

### Setup

1. **Enable 2-Step Verification** on the sending Gmail account
2. Generate a **Gmail App Password** at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. In the repository's **Settings > Secrets and variables > Actions**, add:
   - `GMAIL_ADDRESS`: the sending Gmail address
   - `GMAIL_APP_PASSWORD`: the 16-character app password
   - `RECIPIENT_EMAIL`: one email, or multiple comma-separated emails (e.g. `me@gmail.com,partner@gmail.com`)
4. Push to `main`. The workflow is now live and will run on schedule
5. To test immediately without waiting for the schedule, go to the **Actions** tab, select **Daily IELTS Word**, then click **Run workflow**

```

## Notes

- Some words may have no example sentence or synonyms available from the API. In that case, the script shows a personalised prompt ("Try using '[word]' in your sentence today!") instead of leaving it blank.
- All recipients are added via BCC, so nobody in the recipient list can see who else received the email.
- Up to 100 recipients are supported per email (Gmail's own SMTP limit), far more than needed for personal use.

## Possible future improvements

- Expand the manual override list as more wrong-sense or weak-data words are discovered
- Save each day's word to a running log file to track vocabulary learned over time
- Add a flashcard/quiz mode to test recall of previously shown words
- Audit the full 365-word list against the dictionary API to proactively catch more override candidates
