from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # App
    microservice_name: str = Field(alias="MICROSERVICE_NAME")
    microservice_version: str = Field(alias="MICROSERVICE_VERSION")
    environment: str = Field(alias="ENVIRONMENT")

    # Keyvault
    az_keyvault_url: str = Field(alias="AZURE_KEYVAULT_URL")

    # Databases
    catalog_database: str = Field(alias="CATALOG_DATABASE")
    providers_database: str = Field(alias="DATABASE_PROVIDERS")
    # Azure Services Bus
    az_sb_namespace: str = Field(alias="AZURE_SERVICE_BUS_NAMESPACE")

    # Blob Storage
    az_storage_account_url: str = Field(alias="AZURE_BLOB_STORAGE_ACCOUNT_URL")
    az_bs_container_name: str = Field(alias="AZURE_BLOB_STORAGE_CONTAINER_NAME")

    # Queues
    az_sb_queue_audit: str = Field(alias="AZURE_SB_QUEUE_AUDIT")

    app_insights_conn_str: Optional[str] = Field(
        default=None, alias="APP_INSIGHTS_CONNECTION_STRING"
    )

    # GRPC Services
    security_grpc_endpoint: str = Field(alias="SECURITY_GRPC_HOST")
    grpc_secure: bool = Field(default=True, alias="GRPC_SECURE")


settings = Settings()
