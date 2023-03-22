__author__ = 'ispaneli'
__email__ = 'ispanelki@gmail.com'

__version__ = '0.0.3'

__doc__ = """
FStorage
=====

It's a simple asynchronous secure file storage for microservices.
It is implemented on the FastAPI web framework.

To run the file storage, you need PostgreSQL installed.

WARNING: With the usual installation of `pip install fstorage`,
         the requirements are not installed!
         Installation recommendations:
             1. `pip install 'fstorage[server]'` - to deploy file storage;
             2. `pip install 'fstorage[sync_client]'` - to use SYNC client;
             3. `pip install 'fstorage[async_client]'` - to use ASYNC client.

----------------------------

Author: @ispaneli
E-mail: ispanelki@gmail.com
GitHub repository: <https://github.com/ispaneli/fstorage>
"""
