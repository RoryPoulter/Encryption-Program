# Encryption Program by Rory Poulter
# Encrypts and decrypts text and .txt files
# Last edited: 25/06/23

from tkinter import *
from tkinterdnd2 import *
from random import choice
import pyperclip


# File subroutines
def drop(event):
    if en_file_frame.winfo_ismapped():
        err_lab = en_err_lab
        file_lab = en_file_lab
        entry_sv = en_entry_sv
        confirm_but = en_confirm_but
    else:
        err_lab = de_err_lab
        file_lab = de_file_lab
        entry_sv = de_entry_sv
        confirm_but = de_confirm_but

    err_lab.config(text="")

    if ".txt" not in event.data:
        err_lab.config(text="Invalid file type: enter .txt file")
    else:
        confirm_but.config(state="normal")
        path = event.data.strip("{").strip("}")
        fileName = path.split("/")[-1]
        file_lab.config(text=fileName)

        entry_sv.set(path)


def encryptFile():
    filepath = en_entry.get()
    if filepath == "":
        return
    else:
        name = filepath.split("/")[-1][:-4]
        key = genKey()
        encoded_letters = genEncodedLetters(base10ToBase26(key))

        encodedName = encrypt(name.upper(), encoded_letters)

        with open(filepath, "r") as plainFile:
            encryptedFile = open(encodedName + ".txt", "w")
            encryptedFile.write(key)
            encryptedFile.write("\n")
            for line in plainFile:
                newLine = encrypt(line.upper(), encoded_letters)
                encryptedFile.write(newLine)
            encryptedFile.close()


def decryptFile():
    de_err_lab.config(text="")
    filepath = de_entry.get()
    name = filepath.split("/")[-1][:-4]
    with open(filepath, "r") as encryptedFile:
        lines = encryptedFile.readlines()
    key = lines[0]
    lines.pop(0)

    try:
        encoded_letters = genEncodedLetters(base10ToBase26(key))
    except ValueError:
        de_err_lab.config(text="Invalid key: 1st line must be a valid key ONLY")
    else:
        decryptedName = decrypt(name, encoded_letters)

        with open(decryptedName + ".txt", "w") as f:
            for line in lines:
                newLine = decrypt(line, encoded_letters)
                f.write(newLine)


