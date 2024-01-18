# Encryption-Program
Python program used to encrypt and decrypt text and .txt files using a custom cipher.

The program has 6 functions:
- Encrypting text
- Decrypting text
- Validating keys
- Generating keys
- Encrypting .txt files
- Decrypting .txt files

The cipher is difficult to crack without knowing how it works, as it has over 403 SEPTILLION possible keys.
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
```bash
pip install -r /path/to/requiremnets.txt
```

## Usage


### Encrypting Text
- Enter plain text
- Enter key, or select random key
- Press "Encrypt"
- Copy cipher text or key to clipboard

### Decrypting Text
- Enter cipher text
- Enter key
- Press "Decrypt"
- Copy plain text to clipboard

### Validating Keys
- Enter key
- Press "Check Key"
- If the key is valid, the letter mapping will be shown

### Generating Keys
- Enter the mapping in the format *H,E,M,Q,K,Y,U,J,W,O,V,P,T,X,Z,D,F,C,S,B,N,I,G,R,L,A* where A maps to H, B maps to E, etc.
- Press "Generate Key"
- If the mapping is valid, the corresponding key will be generated

### Encrypting Files
- Open the "Encrypt file" tab on the window
- Open File Explorer and locate chosen .txt file to encrypt
- Drag and drop the file into the box on the window
- Press "Encrypt File" below the file name
- The encrypted file will contain the key used to encrypt/decrypt the text, followed by the encrypted text

### Decrypting Files
- Open the "Decrypt file" tab on the window
- Open File Explorer and locate chosen .txt file to encrypt
- Drag and drop the file into the box on the window
- Press "Decrypt File" below the file name
- The decrypted file will contain decrypted text

## Development
Written in Python 3.10.\
Python version is fully functional.\
Future updates will include:
<ul>
  <li>Ability to generate key from letter mapping</li>
  <li>Browser version</li>
</ul>
