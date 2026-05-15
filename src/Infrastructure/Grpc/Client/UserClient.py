import grpc
from Osdental.Models.Response import Response
from Osdental.Decorators.Retry import grpc_retry
from Osdental.Exception.ControlledException import OSDException
from src.Infrastructure.Grpc.Generated import Common_pb2
from src.Infrastructure.Grpc.Generated import User_pb2_grpc
from src.Shared.Config import Config


class UserClient:

    def __init__(self, host=Config.SECURITY_GRPC_HOST, port=Config.SECURITY_GRPC_PORT):
        if not host:
            raise OSDException("USER_GRPC_HOST is not set")
        self.host = host
        self.port = port
        self.secure = Config.GRPC_SECURE

    async def __aenter__(self):
        print(f"Connecting to Location gRPC server at {self.host}")  #:{self.port}
        if self.secure:

            url = self.host
            creds = grpc.ssl_channel_credentials()
            self.channel = grpc.aio.secure_channel(url, creds)
        else:
            url = self.host  # f"{self.host}:{self.port}"
            self.channel = grpc.aio.insecure_channel(url)

        self.stub = User_pb2_grpc.UserStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.channel.close()

    @grpc_retry
    async def get_user_by_id(self, request) -> Response:
        req = Common_pb2.Request(data=request)
        return await self.stub.GetUserById(req)

    @grpc_retry
    async def get_users_by_client(self, request) -> Response:
        print(f"Sending request to get users by client with data: {request}")
        req = Common_pb2.Request(data=request)
        return await self.stub.GetUsersByClient(req)
