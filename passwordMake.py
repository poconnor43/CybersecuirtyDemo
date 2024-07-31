import random
import string

def generate_password():
    length = int(input("\nPlease enter the desired password length: "))
    alphabet = string.ascii_letters + string.punctuation 
    password = ''.join(random.choice(alphabet) for i in range(length))
    print(f"Generated password: {password}")

# example/Test the function
#generate_password()
