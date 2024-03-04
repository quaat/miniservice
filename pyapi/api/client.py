""" APIClient - communicate with the service
"""

import requests
from typing import Dict, Any


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/person"):
        """
        Initializes the API client with a base URL.

        :param base_url: The base URL for the API endpoints, adjusted to match the '/person' prefix.
        """
        self.base_url = base_url

    def store_person(self, person: Dict[str, Any]) -> Dict:
        """
        Populates the Redis cache with a person's data.

        :param person: The person's data as a dictionary, following the Person model structure.
        :return: The response from the API as a dictionary.
        """
        endpoint = f"{self.base_url}/populate/"
        try:
            response = requests.post(endpoint, json=person)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
            return {"error": str(e)}

    def retrieve_person(self, person_hash: str) -> Dict:
        """
        Retrieves a person's data from the Redis cache using a hash.

        :param person_hash: The hash of the person's data used as the key in Redis.
        :return: The response from the API as a dictionary, structured according to the Person model.
        """
        endpoint = f"{self.base_url}/retrieve/"
        params = {"hash": person_hash}

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
            return {"error": str(e)}
