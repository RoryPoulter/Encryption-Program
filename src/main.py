# Encryption Program by Rory Poulter
# Encrypts and decrypts text and .txt files
# Last edited: 29/01/24

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinterdnd2 import *
import pyperclip
import encryption
import os


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
def browseFiles():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"),
                                                                                             ("all files",  "*.*")))
    file_name = file_path.split("/")[-1]
    print(file_name)
    if ".txt" not in file_name and file_name:
        messagebox.showerror("Error", "Unsupported file type: make sure file is a .txt file")
        return

    if encrypt_file_frame.winfo_ismapped():
        en_entry_sv.set(file_path)
        encrypt_file_name_label.config(text=file_name)
    else:
        de_entry_sv.set(file_path)
        decrypt_file_name_label.config(text=file_name)


def drop(event):
    """
    Finds the file name
    """
    if encrypt_file_frame.winfo_ismapped():
        file_name_label = encrypt_file_name_label
        entry_sv = en_entry_sv
    else:
        file_name_label = decrypt_file_name_label
        entry_sv = de_entry_sv

    if ".txt" not in event.data:
        messagebox.showerror("Error", "Invalid file type: enter .txt file")
    else:
        path = event.data.strip("{").strip("}")
        fileName = path.split("/")[-1]
        file_name_label.config(text=fileName)

        entry_sv.set(path)


def encryptFile():
    """
    Encrypts the text and name of the .txt file as a separate file
    """
    path = en_entry_sv.get()
    if path == "":
        messagebox.showerror("Error", "No file selected")
        return
    else:
        file_name = path.split("/")[-1][:-4]
        key = encrypt_file_key_entry.get()
        if key == "":
            messagebox.showerror("Error", "Key field empty")
            return
        elif not key.isnumeric():
            messagebox.showerror("Error", "Invalid input: key must be a number")
            return

        key = encryption.Key(key)
        valid_key = encryption.testKey(key)
        if valid_key:
            encoded_file_name = key.mapLetters(file_name.upper(), "encrypt")

            with open(path, "r") as file:
                encrypted_file_path = os.path.dirname(__file__)
                encrypted_file = open(os.path.join(encrypted_file_path, "Encrypted and decrypted files/" + encoded_file_name + ".txt"), "w")
                encrypted_file.write(str(key))
                encrypted_file.write("\n")
                for line in file:
                    encrypted_line = key.mapLetters(line.upper(), "encrypt")
                    encrypted_file.write(encrypted_line)
                encrypted_file.close()
            messagebox.showinfo("Success!", "File successfully encrypted")
        else:
            messagebox.showerror("Error", "Invalid key")


def decryptFile():
    """
    Decrypts the text and name of the .txt file as a separate file
    """
    path = de_entry_sv.get()
    if path == "":
        messagebox.showerror("Error", "No file selected")
        return
    file_name = path.split("/")[-1][:-4]
    with open(path, "r") as encrypted_file:
        lines = encrypted_file.readlines()
    base10 = lines[0]
    lines.pop(0)

    try:
        key = encryption.Key(base10)
    except ValueError:
        messagebox.showerror("Error", "Invalid key: 1st line must be a valid key ONLY")
    else:
        decrypted_file_name = key.mapLetters(file_name, "decrypt")

        decrypted_file_path = os.path.dirname(__file__)
        with open(os.path.join(decrypted_file_path, "Encrypted and decrypted files/" + decrypted_file_name + ".txt"), "w") as decrypted_file:
            for line in lines:
                decrypted_line = key.mapLetters(line, "decrypt")
                decrypted_file.write(decrypted_line)
        messagebox.showinfo("Success!", "File successfully decrypted")


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


def copyRandomKey():
    """
    Saves the random key to the clipboard
    """
    pyperclip.copy(random_key_label.config("text")[-1])


def copyKnownKey():
    """
    Saves the known key to the clipboard
    """
    pyperclip.copy(key_label.config("text")[-1])


