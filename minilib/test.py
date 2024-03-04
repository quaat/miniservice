from api.client import APIClient

if __name__ == "__main__":
    client = APIClient(base_url="http://localhost:5000/person")
    person = client.retrieve_person("af5981da0c093cebbaf028581809e3cc59435b83")

    print(person)
