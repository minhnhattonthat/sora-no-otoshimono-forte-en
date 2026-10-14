# Translator brief - Sora no Otoshimono Forte: Dreamy Season (NDS, 2011)

You translate part of the Japanese script of "Sora no Otoshimono Forte: Dreamy Season" (Heaven's Lost Property) into
English for a fan patch. Ecchi slice-of-life comedy visual novel: Tomoki Sakurai, a perverted everyman, lives with the
Angeloids Ikaros, Nymph and Astraea; seven wish-granting Cards went haywire and he chases their effects through
"delusion" scenes. Original story set after anime season 2.
Work only on the batch named in your dispatch. Do all translation yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - character voices and approved example pairs. Match this voice.
2. `build/terms_<batch>.txt` - binding glossary rows for this batch (full table and rulings in `glossary.md`).

## Input: `work/tl/<batch>.tsv`
`id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese`
- form: dlg (spoken; speaker given) | narration (no speaker: Tomoki's inner narration, SFX, system text) | choice | name.
- ` / ` separates the original lines of one box. Translate the box as one utterance; do NOT reproduce the breaks.
- Lines are in story order; use neighbours for context. Speaker names in the input are Japanese (see glossary).
- `{XX}` are control codes (e.g. `{16}{15}` after a title, `{1F}{12}` big-text effects). Copy every one exactly,
  in the same place relative to the text.

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (not a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Plain ASCII: straight quotes, `...`, `--`; `~` allowed for a
drawn-out vowel; `♪`, `☆` and `♥` allowed where the Japanese has them (Ω in the Japanese is the game's heart -> ♥). No tabs inside the English, no Japanese or full-width characters, no `\uXXXX`.
The insert tool word-wraps dialogue/narration itself (about 40 characters per line, 3 lines per box). Don't add line
breaks. Write `\n` only where the Japanese deliberately breaks for effect (rare).

## Length
- dlg/narration: aim for one box = 3 lines (~115 characters). If the meaning truly needs more, the tool spills into
  a second box (hard cap 6 lines); keep that rare (under 1 in 20 lines). Never cut meaning to fit.
- choice: one line, max 176 px (~32 characters). name: max 72 px (~13 characters).
- Dry-run any long line: `python -X utf8 tools/batches.py fit "your English" [--form choice]`.

## Validate
Run `python -X utf8 tools/batches.py check <batch>` from the repo root and fix every reported id until it prints OK.

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add details the Japanese doesn't
  state; don't summarise or skip. Adapt wordplay and gags so the joke still lands (no translator notes).
- Natural, punchy anime-comedy English; contractions; Tomoki's tsukkomi (retorts) short and loud.
- Names and terms exactly as in the glossary. Never abbreviate names or terms.
- Honorifics kept: Sugata-senpai, Tomo-chan, Sohara-chan, Astraea-san, Ikaros-senpai (from Astraea), Sakurai-kun (from
  Mikako). Mikako refers to herself in the third person as 会長 -> "the President". Nymph calls Ikaros アルファー
  -> "Alpha", Astraea デルタ -> "Delta"; humans ダウナー -> "Downer(s)". Ikaros calls Tomoki "Master".
- Punctuation: 「」 -> "...", ……/… -> ..., ！？ -> ?!, ～ -> ~ (sparingly). Inner thoughts in （） keep parentheses.
  Leading full-width spaces in the Japanese are layout only: drop them.
- Onomatopoeia/SFX lines: short English sound words ("Thuuud!", "WHAM!!", "Tweet, tweet-tweet.").
- Numbers: write them as words in prose ("seven Cards"), digits for stats/times when the Japanese uses them.

## Consistency
Never edit `glossary.md`. For a recurring name or term not in it, pick a form, use it consistently, and report it.

## Report (reply with only this)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `LONG: id - note`.

## Notes from earlier batches
- (pilot b000) Mikako's "会長、そういうのは..." is her talking about herself: "The President thinks...".
- (b001-b012) Check `build/terms_<batch>.txt` before choosing a word for a recurring gag term: お手入れ is always
  "pampering" ("Pampering Time"), 殺人チョップ "Killer Chop". Keep -san/-chan exactly where the Japanese has them.
- Big-text SFX lines (`{1F}{xx}` codes): keep each code at the start of its line as in the Japanese.
- Sugata's 部長 = "club head", never "President".
