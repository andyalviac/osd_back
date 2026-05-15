import grpc
from Osdental.Models.Response import Response
from Osdental.Decorators.Retry import grpc_retry
from Osdental.Exception.ControlledException import OSDException
from src.Infrastructure.Grpc.Generated import Common_pb2
from src.Infrastructure.Grpc.Generated import Catalog_pb2_grpc
from src.Shared.Config import Config


class CatalogClient:
    def __init__(self, host=Config.CATALOG_GRPC_HOST, port=Config.CATALOG_GRPC_PORT):
        if not host:
            raise OSDException("CATALOG_GRPC_HOST is not set")
        self.host = host
        self.port = port

    async def __aenter__(self):
        print(f"Connecting to Catalog gRPC server at {self.host}")  #:{self.port}
        if self.port:
            print(f"Using port {self.port} insecure_channel")
            url = f"{self.host}:{self.port}"
            self.channel = grpc.aio.insecure_channel(url)
        else:
            print(f"Using port {self.host} secure_channel")
            url = self.host
            creds = grpc.ssl_channel_credentials()
            self.channel = grpc.aio.secure_channel(url, creds)

        self.stub = Catalog_pb2_grpc.CatalogStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.channel.close()

    @grpc_retry
    async def get_catalog_detail_by_id(self, request) -> Response:
        req = Common_pb2.Request(data=request)
        return await self.stub.FindCatalogDetailById(req)

    @grpc_retry
    async def get_catalog_data(self, request) -> Response:
        req = Common_pb2.Request(data=request)
        return await self.stub.GetCatalogData(req)
