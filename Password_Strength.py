import string


# The same minimum the master password module enforces.
MINIMUM_LENGTH = 14

LOWERCASE = set(string.ascii_lowercase)
UPPERCASE = set(string.ascii_uppercase)
DIGITS = set(string.digits)
SYMBOLS = set(string.punctuation) | {" "}

LABELS = ["Very weak", "Weak", "Fair", "Strong", "Very strong"]


def _count_types(password):
    # How many of the four character types the password uses.
    types_used = 0
    if any(character in LOWERCASE for character in password):
        types_used += 1
    if any(character in UPPERCASE for character in password):
        types_used += 1
    if any(character in DIGITS for character in password):
        types_used += 1
    if any(character in SYMBOLS for character in password):
        types_used += 1
    return types_used


def assess_password_strength(password):
    length = len(password)
    types_used = _count_types(password)
    reasons = []

    # Score 0 to 4, based on length first and character variety second.
    if length < MINIMUM_LENGTH:
        score = 0
        reasons.append(
            f"Only {length} characters; at least {MINIMUM_LENGTH} are required."
        )
    else:
        score = 1
        if length >= 16 and types_used >= 2:
            score = 2
        if length >= 18 and types_used >= 3:
            score = 3
        if length >= 20 and types_used == 4:
            score = 4

    if types_used < 2:
        reasons.append("Use a mix of letters, digits and symbols.")
    elif types_used == 2:
        reasons.append("Add another character type for a stronger password.")

    # Return the assessment without ever echoing the password back.
    return {
        "length": length,
        "score": score,
        "label": LABELS[score],
        "reasons": reasons,
    }


def is_password_acceptable(password):
    return assess_password_strength(password)["score"] >= 3


if __name__ == "__main__":
    samples = [
        "password123",
        "Ab3!xy",
        "Sample passphrase for testing",
        "v3X!q8Zt#Lm2@Rw9",
    ]

    for sample in samples:
        result = assess_password_strength(sample)
        print(f"{result['label']:<11} score={result['score']}  {sample!r}")
        for reason in result["reasons"]:
            print("    -", reason)