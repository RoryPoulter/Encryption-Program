# Encryption Program by Rory Poulter
# Encrypts and decrypts text and .txt files
# Last edited: 25/06/23

from tkinter import *
from tkinterdnd2 import *
from random import choice
import pyperclip


class CustomButton(Button):
    def __init__(self, master, hover_background, hover_foreground, *args, **kwargs):
        """
        Button subclass which changes colours when cursor hovers over it
        :param hover_background: Background colour when cursor is above button
        :type hover_background: str
        :param hover_foreground: Foreground colour when cursor is above button
        :type hover_foreground: str
        """
        Button.__init__(self, master, *args, **kwargs)
        self["borderwidth"] = 0  # Sets the border width to 0
        self.hover_bg = hover_background
        self.hover_fg = hover_foreground
        self.bg = self["bg"]
        self.fg = self["fg"]
        self.bind("<Enter>", self.on_enter)  # Binds the method on_enter when cursor enters label
        self.bind("<Leave>", self.on_leave)  # Binds the method on_leave when cursor leaves label

    def on_enter(self, e):
        """
        Changes the colour of the button when hovered over
        """
        self.config(bg=self.hover_bg, fg=self.hover_fg)  # Changes the colour

    def on_leave(self, e):
        """
        Changes colour back to original when cursor leaves
        """
        self.config(bg=self.bg, fg=self.fg)  # Changes the colour


# File subroutines
def drop(event):
    """
    Finds the file name
    """
    if encrypt_file_frame.winfo_ismapped():
        err_lab = en_err_lab
        file_name_label = encrypt_file_name_label
        entry_sv = en_entry_sv
        confirm_button = encrypt_file_confirm_button
    else:
        err_lab = de_err_lab
        file_name_label = decrypt_file_name_label
        entry_sv = de_entry_sv
        confirm_button = decrypt_file_confirm_button

    err_lab.config(text="")

    if ".txt" not in event.data:
        err_lab.config(text="Invalid file type: enter .txt file")
    else:
        confirm_button.config(state="normal")
        path = event.data.strip("{").strip("}")
        fileName = path.split("/")[-1]
        file_name_label.config(text=fileName)

        entry_sv.set(path)


def encryptFile():
    """
    Encrypts the text and name of the .txt file as a separate file
    """
    path = encrypt_file_entry.get()
    if path == "":
        return
    else:
        file_name = path.split("/")[-1][:-4]
        key = generateKey()
        encoded_letters = generateEncryptedLetters(base10ToBase26(key))

        encoded_file_name = encrypt(file_name.upper(), encoded_letters)

        with open(path, "r") as file:
            encrypted_file = open(encoded_file_name + ".txt", "w")
            encrypted_file.write(key)
            encrypted_file.write("\n")
            for line in file:
                encrypted_line = encrypt(line.upper(), encoded_letters)
                encrypted_file.write(encrypted_line)
            encrypted_file.close()


def decryptFile():
    """
    Decrypts the text and name of the .txt file as a separate file
    """
    de_err_lab.config(text="")
    path = decrypt_file_entry.get()
    file_name = path.split("/")[-1][:-4]
    with open(path, "r") as encrypted_file:
        lines = encrypted_file.readlines()
    key = lines[0]
    lines.pop(0)

    try:
        encoded_letters = generateEncryptedLetters(base10ToBase26(key))
    except ValueError:
        de_err_lab.config(text="Invalid key: 1st line must be a valid key ONLY")
    else:
        decrypted_file_name = decrypt(file_name, encoded_letters)

        with open(decrypted_file_name + ".txt", "w") as decrypted_file:
            for line in lines:
                decrypted_line = decrypt(line, encoded_letters)
                decrypted_file.write(decrypted_line)


