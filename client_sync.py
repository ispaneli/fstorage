from src.fstorage.client.synch.client import SyncClient


if __name__ == '__main__':
    client = SyncClient("http://127.0.0.1:8000")

    upload_response: dict = client.upload(open("LICENSE", 'rb'))
    print(upload_response)
    # {'id': "<file_id>"}

    get_response: dict = client.get(upload_response['id'])
    print(get_response)
    # {'filename': "LICENSE", 'bytes': '<data_as_bytes>'}

    client.delete(upload_response['id'])

    try:
        client.get(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."

    try:
        client.delete(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."
