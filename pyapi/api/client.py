import requests
from typing import Dict


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/dummy"):
        """
        Initializes the API client with a base URL.

        :param base_url: The base URL for the API endpoints.
        """
        self.base_url = base_url

    def populate_redis(self, key: str, value: Dict[str, str]) -> Dict:
        """
        Populates the Redis cache with a key-value pair.

        :param key: The key under which the value is stored.
        :param value: The value to store, a dictionary.
        :return: The response from the API as a dictionary.
        """
        endpoint = f"{self.base_url}/populate/"
        payload = {"key": key, "value": value}

        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
            return {"error": str(e)}

    def retrieve_redis(self, key: str) -> Dict:
        """
        Retrieves the value for a given key from the Redis cache.

        :param key: The key for which to retrieve the value.
        :return: The response from the API as a dictionary.
        """
        endpoint = f"{self.base_url}/retrieve/"
        params = {"key": key}

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
