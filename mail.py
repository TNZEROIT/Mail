import requests
import random
import string
import concurrent.futures
from termcolor import colored

def generate_random_name():
    random_length = random.randint(5, 9)
    random_name = ''.join(random.choices(string.ascii_lowercase, k=random_length))
    return random_name

def check_email_exists(email):
    url = f"https://tempmail.plus/api/mails?email={email}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            mails = response.json().get('mail_list', [])
            if mails:
                return True, email
            else:
                return False, email
        else:
            print(f"Error: {response.status_code}")
            return False, email
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, email

def process_domain(domain, random_name):
    email = f"{random_name}@{domain}"
    exists, email = check_email_exists(email)

    if exists:
        print(colored(f"Email {email} exists.", 'green'))
        with open("mail.txt", "a") as file:
            file.write(email + "\n")
    else:
        print(f"Email {email} does not exist.")

def main():
    domains = [
        "mailto.plus", "fexpost.com", "fexbox.org",
        "mailbox.in.ua", "rover.info", "chitthi.in",
        "fextemp.com", "any.pink", "merepost.com"
    ]

    while True:
        random_name = generate_random_name()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_domain, domain, random_name) for domain in domains]
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
