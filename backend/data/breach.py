import requests


class Breach:
    def __init__(self, email):
        self.email = email

    def getBreaches(self):
        # Construct the URL for the API request
        url = f"https://api.xposedornot.com/v1/check-email/{self.email}"

        try:
            # Make the GET request to the API
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Extract breaches from the response
                breaches = data.get('breaches', [])

                # Check if breaches is a list with the expected structure
                if isinstance(breaches, list) and len(breaches) > 0 and isinstance(breaches[0], list):
                    # Extract the first list of breaches
                    breaches_list = breaches[0]
                else:
                    breaches_list = []

                return breaches_list
            else:
                print(f"Error: Received status code {response.status_code}")
                return []

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return []