# Base conversions
def base10ToBase26(base10):
    base10 = int(base10)
    base26 = ""
    for x in range(25, -1, -1):
        value = 26 ** x
        digit = shifts[base10 // value]
        base10 = base10 % 26 ** x
        base26 += digit
    return base26


def base26ToBase10(base26):
    base10 = 0
    for x in range(26):
        digit = shifts.index(base26[-x - 1])
        value = 26 ** x
        base10 += digit * value
    return str(base10)


# Copy subroutines
def copyPlainText():
    pyperclip.copy(decrypt_out.config("text")[-1])


def copyCipherText():
    pyperclip.copy(encrypt_out.config("text")[-1])


def copyKey():
    pyperclip.copy((key_out.config("text")[-1])[5:])


def encryptText():
    text = (encrypt_inp.get()).upper()
    encrypt_out.config(text="")
    key_out.config(text="")
    en_error_lab.config(text="")
    if toggle_key.config("text")[-1] == "Custom Key":
        key = genKey()
        key_out.config(text="Key: " + str(key))
    else:
        key = key_entry.get()
        if key == "":
            return

    key = base10ToBase26(key)

    valid_key = testKey(key)
    if valid_key:
        encoded_letters = genEncodedLetters(key)
        encoded_text = encrypt(text, encoded_letters)
        encrypt_out.config(text=encoded_text)

    else:
        en_error_lab.config(text="Error: Invalid key")


def encrypt(text, encoded_letters):
    encoded_text = ""
    for char in text:
        if char in letters:
            encoded_text += encoded_letters[letters.index(char)]
        else:
            encoded_text += char
    return encoded_text


def decryptText():
    text = (decrypt_inp.get()).upper()
    decrypt_out.config(text="")
    de_error_lab.config(text="")
    key = de_key_enter.get()
    if key == "":
        return
    key = base10ToBase26(key)

    valid_key = testKey(key)
    if valid_key:
        encoded_letters = genEncodedLetters(key)
        decoded_text = decrypt(text, encoded_letters)
        decrypt_out.config(text=decoded_text)
    else:
        de_error_lab.config(text="Error: Invalid key")


def decrypt(text, encoded_letters):
    decoded_text = ""
    for char in text:
        if char in encoded_letters:
            decoded_text += letters[encoded_letters.index(char)]
        else:
            decoded_text += char
    return decoded_text


def genKey():
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


def genEncodedLetters(key):
    encoded_letters = []
    for x in range(26):
        shift = shifts.index(key[x])
        place = (shift + x) % 26
        encoded_letters.append(letters[place])
    return encoded_letters


def checkKey():
    shifts_lab.config(text="Shifts: Invalid", fg=invalid)
    encoded_lab.config(text=letters)
    key = key_check_entry.get()
    if key == "":
        return
    key = base10ToBase26(key)

    shift_check = testKey(key)

    if shift_check:
        shifts_lab.config(text="Shifts: Valid", fg=valid)

        encoded_letters = genEncodedLetters(key)
        encoded_lab.config(text=encoded_letters)


def testKey(key):
    shift_check = True
    total = [27] * 26

    for x in range(26):
        shift = (shifts.index(key[x]) + x) % 26
        if shift in total:
            shift_check = False
        else:
            total[x] = shift

    return shift_check


def toggle():
    if toggle_key.config("text")[-1] == "Random Key":
        toggle_key.config(text="Custom Key")
        key_entry.config(state="disabled")
    else:
        toggle_key.config(text="Random Key")
        key_entry.config(state="normal")


def setupDecryptText():
    Label(de_frame, text="Decrypt Message", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(de_frame, text="Cipher Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    decrypt_inp.pack(pady=5)
    Label(de_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    de_key_enter.pack(pady=5)
    Button(de_frame, text="Decrypt", bg=emphasis, fg=text_col,
           font=(font, 12), command=decryptText, borderwidth=0, width=18).pack(pady=5)
    Label(de_frame, text="Plain Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    decrypt_out.pack(pady=5)
    de_error_lab.pack(pady=5)
    Button(de_frame, text="Copy Plain Text", bg=emphasis, fg=text_col,
           font=(font, 12), command=copyPlainText, borderwidth=0, width=18).pack(pady=5)


def setupEncryptText():
    Label(en_frame, text="Encrypt Message", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(en_frame, text="Plain Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_inp.pack(pady=5)
    Label(en_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    toggle_key.pack(pady=5)
    key_entry.pack(pady=5)
    Button(en_frame, text="Encrypt", bg=emphasis, fg=text_col, font=(font, 12), command=encryptText,
           borderwidth=0, width=18).pack(pady=5)
    Label(en_frame, text="Cipher Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_out.pack(pady=5)
    key_out.pack(pady=5)
    en_error_lab.pack(pady=5)
    Button(en_frame, text="Copy Cipher Text", bg=emphasis, fg=text_col, font=(font, 12), command=copyCipherText,
           borderwidth=0, width=18).pack(padx=35, side=RIGHT)
    Button(en_frame, text="Copy Key", bg=emphasis, fg=text_col, font=(font, 12), command=copyKey,
           borderwidth=0, width=18).pack(padx=35, side=LEFT)


def setupKeyCheck():
    Label(key_frame, text="Check Key Validity", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(key_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    key_check_entry.pack(pady=5)
    key_check_but.pack(pady=5)
    shifts_lab.pack(pady=5)
    letters_lab.pack(pady=5)
    encoded_lab.pack(pady=5)


def setupEncryptFile():
    Label(en_file_frame, text="Encrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(en_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    en_entry.place(height=250, width=250, x=200, y=115)
    en_file_lab.place(x=325, y=400, anchor=CENTER)
    en_err_lab.place(x=325, y=430, anchor=CENTER)
    en_confirm_but.place(x=325, y=465, anchor=CENTER)


def setupDecryptFile():
    Label(de_file_frame, text="Decrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(de_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    de_entry.place(height=250, width=250, x=200, y=115)
    de_file_lab.place(x=325, y=400, anchor=CENTER)
    de_err_lab.place(x=325, y=430, anchor=CENTER)
    de_confirm_but.place(x=325, y=465, anchor=CENTER)


def loadDecryptText():
    key_frame.place_forget()
    en_frame.place_forget()
    en_file_frame.place_forget()
    de_file_frame.place_forget()
    de_frame.place(x=350, y=50, width=650, height=600)


def loadEncryptText():
    key_frame.place_forget()
    de_frame.place_forget()
    en_file_frame.place_forget()
    de_file_frame.place_forget()
    en_frame.place(x=350, y=50, width=650, height=600)


def loadKeyCheck():
    de_frame.place_forget()
    en_frame.place_forget()
    en_file_frame.place_forget()
    de_file_frame.place_forget()
    key_frame.place(x=350, y=50, width=650, height=600)


def loadEncryptFile():
    de_frame.place_forget()
    en_frame.place_forget()
    key_frame.place_forget()
    de_file_frame.place_forget()
    en_file_frame.place(x=350, y=50, width=650, height=600)


def loadDecryptFile():
    de_frame.place_forget()
    en_frame.place_forget()
    key_frame.place_forget()
    en_file_frame.place_forget()
    de_file_frame.place(x=350, y=50, width=650, height=600)


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

shifts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
          'M', 'N', 'O', 'P']

# Style variables
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

de_but = Button(menu_frame, text="Decrypt text", bg=emphasis, fg=text_col, font=(font, 12, "bold"),
                command=loadDecryptText, width=15, height=1, borderwidth=0, anchor="w")

en_but = Button(menu_frame, text="Encrypt text", bg=emphasis, fg=text_col, font=(font, 12, "bold"),
                command=loadEncryptText, width=15, height=1, borderwidth=0, anchor="w")

key_but = Button(menu_frame, text="Check key", bg=emphasis, fg=text_col, font=(font, 12, "bold"),
                 command=loadKeyCheck, width=15, height=1, borderwidth=0, anchor="w")

en_file_but = Button(menu_frame, text="Encrypt file", bg=emphasis, fg=text_col, font=(font, 12, "bold"),
                     width=15, height=1, borderwidth=0, command=loadEncryptFile, anchor="w")

de_file_but = Button(menu_frame, text="Decrypt file", bg=emphasis, fg=text_col, font=(font, 12, "bold"),
                     width=15, height=1, borderwidth=0, command=loadDecryptFile, anchor="w")

menu_widgets = (de_but, en_but, key_but, en_file_but, de_file_but)

de_frame = Frame(window, bg=bg)
en_frame = Frame(window, bg=bg)
key_frame = Frame(window, bg=bg)
en_file_frame = Frame(window, bg=bg)
de_file_frame = Frame(window, bg=bg)

# Decrypt Widgets
decrypt_inp = Entry(de_frame, font=(font, 12), bg=bg2, fg=text_col, borderwidth=0)
de_key_enter = Entry(de_frame, font=(font, 12), bg=bg2, fg=text_col, width=38, borderwidth=0)
decrypt_out = Label(de_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))
de_error_lab = Label(de_frame, font=(font, 12, "bold"), bg=bg, fg=emphasis)

# Encrypt Widgets
encrypt_inp = Entry(en_frame, font=(font, 12), bg=bg2, fg=text_col, borderwidth=0)
toggle_key = Button(en_frame, text="Random Key", bg=emphasis, fg=text_col, font=(font, 12), command=toggle,
                    borderwidth=0, width=18)
key_entry = Entry(en_frame, font=(font, 12), bg=bg2, fg=text_col, width=38, borderwidth=0)
encrypt_out = Label(en_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))
key_out = Label(en_frame, bg=bg, fg=text_col, font=(font, 16))
en_error_lab = Label(en_frame, font=(font, 12, "bold"), bg=bg, fg=emphasis)

# Key Widgets
key_check_entry = Entry(key_frame, font=(font, 12), bg=bg2, fg=text_col, width=38, borderwidth=0)
key_check_but = Button(key_frame, text="Check Key", bg=emphasis, fg=text_col, command=checkKey, font=(font, 12),
                       borderwidth=0, width=18)
shifts_lab = Label(key_frame, text="Shifts: Invalid", bg=bg, fg=invalid, font=(font, 12))
letters_lab = Label(key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))
encoded_lab = Label(key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))

# Encrypt File Widgets
en_entry_sv = StringVar()
en_entry = Entry(en_file_frame, text=en_entry_sv, width=25, font=(font, 14), disabledbackground="#161616",
                 disabledforeground="#161616", state="disabled")

en_file_lab = Label(en_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

en_err_lab = Label(en_file_frame, bg="#222222", fg="#AA0000", font=(font, 14, "bold"))

en_confirm_but = Button(en_file_frame, text="Encrypt File", bg="#AA0000", fg="#FFFFFF", borderwidth=0,
                        width=15, font=(font, 14), command=encryptFile, state="disabled", disabledforeground=text_col)

en_entry.drop_target_register(DND_FILES)
en_entry.dnd_bind('<<Drop>>', drop)

# Decrypt File Widgets
de_entry_sv = StringVar()
de_entry = Entry(de_file_frame, text=de_entry_sv, width=25, font=(font, 14), disabledbackground="#161616",
                 disabledforeground="#161616", state="disabled")

de_file_lab = Label(de_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

de_err_lab = Label(de_file_frame, bg="#222222", fg="#AA0000", font=(font, 14, "bold"))

de_confirm_but = Button(de_file_frame, text="Decrypt File", bg="#AA0000", fg="#FFFFFF", borderwidth=0,
                        width=15, font=(font, 14), command=decryptFile, disabledforeground=text_col, state="disabled")

de_entry.drop_target_register(DND_FILES)
de_entry.dnd_bind('<<Drop>>', drop)

setupDecryptText()
setupEncryptText()
setupKeyCheck()
setupEncryptFile()
setupDecryptFile()

menu_frame.place(x=0, y=0, width=150, height=700)

for wid in menu_widgets:
    wid.pack(anchor="e", padx=5, pady=20)

Label(text="R. Poulter v1.4", bg=bg2, fg=bg, font=(font, 10)).place(x=0, y=677)

window.mainloop()
