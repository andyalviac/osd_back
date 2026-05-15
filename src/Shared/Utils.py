import base64
import mimetypes
from decimal import Decimal
from typing import Dict, Any, List
from datetime import datetime, date
from Osdental.Models.Token import AuthToken
from Osdental.Shared.Utils.DataUtils import DataUtils
from src.Shared.Enums.Constant import Constant
from src.Shared.Instances import aes  # , blob_connection_string, blob_container_name
from src.Application.Services.UserService import UserService
from src.Infrastructure.Grpc.Client.UserClient import UserClient
from azure.storage.blob import ContentSettings
import asyncio
from src.Shared.Enums.Secrets import Secrets

from Osdental.Helpers.KeyVaultService import AzureKeyVaultSecretProvider
from Osdental.Encryptor.Rsa import RSAEncryptor
from Osdental.Encryptor.Jwt import JWT
from Osdental.Encryptor.Aes import AES
from pydantic import Field
from Osdental.Models.Response import Response

from Osdental.Shared.Utils.RsaUtils import normalize_rsa_keys

az_keyvault_url: str = Field(alias="AZURE_KEYVAULT_URL")
key_vault = AzureKeyVaultSecretProvider(az_keyvault_url)


def custom_serializer(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def get_id_external(token: AuthToken, data: Dict[str, str]) -> str:
    """
    if mk_id_external_enterprise is present in the token, return it.
    if mk_id_external_enterprise is not present, return id_external_enterprise
    """
    print("get_id_external called with token and data:")
    return (
        DataUtils.normalize_uuid_value(
            aes.decrypt(token.aes_key_auth, token.mk_id_external_enterprise)
        )
        if token.mk_id_external_enterprise
        else (data.get(Constant.ID_EXTERNAL) or token.id_external_enterprise)
    )


async def fill_authors_fields(items: List[Dict[str, Any]], cache: Dict) -> None:
    async with UserClient() as user_client:
        user_service = UserService(user_client)
        for item in items:
            for field, user_id in item.items():
                if not (field.endswith("By") or field == "author") or not user_id:
                    continue
                if user_id not in cache:
                    user_name = await user_service.get_user_by_id(user_id)
                    if not user_name:
                        continue
                    cache[user_id] = user_name
                item[field] = cache[user_id]
        return items


def build_blob_base_url(connection_string: str) -> str:
    parts = {
        key: value
        for item in connection_string.split(";")
        if "=" in item
        for key, value in [item.split("=", 1)]
    }

    protocol = parts.get("DefaultEndpointsProtocol", "https")
    account_name = parts.get("AccountName")
    endpoint_suffix = parts.get("EndpointSuffix", "core.windows.net")

    return f"{protocol}://{account_name}.blob.{endpoint_suffix}"


def get_deduction_blob_path(cycle_id, deduction_id):
    return f"compensations/files/cycles/{cycle_id}/deductions/{deduction_id}/document"


async def decriptar(encrypted_access_token, data):
    rsa_private_key_2, jwt_secret_key = await asyncio.gather(
        key_vault.get(Secrets.SECRET_RSA_KEY_2),
        key_vault.get(Secrets.AUTH_JWT_SECRET_KEY),
    )

    rsa_private_key_2 = normalize_rsa_keys(rsa_private_key_2)

    access_token = RSAEncryptor.decrypt(encrypted_access_token, rsa_private_key_2)
    payload_token = JWT.extract_payload(access_token, jwt_secret_key)

    aes_key = payload_token.get("aesKey")
    payload = AES.decrypt(aes_key, data)

    data_encrypted = AES.encrypt(aes_key, data)
    return Response(data=data_encrypted, key=aes_key)