def encryptText():
    """
    Encrypts the text input using the key or a random key
    """
    text = (encrypt_text_entry.get()).upper()
    encrypt_output.config(text="")
    key = encrypt_key_entry.get()
    if key == "":
        messagebox.showerror("Error", "Key field empty")
        return
    elif not key.isnumeric():
        messagebox.showerror("Error", "Invalid input: key must be a number")
        return

    key = encryption.Key(key)

    valid_key = encryption.testKey(key)
    if valid_key:
        encrypted_text = key.mapLetters(text, "encrypt")
        encrypt_output.config(text=encrypted_text)

    else:
        messagebox.showerror("Error", "Invalid key")


def decryptText():
    """
    Decrypts the text input using the key
    """
    text = (decrypt_text_entry.get()).upper()
    decrypt_output.config(text="")
    key = decrypt_key_entry.get()
    if key == "":
        messagebox.showerror("Error", "Key field empty")
        return
    elif not key.isnumeric():
        messagebox.showerror("Error", "Invalid input: key must be a number")
        return
    key = encryption.Key(key)

    valid_key = encryption.testKey(key)
    if valid_key:
        decrypted_text = key.mapLetters(text, "decrypt")
        decrypt_output.config(text=decrypted_text)
    else:
        messagebox.showerror("Error", "Invalid key")


def checkKey():
    """
    Checks if the key is valid and updates display
    """
    mapped_letters_label.config(text=letters)
    key = key_check_entry.get()
    if key == "":
        messagebox.showerror("Error", "Key field empty")
        return
    elif not key.isnumeric():
        messagebox.showerror("Error", "Invalid input: key must be a number")
        return
    try:
        key = encryption.Key(key)
    except ValueError:
        messagebox.showerror("Error", "Invalid key")
    else:
        mapped_letters = list(key.forward_mapping.values())
        mapped_letters_label.config(text=mapped_letters)


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

    CustomButton(decrypt_text_frame, **styles["button"], text="Copy Plain Text", command=copyPlainText, width=18).pack(pady=5)


