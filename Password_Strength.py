import string


MINIMUM_LENGTH = 14
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = string.punctuation + " "
LABELS = ["Very weak", "Weak", "Fair", "Strong", "Very strong"]


def _count_types(password):
    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_symbol = False

    # Check the characters one at a time.
    for character in password:
        if character in LOWERCASE:
            has_lowercase = True
        if character in UPPERCASE:
            has_uppercase = True
        if character in DIGITS:
            has_digit = True
        if character in SYMBOLS:
            has_symbol = True

    types_used = 0
    if has_lowercase:
        types_used = types_used + 1
    if has_uppercase:
        types_used = types_used + 1
    if has_digit:
        types_used = types_used + 1
    if has_symbol:
        types_used = types_used + 1

    return types_used


def assess_password_strength(password):
    length = len(password)
    types_used = _count_types(password)
    reasons = []

    # These scores are advice, not a guarantee of security.
    if length < MINIMUM_LENGTH:
        score = 0
        reasons.append("Only " + str(length) + " characters; at least 14 are required.")
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

    return {
        "length": length,
        "score": score,
        "label": LABELS[score],
        "reasons": reasons
    }


def is_password_acceptable(password):
    result = assess_password_strength(password)
    return result["score"] >= 3


if __name__ == "__main__":
    result = assess_password_strength("Sample passphrase for testing")
    print("Strength:", result["label"])
    print("Score:", result["score"])
    for reason in result["reasons"]:
        print(reason)
