import time
from urllib.parse import urlparse, parse_qs
import selenium
from selenium import webdriver
import requests
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def auth(uuid, username, password):
    base_url = (
        "https://somtoday.nl/oauth2/authorize?"
        "redirect_uri=somtoday://nl.topicus.somtoday.leerling/oauth/callback"
        "&client_id=somtoday-leerling-native"
        "&response_type=code"
        "&prompt=login"
        "&state=testets"
        "&scope=openid"
        "&code_challenge=tCqjy6FPb1kdOfvSa43D8a7j8FLDmKFCAz8EdRGdtQA"
        "&code_challenge_method=S256"
        f"&tenant_uuid={uuid}"
    )

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)

    def login():
        browser.get(base_url)

        username_field = browser.find_element(By.ID, "usernameField")
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)

        password_field = browser.find_element(By.ID, "password-field")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        attempt = 0

        while attempt < 3:
            console_logs = browser.get_log('browser')
            for log_entry in console_logs:
                if 'Failed to launch' in log_entry['message']:
                    url = log_entry['message'].split("'")[1]
                    code = parse_qs(urlparse(url).query)['code'][0]

                    # Exchange the authorization code for tokens
                    payload = {
                        'grant_type': 'authorization_code',
                        'redirect_uri': 'somtoday://nl.topicus.somtoday.leerling/oauth/callback',
                        'code_verifier': 't9b9-QCBB3hwdYa3UW2U2c9hhrhNzDdPww8Xp6wETWQ',
                        'code': code,
                        'scope': 'openid',
                        'client_id': 'somtoday-leerling-native'
                    }

                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }

                    response = requests.post('https://somtoday.nl/oauth2/token', data=payload, headers=headers)
                    token_data = response.json()
                    browser.quit()
                    return token_data
            
            time.sleep(1)

            password_field = browser.find_element(By.ID, "password-field")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            
            attempt += 1
        
        return {"message": "error"}

    try:
        return login()
    except selenium.common.exceptions.NoSuchElementException:
        # Retry
        return login()
    except Exception:
        return {"message": "error"}