def setupFrameEncryptText():
    """
    Sets up the frame for encrypting text
    """
    Label(encrypt_text_frame, text="Encrypt Message", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(encrypt_text_frame, text="Plain Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_text_entry.pack(pady=5)
    Label(encrypt_text_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_key_entry.pack(pady=5)
    CustomButton(encrypt_text_frame, **styles["button"], text="Encrypt", command=encryptText, width=18).pack(pady=5)
    Label(encrypt_text_frame, text="Cipher Text:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    encrypt_output.pack(pady=5)
    CustomButton(encrypt_text_frame, **styles["button"], text="Copy Cipher Text", command=copyCipherText,
                 width=18).pack(padx=35)


def setupFrameKeyCheck():
    """
    Sets up the frame for checking keys
    """
    Label(random_key_frame, text="Check Key Validity", bg=bg, fg=emphasis, font=(font, 18, "bold")).pack(pady=10)
    Label(random_key_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).pack(pady=5)
    key_check_entry.pack(pady=5)
    key_check_but.pack(pady=5)
    letters_label.pack(pady=5)
    mapped_letters_label.pack(pady=5)


def setupFrameEncryptFile():
    """
    Sets up the frame for encrypting files
    """
    Label(encrypt_file_frame, text="Encrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(encrypt_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    encrypt_file_entry.place(height=250, width=250, x=200, y=115)
    CustomButton(encrypt_file_frame, **styles["button"], text="Select File", command=browseFiles).place(x=325, y=400,
                                                                                                        anchor=CENTER)
    encrypt_file_name_label.place(x=325, y=450, anchor=CENTER)
    Label(encrypt_file_frame, text="Key:", bg=bg, fg=text_col, font=(font, 12)).place(x=325, y=500, anchor=CENTER)
    encrypt_file_key_entry.place(x=325, y=530, anchor=CENTER)
    encrypt_file_confirm_button.place(x=325, y=570, anchor=CENTER)


def setupFrameDecryptFile():
    """
    Sets up the frame for encrypting files
    """
    Label(decrypt_file_frame, text="Decrypt File", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(decrypt_file_frame, text="Drop file:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    decrypt_file_entry.place(height=250, width=250, x=200, y=115)
    CustomButton(decrypt_file_frame, **styles["button"], text="Select File", command=browseFiles).place(x=325, y=400,
                                                                                                        anchor=CENTER)
    decrypt_file_name_label.place(x=325, y=450, anchor=CENTER)
    decrypt_file_confirm_button.place(x=325, y=515, anchor=CENTER)


def setupFrameGenerateKey():
    """
    Sets up the frame for generating keys from mappings
    """
    Label(known_key_frame, text="Generate Key", bg="#222222", fg="#AA0000", font=(font, 18, "bold")).pack(pady=15)
    Label(known_key_frame, text="Mapping:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack()
    generate_key_entry.pack(pady=15)
    generate_known_key_button.pack()
    key_label.pack(pady=15)
    CustomButton(known_key_frame, **styles["button"], text="Copy Key", command=copyKnownKey).pack()
    Label(known_key_frame, text="Random:", bg="#222222", fg="#FFFFFF", font=(font, 14)).pack(pady=15)
    generate_random_key_button.pack()
    random_key_label.pack(pady=15)
    CustomButton(known_key_frame, **styles["button"], text="Copy Key", command=copyRandomKey).pack()


def loadFrameDecryptText():
    """
    Loads the frame for decrypting text
    """
    random_key_frame.place_forget()
    known_key_frame.place_forget()
    encrypt_text_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place_forget()
    decrypt_text_frame.place(x=350, y=50, width=650, height=600)


def loadFrameEncryptText():
    """
    Loads the frame for encrypting text
    """
    random_key_frame.place_forget()
    known_key_frame.place_forget()
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
    known_key_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place_forget()
    random_key_frame.place(x=350, y=50, width=650, height=600)


def loadFrameEncryptFile():
    """
    Loads the frame for encrypting files
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    random_key_frame.place_forget()
    known_key_frame.place_forget()
    decrypt_file_frame.place_forget()
    encrypt_file_frame.place(x=350, y=50, width=650, height=600)


def loadFrameDecryptFile():
    """
    Loads the frame for decrypting files
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    random_key_frame.place_forget()
    known_key_frame.place_forget()
    encrypt_file_frame.place_forget()
    decrypt_file_frame.place(x=350, y=50, width=650, height=600)


def loadFrameGenerateKey():
    """
    Loads the frame for generating keys from mapping
    """
    decrypt_text_frame.place_forget()
    encrypt_text_frame.place_forget()
    random_key_frame.place_forget()
    decrypt_file_frame.place_forget()
    encrypt_file_frame.place_forget()
    known_key_frame.place(x=350, y=50, width=650, height=600)


def generateKnownKey():
    """
    Displays the mapped key to the window
    """
    mapped_letters = generate_key_entry.get().split(",")
    if not encryption.validateMapping(mapped_letters):
        messagebox.showerror("Error", "Invalid mapping")
        return
    else:
        key = encryption.generateKnownKey(mapped_letters)
        key_label.config(text=key)


def generateRandomKey():
    """
    Displays the random key to the window
    """
    key = encryption.generateRandomKey()
    random_key_label.config(text=key)


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

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

if not os.path.exists("./Encrypted and decrypted files"):
    os.mkdir("./Encrypted and decrypted files")

bg = "#222222"
bg2 = "#161616"
text_col = "#FFFFFF"
emphasis = "#AA0000"
invalid = "#AA0000"
valid = "#00AA00"
font = "verdana"

window = TkinterDnD.Tk()
window.title("Encryption Program")
window.geometry("1200x675")
window.config(bg=bg)
window.resizable(False, False)

# Widgets

# Main menu

menu_frame = Frame(window, bg=bg2)
menu_frame.config(width=150, height=600)

filepath = os.path.dirname(__file__)
image = PhotoImage(file=os.path.join(filepath, "lock.png"))
Label(menu_frame, image=image, bg=bg2, borderwidth=0).pack(pady=5)

menu_decrypt_text_button = CustomButton(menu_frame, **styles["side button"], text="Decrypt text", command=loadFrameDecryptText)
menu_encrypt_text_button = CustomButton(menu_frame, **styles["side button"], text="Encrypt text", command=loadFrameEncryptText)
menu_random_key_button = CustomButton(menu_frame, **styles["side button"], text="Check key", command=loadFrameKeyCheck)
menu_known_key_button = CustomButton(menu_frame, **styles["side button"], text="Generate key", command=loadFrameGenerateKey)
menu_encrypt_file_button = CustomButton(menu_frame, **styles["side button"], text="Encrypt file", command=loadFrameEncryptFile)
menu_decrypt_file_button = CustomButton(menu_frame, **styles["side button"], text="Decrypt file", command=loadFrameDecryptFile)

menu_widgets = (menu_decrypt_text_button, menu_encrypt_text_button, menu_random_key_button,
                menu_known_key_button, menu_encrypt_file_button, menu_decrypt_file_button)

decrypt_text_frame = Frame(window, bg=bg)
encrypt_text_frame = Frame(window, bg=bg)
random_key_frame = Frame(window, bg=bg)
known_key_frame = Frame(window, bg=bg)
encrypt_file_frame = Frame(window, bg=bg)
decrypt_file_frame = Frame(window, bg=bg)

# Decrypt Widgets
decrypt_text_entry = Entry(decrypt_text_frame, **styles["entry"])
decrypt_key_entry = Entry(decrypt_text_frame, **styles["entry"], width=38)
decrypt_output = Label(decrypt_text_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))

# Encrypt Widgets
encrypt_text_entry = Entry(encrypt_text_frame, **styles["entry"])
encrypt_key_entry = Entry(encrypt_text_frame, **styles["entry"], width=38)
encrypt_output = Label(encrypt_text_frame, bg=bg, fg=emphasis, font=(font, 16, "bold"))

# Random Key Widgets
key_check_entry = Entry(random_key_frame, **styles["entry"], width=38)
key_check_but = CustomButton(random_key_frame, **styles["button"], text="Check Key", command=checkKey, width=18)
letters_label = Label(random_key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))
mapped_letters_label = Label(random_key_frame, text=letters, bg=bg, fg=text_col, font=("Consolas", 14))

# Known Key Widgets
generate_key_entry = Entry(known_key_frame, **styles["entry"], width=45)
generate_known_key_button = CustomButton(known_key_frame, **styles["button"], text="Generate Key",
                                         command=generateKnownKey, width=18)
key_label = Label(known_key_frame, bg=bg, fg=text_col, font=(font, 16))
generate_random_key_button = CustomButton(known_key_frame, **styles["button"], text="Generate Key",
                                          command=generateRandomKey, width=18)
random_key_label = Label(known_key_frame, bg=bg, fg=text_col, font=(font, 16))

# Encrypt File Widgets
en_entry_sv = StringVar()
encrypt_file_entry = Entry(encrypt_file_frame, textvariable=en_entry_sv, width=25, font=(font, 14),
                           disabledbackground="#161616", disabledforeground="#161616", state="disabled")

encrypt_file_name_label = Label(encrypt_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

encrypt_file_confirm_button = CustomButton(encrypt_file_frame, **styles["button"], text="Encrypt File", width=15,
                                           command=encryptFile, disabledforeground=text_col)

encrypt_file_entry.drop_target_register(DND_FILES)
encrypt_file_entry.dnd_bind('<<Drop>>', drop)
encrypt_file_key_entry = Entry(encrypt_file_frame, **styles["entry"], width=45)

# Decrypt File Widgets
de_entry_sv = StringVar()
decrypt_file_entry = Entry(decrypt_file_frame, textvariable=de_entry_sv, width=25, font=(font, 14),
                           disabledbackground="#161616", disabledforeground="#161616", state="disabled")

decrypt_file_name_label = Label(decrypt_file_frame, bg="#222222", fg="#FFFFFF", font=(font, 14))

decrypt_file_confirm_button = CustomButton(decrypt_file_frame, **styles["button"], text="Decrypt File", width=15,
                                           command=decryptFile, disabledforeground=text_col)

decrypt_file_entry.drop_target_register(DND_FILES)
decrypt_file_entry.dnd_bind('<<Drop>>', drop)

setupFrameDecryptText()
setupFrameEncryptText()
setupFrameKeyCheck()
setupFrameEncryptFile()
setupFrameDecryptFile()
setupFrameGenerateKey()

menu_frame.place(x=0, y=0, width=150, height=700)

for wid in menu_widgets:
    wid.pack(anchor="e", padx=5, pady=20)

Label(text="R. Poulter v1.2.2", bg=bg2, fg=bg, font=(font, 10)).place(x=0, y=652)

window.mainloop()
