import random, string

def get_random_string():
    length=30
    # choose from all lowercase letter, uppercase
    stringa = ""
    letters = string.ascii_letters + "1234567890"
#    print(letters) # stringa di tutte le lettere maiuscole e minuscole + numeri
    for i in range(length):
        #print(random.choice(letters))
        stringa = stringa + random.choice(letters)
    return stringa
