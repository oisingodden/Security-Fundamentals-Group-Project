import secrets
import string


# The same minimum the master password module enforces.
MINIMUM_LENGTH = 14

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?"


def generate_password(length=20):
    # The only rule: a password must be long enough.
    if length < MINIMUM_LENGTH:
        raise ValueError(f"Use at least {MINIMUM_LENGTH} characters.")

    # Start with one character from every type so each type is guaranteed.
    characters = [
        secrets.choice(LOWERCASE),
        secrets.choice(UPPERCASE),
        secrets.choice(DIGITS),
        secrets.choice(SYMBOLS),
    ]

    # Fill the rest from all types combined.
    combined = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS
    while len(characters) < length:
        characters.append(secrets.choice(combined))

    # Shuffle so the guaranteed characters are not always at the start.
    secrets.SystemRandom().shuffle(characters)

    return "".join(characters)


if __name__ == "__main__":
    print("Default (20 characters):", generate_password())
    print("32 characters:          ", generate_password(32))