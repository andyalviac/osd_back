from Osdental.Decorators.Grpc import grpc_response
from Osdental.Database.Connection import Connection
from Osdental.Database.UowFactory import UowFactory
from src.Infrastructure.Grpc.Generated import Client_pb2_grpc
from src.Application.UseCases.Grpc.ClientUseCase import ClientUseCase 
from src.Infrastructure.Repositories.Client.ClientRepository import ClientRepository
from src.Shared.Config import Config

conn = Connection(Config.DB_SECURITY)
repositories = {
    'client_repository': ClientRepository
}
uow = UowFactory.generate(conn.get_session, repositories)

use_case = ClientUseCase(uow)
 
class ClientServicer(Client_pb2_grpc.ClientServicer):
    
    @grpc_response
    async def GetClients(self, request, context):
        return await use_case.get_list_clients(request)
    
 
    @grpc_response
    async def GetClientById(self, request, context):
        return await use_case.get_client_info_by_id(request)