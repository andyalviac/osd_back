import grpc
from Osdental.Models.Response import Response
from Osdental.Decorators.Retry import grpc_retry
from Osdental.Exception.ControlledException import OSDException
from src.Infrastructure.Grpc.Generated import Common_pb2
from src.Infrastructure.Grpc.Generated import Connection_pb2_grpc
from src.Shared.Config import Config


class ConnectionClient:

    def __init__(
        self, host=Config.CONNECTION_GRPC_HOST, port=Config.CONNECTION_GRPC_PORT
    ):
        if not host:
            raise OSDException("CONNECTION_GRPC_HOST is not set")
        self.host = host
        self.port = port

    async def __aenter__(self):
        print(f"Connecting to Connection gRPC server at {self.host}:{self.port}")
        if self.port:
            url = f"{self.host}:{self.port}"
            self.channel = grpc.aio.insecure_channel(url)
        else:
            url = self.host
            creds = grpc.ssl_channel_credentials()
            self.channel = grpc.aio.secure_channel(url, creds)

        self.stub = Connection_pb2_grpc.ConnectionStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.channel.close()

    @grpc_retry
    async def get_all_providers_by_ids(self, request) -> Response:
        req = Common_pb2.Request(data=request)
        return await self.stub.GetAllProvidersByIds(req)
