from api.client import APIClient

if __name__ == "__main__":
    client = APIClient(base_url="http://localhost:8080")
    hello_world_message = client.hello_world()
    print(hello_world_message)
