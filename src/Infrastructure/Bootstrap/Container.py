import asyncio
from typing import Callable
from Osdental.Helpers.KeyVaultService import AzureKeyVaultSecretProvider
from Osdental.Database.Connection import Connection
from Osdental.Messaging.AzureServiceBus import AzureServiceBusQueue
from Osdental.Storage.AzureBlobStorage import AzureBlobStorage
from Osdental.Graphql._Helpers._TokenService import TokenService

from src.Infrastructure.Persistence.UnitOfWork import UnitOfWork
from src.Infrastructure.Grpc.Client.Connection import GrpcConnection
from src.Infrastructure.Grpc.Client.AuthGrpcClient import AuthGrpcClient
from src.Infrastructure.Grpc.Adapter.AuthGrpcAdapter import AuthGrpcAdapter
from src.Shared.Enums.Secrets import Secrets
from src.Application.Dto.AppConfig import AppConfig
from src.Infrastructure.Config.Settings import settings


class Container:
    # KeyVault
    key_vault: AzureKeyVaultSecretProvider | None = None
    # Database
    catalog_database: Connection | None = None
    uow_factory: Callable[[], UnitOfWork] = None
    # gRPC Security
    grpc_security_conn: GrpcConnection | None = None
    grpc_security_client: AuthGrpcClient | None = None
    grpc_security: AuthGrpcAdapter | None = None
    # Azure Services Bus for Audit
    az_sb_audit: AzureServiceBusQueue | None = None
    # Blob Storage
    az_blob_storage: AzureBlobStorage | None = None
    # Token Service for AuditExtension
    token_service: TokenService | None = None

    secrets_to_get = [
        Secrets.AES_KEY_AUTH,
        Secrets.AES_KEY_USER,
        Secrets.AUTH_JWT_USER_KEY,
    ]

    config: AppConfig | None = None

    @classmethod
    async def startup(cls):
        # KeyVault
        cls.key_vault = AzureKeyVaultSecretProvider(settings.az_keyvault_url)

        # Get secrets from KeyVault
        config_values = await asyncio.gather(
            *(cls.key_vault.get(s) for s in cls.secrets_to_get)
        )
        cls.config = AppConfig(*config_values)

        # Database
        cls.catalog_database = Connection(db_url=settings.catalog_database)
        cls.provider_database = Connection(db_url=settings.providers_database)
        cls.uow_factory = lambda: UnitOfWork(cls.catalog_database.session_factory)
        # gRPC auth
        print("GRPC ENDPOINT:", settings.security_grpc_endpoint)
        cls.grpc_security_conn = GrpcConnection(
            settings.security_grpc_endpoint, secure=settings.grpc_secure
        )
        channel = cls.grpc_security_conn.connect()
        cls.grpc_security_client = AuthGrpcClient(channel)
        cls.grpc_security = AuthGrpcAdapter(cls.grpc_security_client)
        # ServiceBus
        cls.az_sb_audit = AzureServiceBusQueue(
            settings.az_sb_namespace, settings.az_sb_queue_audit
        )
        # Blob Storage
        cls.az_blob_storage = AzureBlobStorage(
            account_url=settings.az_storage_account_url,
            container_name=settings.az_bs_container_name,
        )
        # Token Service for AuditExtension
        cls.token_service = TokenService(
            jwt_user_key=cls.config.jwt_user_key, auth_validator=cls.grpc_security
        )

    @classmethod
    async def shutdown(cls):
        if cls.key_vault:
            await cls.key_vault.close()

        if cls.grpc_security_conn:
            await cls.grpc_security_conn.close()

        if cls.catalog_database:
            await cls.catalog_database.close_engine()

        if cls.az_sb_audit:
            await cls.az_sb_audit.close()

        if cls.az_blob_storage:
            await cls.az_blob_storage.close()
