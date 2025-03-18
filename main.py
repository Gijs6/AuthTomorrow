import time
import difflib
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CLIENT_ID = 'somtoday-leerling-native'
REDIRECT_URI = "somtoday://nl.topicus.somtoday.leerling/oauth/callback"
response = requests.get('https://servers.somtoday.nl/organisaties.json')
data = response.json()
school_list = data[0]['instellingen']
school_names = [school["naam"] for school in school_list]

school_input = input("Search for your school name: ")
matches = difflib.get_close_matches(school_input, school_names, n=5, cutoff=0.3)

if matches:
    print("Search results:")
    for i, match in enumerate(matches):
        print(f"{i + 1}. {match}")
    choice = input("Enter the number of your school on the list: ")
    if choice.isdigit() and 1 <= int(choice) <= len(matches):
        selected_name = matches[int(choice) - 1]
        selected_school = next(school for school in school_list if school["naam"] == selected_name)
        print(f"\nYou have chosen '{selected_name}' (UUID: {selected_school['uuid']})")
    else:
        raise ValueError("Invalid choice")
else:
    raise ValueError("No schools found")

username = input("Username: ")
password = input("Password: ")  # getpass didn't work for some reason

base_url = (
    "https://somtoday.nl/oauth2/authorize?"
    f"redirect_uri={REDIRECT_URI}"
    f"&client_id={CLIENT_ID}"
    "&response_type=code"
    "&prompt=login"
    "&scope=openid"
    "&code_challenge=tCqjy6FPb1kdOfvSa43D8a7j8FLDmKFCAz8EdRGdtQA"
    "&code_challenge_method=S256"
    f"&tenant_uuid={selected_school['uuid']}"
)

print("Getting browser ready...")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)
browser.get(base_url)

# Logging in
print("Entering username and password...")
username_field = browser.find_element(By.ID, "usernameField")
username_field.send_keys(username)
username_field.send_keys(Keys.RETURN)

password_field = browser.find_element(By.ID, "password-field")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Bug that requires entering password twice
password_field = browser.find_element(By.ID, "password-field")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

print("Receiving auth data...")
start_time = time.time()

while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= 20:  # Can be modified
        print("Timeout: No response after 20 seconds")
        break

    # Check logs for the auth
    console_logs = browser.get_log('browser')

    for log_entry in console_logs:
        if 'Failed to launch' in log_entry['message']:
            url = log_entry['message'].split("'")[1]
            code = parse_qs(urlparse(url).query)['code'][0]

            payload = {
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI,
                'code_verifier': 't9b9-QCBB3hwdYa3UW2U2c9hhrhNzDdPww8Xp6wETWQ',
                'code': code,
                'scope': 'openid',
                'client_id': CLIENT_ID
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post('https://somtoday.nl/oauth2/token', data=payload, headers=headers)
            token_data = response.json()

            # Save to JSON
            # with open("token.json", "w") as json_file:
            #    json.dump(token_data, json_file, indent=4)
            print("Access token:")
            print(token_data["access_token"])
            print("\nRefresh token:")
            print(token_data["refresh_token"])
            break
    else:
        time.sleep(1)
        continue
    break
