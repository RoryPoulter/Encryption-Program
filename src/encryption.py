from random import choice


class Key:
    def __init__(self, base10):
        """
        Creates a key object
        :param base10: The base-10 representation of the key
        :type base10: int | str
        """
        self.base10 = int(base10)
        self.base26 = base10ToBase26(self.base10)
        self.forward_mapping = self.generateMapping()  # Decrypted -> Encrypted
        self.backward_mapping = invertDictionary(self.forward_mapping)  # Encrypted -> Decrypted

        valid = testKey(self)
        if not valid:
            raise ValueError("Invalid key: base-10 value does not produce unique mapping")

    def __repr__(self):
        """
        Represents the key as its base-10 value
        :return: The base-10 value
        """
        return self.base10

    def __str__(self):
        return str(self.base10)

    def generateMapping(self):
        """
        Generates the letter mapping from the key
        :return: The letter mapping
        :rtype: dict[str, str]
        """
        mapping = {}
        for i in range(26):
            shift = BASE26_DIGITS.index(self.base26[i])
            place = (shift + i) % 26
            mapping[LETTERS[i]] = LETTERS[place]
        return mapping

    def mapLetters(self, text, mode="encrypt"):
        """
        Used to map letters using a mapping
        :param text: The text which will have the mapping applied to
        :type text: str
        :param mode:
        :return: The mapped text
        :rtype: str
        """
        if mode == "encrypt":
            mapping = self.forward_mapping
        elif mode == "decrypt":
            mapping = self.backward_mapping
        else:
            raise Exception("Invalid mode: enter either 'encrypt' or 'decrypt'")
        new_text = ""
        for char in text.upper():
            new_text += mapping.get(char, char)
        return new_text


def base10ToBase26(base10):
    """
    Converts a base-10 integer into a base-26 string
    :param base10: The base-10 representation of the key
    :type base10: int
    :return: The base-26 representation of the key
    :rtype: str
    """
    base10 = int(base10)
    base26 = ""
    for x in range(25, -1, -1):
        value = 26 ** x
        digit = BASE26_DIGITS[base10 // value]
        base10 = base10 % 26 ** x
        base26 += digit
    return base26


def base26ToBase10(base26):
    """
    Converts a base-26 string into a base-10 integer
    :param base26: The base-1 representation of the key
    :type base26: str
    :return: The base-10 representation of the key
    :rtype: int
    """
    base10 = 0
    for x in range(26):
        digit = BASE26_DIGITS.index(base26[-x - 1])
        value = 26 ** x
        base10 += digit * value
    return str(base10)


def invertDictionary(dictionary):
    """
    Swaps the keys and values in a dictionary
    :param dictionary: The initial dictionary
    :type dictionary: dict
    :return: The inverted dictionary
    :rtype: dict
    """
    return dict(zip(dictionary.values(), dictionary.keys()))


def generateRandomKey():
    """
    Generates a random key
    :return: The key for the letter mapping
    :rtype: Key
    """
    base26 = ""
    total = set()
    x = 0
    while len(base26) != 26:
        char_shift = choice(BASE26_DIGITS)
        # checks if the shift won't create duplicate letters
        if (BASE26_DIGITS.index(char_shift) + x) % 26 not in total:
            base26 += char_shift
            total.add((BASE26_DIGITS.index(char_shift) + x) % 26)
            x += 1
    key = Key(base26ToBase10(base26))
    return key


def generateKnownKey(mapped_letters):
    """
    Generates a key from a letter mapping
    :param mapped_letters:
    :type mapped_letters: list[str]
    :return: The key generated from the mapping
    :rtype: Key
    """
    if not validateMapping(mapped_letters):
        return
    base26 = ""
    for i in range(26):
        shift = (LETTERS.index(mapped_letters[i]) - i + 26) % 26
        digit = BASE26_DIGITS[shift]
        base26 += digit
    base10 = base26ToBase10(base26)
    return Key(base10)


def validateMapping(mapped_letters):
    """
    Checks if the mapping is valid
    :param mapped_letters: The letter mapping
    :type mapped_letters: list[str]
    :return: Boolean value for if the mapping is valid
    :rtype: bool
    """
    letter_set = set(LETTERS)
    mapping_set = set(mapped_letters)
    return letter_set == mapping_set


def testKey(key):
    """
    Tests if the key is valid
    :param key: the key to be tested
    :type key: Key
    :return: Boolean value for if the key is valid
    :rtype: bool
    """
    shift_check = True
    total = set()

    for i in range(26):
        shift = (BASE26_DIGITS.index(key.base26[i]) + i) % 26
        if shift in total:
            shift_check = False
        else:
            total.add(shift)

    return shift_check


LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

BASE26_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                 'K', 'L', 'M', 'N', 'O', 'P']

if __name__ == "__main__":
    print(example_key := generateRandomKey())
    print(cipher := example_key.mapLetters("Hello world"))
    print(example_key.mapLetters(cipher, "decrypt"))
