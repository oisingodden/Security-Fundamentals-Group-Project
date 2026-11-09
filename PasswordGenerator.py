import secrets
import string


MINIMUM_LENGTH = 14
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?"


def generate_password(length=20):
    if length < MINIMUM_LENGTH:
        raise ValueError("Use at least 14 characters.")

    # Include one character from each group.
    characters = []
    characters.append(secrets.choice(LOWERCASE))
    characters.append(secrets.choice(UPPERCASE))
    characters.append(secrets.choice(DIGITS))
    characters.append(secrets.choice(SYMBOLS))

    # Add random characters until the chosen length is reached.
    all_characters = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS
    while len(characters) < length:
        characters.append(secrets.choice(all_characters))

    # Pick and remove characters to put them in a random order.
    password = ""
    while len(characters) > 0:
        character = secrets.choice(characters)
        password = password + character
        characters.remove(character)

    return password


if __name__ == "__main__":
    print("Generated password:", generate_password())
