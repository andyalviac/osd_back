import os
from dotenv import load_dotenv
from Osdental.Encryptor.Aes import AES
from Osdental.Database.Connection import Connection
from Osdental.Database.BaseRepository import BaseRepository

# from Osdental.RedisCache.Redis import RedisCacheAsync
from azure.storage.blob.aio import BlobServiceClient
from Osdental.Cache.Redis import RedisCacheAsync

load_dotenv(dotenv_path=".env", override=True)

aes = AES()
redis = RedisCacheAsync(os.getenv("REDIS_PROVIDERS"))
# blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")
# blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
# blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

# Connection
db_providers = BaseRepository(os.getenv("DATABASE_PROVIDERS"))
