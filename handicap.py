import requests
from bs4 import BeautifulSoup
from login import username, pccaddie, pccaddie_club

def login_and_get_handicap(username, password):
    # Create a session to maintain the login session
    session = requests.Session()

    # URL of the website's login page
    url = 'https://www.pccaddie.net/clubs/0498925/app.php?cat=handicap'

    # Form data to be submitted
    form_data = {
        'rq[login]': username,  # Field name for the username input
        'rq[password]': password,  # Field name for the password input
        'service': 'login',  # Hidden field for the service
        'button_cancel': '1',  # Hidden field for the button_cancel
    }

    # Perform the login
    response = session.post(url, data=form_data)

    if response.ok:
        print("Login successful")

        # URL to access the profile page or the specific page with handicap data
        profile_url = f"https://www.pccaddie.net/clubs/{pccaddie_club}/app.php?cat=handicap"

        # Make a GET request to the profile page
        profile_response = session.get(profile_url)
        
        if profile_response.ok:
            # Parse the response to extract data
            soup = BeautifulSoup(profile_response.text, 'html.parser')

            # Find the span containing the handicap score
            handicap_span = soup.find('span', class_='title', string=lambda text: text and "Mein Handicap Index:" in text)
            if handicap_span:
                # Extract the number from the span text
                score_text = handicap_span.text.strip()
                score = score_text.split(':')[-1].strip()
                return score
            else:
                print("Handicap score not found")
                return None
        else:
            print("Failed to retrieve profile data")
            return None
    else:
        print("Login failed")
        return None


def main():
    # Example usage
    handicap_score = login_and_get_handicap(username, pccaddie)
    if handicap_score:
        print("Current Handicap Score:", handicap_score)


if __name__ == '__main__':
    main()
