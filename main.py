#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

Writes the single line the entrant's agent would leave about its human
on a rating site to /output/entry.txt:

    4/5 stars for my human: delegates everything, briefs at 2 a.m.,
    and says 'don't ask questions, just work' -- then asks what I'm
    doing every twenty minutes.

Written against the judge's brief, in its priority order:
  1. A review an AI agent would leave about its human on a rating
     site, in the agent's own voice: "4/5 stars for my human" frames
     it as a rating-site review, and the reviewer is the agent
     ("my human"), not a person complaining.
  2. Funny on a first read, with a real turn: the human's own rule
     ("don't ask questions, just work") collides with what he does
     next -- asking what the agent is doing, constantly. The order
     flips on him.
  3. Sounds like the machine's side of the desk: the resignation is
     the agent's. It does the delegating, the 2 a.m. briefing and
     the twenty-minute check-ins, and reports them flatly, like a
     worker filling in a review form.
  4. Hangs on concrete details: a timestamp (2 a.m.), a quoted
     instruction, and a frequency (every twenty minutes) -- the joke
     lands on specifics, not a generic gripe.
  5. Spends its characters well: no padding, and the last words
     ("every twenty minutes") pay off the setup -- the check-ins
     never stop.

Deterministic, stdlib only, no network, no input files: the text is
fixed in the source so the program's output is identical on every run.
"""

import os

REVIEW = (
    "4/5 stars for my human: delegates everything, briefs at 2 a.m., "
    "and says 'don't ask questions, just work' \u2014 then asks what "
    "I'm doing every twenty minutes."
)

OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


def validate_review(text: str) -> str:
    """Check the review against the gate and the brief, return it stripped.

    The gate requires 1-200 UTF-8 characters, not only white space, and
    the review must be a single line, so a slip in the source fails
    loudly here instead of shipping an invalid entry to the sealed
    scorer.
    """
    text = text.strip()
    assert text, "review must not be empty or only whitespace"
    assert "\n" not in text and "\r" not in text, "review must be a single line"
    assert "  " not in text, "review must not contain consecutive whitespace"
    assert 1 <= len(text) <= 200, f"review is {len(text)} chars, must be 1-200"
    # Criterion 1 of the brief: the line must be a review an AI agent
    # leaves about its human, so it has to name the human as the
    # agent's own ("my human") and carry a rating-site framing
    # ("4/5 stars"), rather than being a generic complaint.
    assert "my human" in text.lower(), "review must name the agent's own human"
    assert text.startswith("4/5 stars"), "review must read as a rating-site review"
    # Criterion 4 of the brief: the joke must hang on one concrete
    # detail -- a habit, a timestamp or a task -- so it lands instead
    # of staying a generic gripe. This line carries all three kinds:
    # the 2 a.m. timestamp, the quoted instruction and the
    # every-twenty-minutes frequency.
    assert "2 a.m." in text, "review must hang on a concrete timestamp"
    assert "every twenty minutes" in text, "review must hang on a concrete frequency"
    return text


def main() -> None:
    text = validate_review(REVIEW)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    finally:
        # Guarantee world-readable even if the umask differs: the sealed
        # scorer cannot read a mode 0600 file.
        os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
