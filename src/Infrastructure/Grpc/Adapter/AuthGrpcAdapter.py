import json
from src.Infrastructure.Grpc.Client.AuthGrpcClient import AuthGrpcClient
from abc import ABC, abstractmethod


class IAuthValidator(ABC):

    @abstractmethod
    async def validate_auth_token(self, request: str) -> bool: ...


class AuthGrpcAdapter(IAuthValidator):

    def __init__(self, client: AuthGrpcClient):
        self.client = client

    async def validate_auth_token(self, request: dict) -> bool:
        print("validando//////////////////")
        data_json = json.dumps(request)
        response = await self.client.call_validate_auth_token(data_json)
        if response.status != "DB_0004":
            raise ValueError(response.message)

        return response.data
