from grpc.aio import Channel
from src.Application.Dto.GrpcResponse import GrpcResponse
from src.Infrastructure.Grpc.Generated import Portal_pb2_grpc
from src.Infrastructure.Grpc.Generated import Common_pb2


class AuthGrpcClient:

    def __init__(self, channel: Channel):
        self.stub = Portal_pb2_grpc.PortalStub(channel)

    async def call_validate_auth_token(self, request: str) -> GrpcResponse:
        try:
            print("Enviando solicitud gRPC para validar token de autenticación...")
            request = Common_pb2.Request(data=request)

            response = await self.stub.ValidateAuthToken(request, timeout=5)

            print("Respuesta gRPC recibida:", response)

            return GrpcResponse(
                status=response.status, message=response.message, data=response.data
            )

        except Exception as e:
            import traceback

            print("💥 ERROR EN LLAMADA GRPC:")
            traceback.print_exc()
            raise
