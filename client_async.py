import asyncio

from src.fstorage.client.asynch.client import AsyncClient


async def main():
    client = AsyncClient("http://127.0.0.1:8000")

    upload_response: dict = await client.upload(open("LICENSE", 'rb'))
    print(upload_response)
    # {'id': "<file_id>"}

    get_response: dict = await client.get(upload_response['id'])
    print(get_response)
    # {'filename': "LICENSE", 'bytes': '<data_as_bytes>'}

    await client.delete(upload_response['id'])

    try:
        await client.get(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."

    try:
        await client.delete(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."


if __name__ == '__main__':
    asyncio.run(main())
