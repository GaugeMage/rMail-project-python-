# Imports
import hashlib
import os.path

# Global variables
m = hashlib.sha256()
attempts = 5
key = 4
userData = {}
alphabet = "abcdefghijklmnopqrstuvwxyz"
newAlphabet = ""

if os.path.exists("userInformation.txt"): #Don't want to explain it
    f = open("userInformation.txt", "r")
    for line in f:
        words = line.split("`")
        userName = words[0]
        mailString = words[3][:-2]
        inbox = mailString.split("^")
        info = (words[1], words[2], inbox)
        userData[userName] = info
    f.close()

def encryption(message): # Function for encrypting the message
    key = 4
    newMessage = ""
    for y in range(0, len(message)):
        fIndex: alphabet.find(message[y])
        if key < 0:  # If key is negative
            newAlphabet = alphabet[(26 + key):] + alphabet[:(26 + key)]
        else:  # If key is positive
            newAlphabet = alphabet[key:] + alphabet[:key]
        fIndex = alphabet.find(message[y])
        if fIndex < 0:
            newMessage += message[y]
        else:
            newMessage += newAlphabet[fIndex]
    return newMessage

def decryption(message):
    newMessage = ""
    key = -4
    newAlphabet = alphabet[(26 + key):] + alphabet[:(26 + key)]
    for x in range(0, len(message)):
        index = alphabet.find(message[x])
        if index < 0:
            newMessage += message[x]
        else:
            newMessage += newAlphabet[index]
    return newMessage

def rewriteFile(): #Function for writing file
    f = open("userInformation.txt", "w")
    for user in userData:
        info = userData[user]
        line = str(user + "`" + info[0] + "`" + info[1] + "`")
        f.write(line)
        inbox = info[2]
        for email in inbox:
            f.write(email + "^")
        f.write("\n")
    f.close()

def hasher(x): # Function for hashing passwords
    b = bytes(x, "UTF-8")
    return hashlib.sha256(b).hexdigest()

def account(user): # Function for account
    inboxOrWrite = input("Enter I if you want to access your inbox. Enter W if you want to write a message to another user. Enter Q if you want to exit your account: ").lower()
    while inboxOrWrite:
        if inboxOrWrite == "i":  # If user accesses inbox
            inbox = userData[user][2]
            for item in inbox:
                dMessage = decryption(item)
                print(dMessage)
        elif inboxOrWrite == "w":  # If user sends message to another user
            mailRecipient = input("Who is the recipient of this email: ")
            if not userData.get(mailRecipient):  # If there is no user to begin with
                print("Error no user detected")
                continue
            eMail = input("What is the message you want to send: ").strip("^") #If there is a ^ in their message
            info = userData[mailRecipient]
            friendInbox = info[2]
            friendInbox.append(encryption(eMail)) # Encrypts message
        elif inboxOrWrite == "q":
            break
        else:
            print("That is not an option Try again!")
        inboxOrWrite = input("Enter I if you want to access your inbox. Enter W if you want to write a message to another user. Enter Q if you want to exit your account: ").lower()

registerOrLogin = input("Enter C if you want to create an account. Enter L if you want to login. Enter Q if you want to quit: ").lower() #Beginning of user's input
while (registerOrLogin != "l" or registerOrLogin != "c") and registerOrLogin != "q":
    if registerOrLogin == "c": # If user wants to register
        userName = input("Create Name: ")
        password = input("Create Password: ")
        birthday = input("Enter Birthday: ")
        inbox = []
        inbox.append(encryption("Welcome to rMail")) #Encrypts initial message
        hashValue = hasher(password)
        info = (hashValue, birthday, inbox)
        userData[userName] = info
    elif registerOrLogin == "l": # If user wants to login
        for x in range(0, 5):
            uUserName = input("Name: ")
            uPassword = input("Password: ")
            uPassword = hasher(uPassword)
            if uPassword == "q" or uPassword == "Q" or uUserName == "q" or uUserName == "Q":
                break
            elif not userData.get(uUserName): # If there is no user to begin with
                print("Error no user detected")
                print(str(attempts-1) + " attempts remaining")
                attempts -= 1
                continue
            elif uPassword != userData[uUserName][0]: # If the user gets the wrong password
                print("Wrong! " + str(attempts-1) + " attempts remaining")
                attempts -= 1
            else: # If the user login is successful.
                account(uUserName)
                break
    registerOrLogin = input("Enter C if you want to create an account. Enter L if you want to login. Enter Q if you want to quit: ").lower()
rewriteFile() #Rewrites file