# Base conversions
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
        digit = shifts[base10 // value]
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
        digit = shifts.index(base26[-x - 1])
        value = 26 ** x
        base10 += digit * value
    return str(base10)


# Copy subroutines
def copyPlainText():
    """
    Saves the plain text result to the clipboard
    """
    pyperclip.copy(decrypt_output.config("text")[-1])


def copyCipherText():
    """
    Saves the cipher text result to the clipboard
    """
    pyperclip.copy(encrypt_output.config("text")[-1])


def copyKey():
    """
    Saves the key to the clipboard
    """
    pyperclip.copy((encrypt_key_output.config("text")[-1])[5:])


def encryptText():
    """
    Encrypts the text input using the key or a random key
    """
    text = (encrypt_text_entry.get()).upper()
    encrypt_output.config(text="")
    encrypt_key_output.config(text="")
    en_error_lab.config(text="")
    if toggle_random_key_button.config("text")[-1] == "Custom Key":
        key = generateKey()
        encrypt_key_output.config(text="Key: " + str(key))
    else:
        key = encrypt_key_entry.get()
        if key == "":
            return

    key = base10ToBase26(key)

    valid_key = testKey(key)
    if valid_key:
        encrypted_letters = generateEncryptedLetters(key)
        encrypted_text = encrypt(text, encrypted_letters)
        encrypt_output.config(text=encrypted_text)

    else:
        en_error_lab.config(text="Error: Invalid key")


def encrypt(decrypted_text, letter_mapping):
    """
    Encrypts the text using the letter mapping
    :param decrypted_text: The decrypted text
    :type decrypted_text: str
    :param letter_mapping: The letter mapping
    :type letter_mapping: list[str]
    :return: The encrypted text
    :rtype: str
    """
    encrypted_text = ""
    for char in decrypted_text:
        if char in letters:
            encrypted_text += letter_mapping[letters.index(char)]
        else:
            encrypted_text += char
    return encrypted_text


def decryptText():
    """
    Decrypts the text input using the key
    """
    text = (decrypt_text_entry.get()).upper()
    decrypt_output.config(text="")
    de_error_lab.config(text="")
    key = decrypt_key_entry.get()
    if key == "":
        return
    key = base10ToBase26(key)

    valid_key = testKey(key)
    if valid_key:
        encrypted_letters = generateEncryptedLetters(key)
        decrypted_text = decrypt(text, encrypted_letters)
        decrypt_output.config(text=decrypted_text)
    else:
        de_error_lab.config(text="Error: Invalid key")


def decrypt(encrypted_text, letter_mapping):
    """
    Encrypts the text using the letter mapping
    :param encrypted_text: The encrypted text
    :type encrypted_text: str
    :param letter_mapping: The letter mapping
    :type letter_mapping: list[str]
    :return: The decrypted text
    :rtype: str
    """
    decrypted_text = ""
    for char in encrypted_text:
        if char in letter_mapping:
            decrypted_text += letters[letter_mapping.index(char)]
        else:
            decrypted_text += char
    return decrypted_text


def generateKey():
    """
    Generates a random key
    :return: The key for the letter mapping
    :rtype: int
    """
    key = ""
    total = [27] * 26
    x = 0
    while len(key) != 26:
        char_shift = choice(shifts)
        # checks if the shift won't create duplicate letters
        if (shifts.index(char_shift) + x) % 26 not in total:
            key += char_shift
            total[x] = (shifts.index(char_shift) + x) % 26
            x += 1
    key = base26ToBase10(key)
    return key


def generateEncryptedLetters(base26_key):
    """
    Generates the letter mapping from the key
    :param base26_key: The base-26 representation of the key
    :type base26_key: str
    :return: The letter mapping
    :rtype: list[str]
    """
    letter_mapping = []
    for x in range(26):
        shift = shifts.index(base26_key[x])
        place = (shift + x) % 26
        letter_mapping.append(letters[place])
    return letter_mapping


def checkKey():
    """
    Checks if the key is valid and updates display
    """
    shifts_label.config(text="Shifts: Invalid", fg=invalid)
    mapped_letters_label.config(text=letters)
    key = key_check_entry.get()
    if key == "":
        return
    key = base10ToBase26(key)

    shift_check = testKey(key)

    if shift_check:
        shifts_label.config(text="Shifts: Valid", fg=valid)

        encoded_letters = generateEncryptedLetters(key)
        mapped_letters_label.config(text=encoded_letters)


def testKey(base26_key):
    """
    Tests if the key is valid
    :param base26_key: the base-26 representation of the key
    :type base26_key: str
    :return: Boolean value for if the key is valid
    :rtype: bool
    """
    shift_check = True
    total = [27] * 26

    for x in range(26):
        shift = (shifts.index(base26_key[x]) + x) % 26
        if shift in total:
            shift_check = False
        else:
            total[x] = shift

    return shift_check


def toggleRandomKey():
    """
    Toggles whether a random key is to be generated
    """
    if toggle_random_key_button.config("text")[-1] == "Random Key":
        toggle_random_key_button.config(text="Custom Key")
        encrypt_key_entry.config(state="disabled")
    else:
        toggle_random_key_button.config(text="Random Key")
        encrypt_key_entry.config(state="normal")


def setupFrameDecryptText():
    """
    Sets up the frame for decrypting text
    """
    Label(decrypt_text_frame, text="Decrypt Message", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(decrypt_text_frame, text="Cipher Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    decrypt_text_entry.pack(pady=5)
    Label(decrypt_text_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    decrypt_key_entry.pack(pady=5)
    CustomButton(decrypt_text_frame, **styles["button"], text="Decrypt", command=decryptText, width=18).pack(pady=5)
    Label(decrypt_text_frame, text="Plain Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    decrypt_output.pack(pady=5)
    de_error_lab.pack(pady=5)
    CustomButton(decrypt_text_frame, **styles["button"], text="Copy Plain Text", command=copyPlainText, width=18).pack(pady=5)


def setupFrameEncryptText():
    """
    Sets up the frame for encrypting text
    """
    Label(encrypt_text_frame, text="Encrypt Message", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(encrypt_text_frame, text="Plain Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_text_entry.pack(pady=5)
    Label(encrypt_text_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    toggle_random_key_button.pack(pady=5)
    encrypt_key_entry.pack(pady=5)
    CustomButton(encrypt_text_frame, **styles["button"], text="Encrypt", command=encryptText, width=18).pack(pady=5)
    Label(encrypt_text_frame, text="Cipher Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_output.pack(pady=5)
    encrypt_key_output.pack(pady=5)
    en_error_lab.pack(pady=5)
    CustomButton(encrypt_text_frame, **styles["button"], text="Copy Cipher Text", command=copyCipherText,
                 width=18).pack(padx=35, side=RIGHT)
    CustomButton(encrypt_text_frame, **styles["button"], text="Copy Key", command=copyKey, width=18).pack(padx=35, side=LEFT)


def setupFrameKeyCheck():
    """
    Sets up the frame for checking keys
    """
    Label(key_frame, text="Check Key Validity", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(key_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    key_check_entry.pack(pady=5)
    key_check_but.pack(pady=5)
    shifts_label.pack(pady=5)
    letters_label.pack(pady=5)
    mapped_letters_label.pack(pady=5)


def setupFrameEncryptFile():
    """
    Sets up the frame for encrypting files
    """
    Label(encrypt_file_frame, text="Encrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(encrypt_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    encrypt_file_entry.place(height=250, width=250, x=200, y=115)
    encrypt_file_name_label.place(x=325, y=400, anchor=CENTER)
    en_err_lab.place(x=325, y=430, anchor=CENTER)
    encrypt_file_confirm_button.place(x=325, y=465, anchor=CENTER)


def setupFrameDecryptFile():
    """
    Sets up the frame for encrypting files
    """
    Label(decrypt_file_frame, text="Decrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(decrypt_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    decrypt_file_entry.place(height=250, width=250, x=200, y=115)
    decrypt_file_name_label.place(x=325, y=400, anchor=CENTER)
    de_err_lab.place(x=325, y=430, anchor=CENTER)
    decrypt_file_confirm_button.place(x=325, y=465, anchor=CENTER)


def loadFrameDecryptText():
    """
    Loads the frame for decrypting text
    """
    key_frame.place_forget()
    encrypt_text_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place_forget()
    decrypt_text_frame.place(x=350, y=50, width=650, height=600)


def loadFrameEncryptText():
    """
    Loads the frame for encrypting text
    """
    key_frame.place_forget()
    decrypt_text_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place_forget()
    encrypt_text_frame.place(x=350, y=50, width=650, height=600)


def loadFrameKeyCheck():
    """
    Loads the frame for checking keys
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place_forget()
    key_frame.place(x=350, y=50, width=650, height=600)


def loadFrameEncryptFile():
    """
    Loads the frame for encrypting files
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    key_frame.place_forget()
    decrypt_file_frame.place_forget()
    encrypt_file_frame.place(x=350, y=50, width=650, height=600)


def loadFrameDecryptFile():
    """
    Loads the frame for decrypting files
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    key_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place(x=350, y=50, width=650, height=600)


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

shifts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
          'M', 'N', 'O', 'P']

# Style variables
styles = {
    "side button": {
        "bg": "#AA0000",
        "fg": "#FFFFFF",
        "font": ("verdana", 12, "bold"),
        "hover_background": "#770000",
        "hover_foreground": "#FFFFFF",
        "width": 15,
        "anchor": "w"
    },
    "button": {
        "bg": "#AA0000",
        "fg": "#FFFFFF",
        "font": ("verdana", 12),
        "hover_background": "#770000",
        "hover_foreground": "#FFFFFF",
    },
    "entry": {
        "bg": "#161616",
        "font": ("verdana", 12),
        "borderwidth": 0,
        "fg": "#FFFFFF"
    },
    "file entry": {
        "width": 25,
        "bg": "#161616",
        "font": ("Verdana", 14),
        "disabledbackground": "#161616",
        "disabledforeground": "#161616"
    }
}

bg = "#222222"
bg2 = "#161616"
text_col = "#FFFFFF"
emphasis = "#AA0000"
invalid = "#AA0000"
valid = "#00AA00"
font = "verdana"

window = TkinterDnD.Tk()
window.title("Encryption Program")
window.geometry("1200x700")
window.config(bg=bg)
window.resizable(False, False)

# Widgets

# Main menu

menu_frame = Frame(window, bg=bg2)
menu_frame.config(width=150, height=600)

img = "lock2.png"
image = PhotoImage(file=img)
Label(menu_frame, image=image, bg=bg2, borderwidth=0).pack(pady=5)

menu_decrypt_text_button = CustomButton(menu_frame, **styles["side button"], text="Decrypt text", command=loadFrameDecryptText)
menu_encrypt_text_button = CustomButton(menu_frame, **styles["side button"], text="Encrypt text", command=loadFrameEncryptText)
menu_key_button = CustomButton(menu_frame, **styles["side button"], text="Check key", command=loadFrameKeyCheck)
menu_encrypt_file_button = CustomButton(menu_frame, **styles["side button"], text="Encrypt file", command=loadFrameEncryptFile)
menu_decrypt_file_button = CustomButton(menu_frame, **styles["side button"], text="Decrypt file", command=loadFrameDecryptFile)

menu_widgets = (menu_decrypt_text_button, menu_encrypt_text_button, menu_key_button, menu_encrypt_file_button, menu_decrypt_file_button)

decrypt_text_frame = Frame(window, bg=bg)
encrypt_text_frame = Frame(window, bg=bg)
key_frame = Frame(window, bg=bg)
encrypt_file_frame = Frame(window, bg=bg)
decrypt_file_frame = Frame(window, bg=bg)

# Decrypt Widgets
decrypt_text_entry = Entry(decrypt_text_frame, **styles["entry"])
decrypt_key_entry = Entry(decrypt_text_frame, **styles["entry"], width=38)
decrypt_output = Label(decrypt_text_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))
de_error_lab = Label(decrypt_text_frame, font=(font, 12, "bold"), bg=bg, fg=emphasis)

# Encrypt Widgets
encrypt_text_entry = Entry(encrypt_text_frame, **styles["entry"])
toggle_random_key_button = CustomButton(encrypt_text_frame, **styles["button"], text="Random Key", command=toggleRandomKey, width=18)
encrypt_key_entry = Entry(encrypt_text_frame, **styles["entry"], width=38)
encrypt_output = Label(encrypt_text_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))
encrypt_key_output = Label(encrypt_text_frame, bg=bg, fg=text_col, font=(font, 16))
en_error_lab = Label(encrypt_text_frame, font=(font, 12, "bold"), bg=bg, fg=emphasis)

# Key Widgets
key_check_entry = Entry(key_frame, **styles["entry"], width=38)
key_check_but = CustomButton(key_frame, **styles["button"], text="Check Key", command=checkKey, width=18)
shifts_label = Label(key_frame, text="Shifts: Invalid", bg=bg, fg=invalid, font=(font, 12))
letters_label = Label(key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))
mapped_letters_label = Label(key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))

# Encrypt File Widgets
en_entry_sv = StringVar()
encrypt_file_entry = Entry(encrypt_file_frame, text=en_entry_sv, width=25, font=(font, 14), disabledbackground="#161616",
                           disabledforeground="#161616", state="disabled")

encrypt_file_name_label = Label(encrypt_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

en_err_lab = Label(encrypt_file_frame, bg="#222222", fg="#AA0000", font=(font, 14, "bold"))

encrypt_file_confirm_button = CustomButton(encrypt_file_frame, **styles["button"], text="Encrypt File", width=15, command=encryptFile,
                                           state="disabled", disabledforeground=text_col)

encrypt_file_entry.drop_target_register(DND_FILES)
encrypt_file_entry.dnd_bind('<<Drop>>', drop)

# Decrypt File Widgets
de_entry_sv = StringVar()
decrypt_file_entry = Entry(decrypt_file_frame, text=de_entry_sv, width=25, font=(font, 14), disabledbackground="#161616",
                           disabledforeground="#161616", state="disabled")

decrypt_file_name_label = Label(decrypt_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

de_err_lab = Label(decrypt_file_frame, bg="#222222", fg="#AA0000", font=(font, 14, "bold"))

decrypt_file_confirm_button = CustomButton(decrypt_file_frame, **styles["button"], text="Decrypt File", width=15, command=decryptFile,
                                           disabledforeground=text_col, state="disabled")

decrypt_file_entry.drop_target_register(DND_FILES)
decrypt_file_entry.dnd_bind('<<Drop>>', drop)

setupFrameDecryptText()
setupFrameEncryptText()
setupFrameKeyCheck()
setupFrameEncryptFile()
setupFrameDecryptFile()

menu_frame.place(x=0, y=0, width=150, height=700)

for wid in menu_widgets:
    wid.pack(anchor="e", padx=5, pady=20)

Label(text="R. Poulter v1.1", bg=bg2, fg=bg, font=(font, 10)).place(x=0, y=677)

window.mainloop()
