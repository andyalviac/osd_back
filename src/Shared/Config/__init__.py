import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)


class Config:
    SECURITY_GRPC_HOST = os.getenv("SECURITY_GRPC_HOST")
    SECURITY_GRPC_PORT = os.getenv("SECURITY_GRPC_PORT")
    CATALOG_GRPC_HOST = os.getenv("CATALOG_GRPC_HOST")
    CATALOG_GRPC_PORT = os.getenv("CATALOG_GRPC_PORT")
    CONNECTION_GRPC_HOST = os.getenv("CONNECTION_GRPC_HOST")
    CONNECTION_GRPC_PORT = os.getenv("CONNECTION_GRPC_PORT")
    GRPC_SECURE = os.getenv("GRPC_SECURE", "true").lower() == "true"
