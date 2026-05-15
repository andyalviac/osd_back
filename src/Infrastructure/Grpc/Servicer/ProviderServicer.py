# from Osdental.Decorators.Grpc import grpc_response
import json
from src.Infrastructure.Grpc.Generated import Provider_pb2_grpc, Common_pb2
from src.Application.UseCases.Grpc.ProviderUseCase import ProviderUseCase
from src.Infrastructure.Repositories.Provider.ProviderRepository import (
    ProviderRepository,
)
from src.Application.Services.ApplicationServices import ApplicationServices

from src.Infrastructure.Grpc.Decorators import rpc_handler

# use_case = ProviderUseCase(repository=ProviderRepository())


class ProviderServicer(Provider_pb2_grpc.ProviderServicer):

    def __init__(self, container):
        self.container = container

    @rpc_handler
    async def GetAllProvidersByGroup(self, request, context):
        app = ApplicationServices(self.container)
        return await app.grpc_provider.get_provider_group_data_by_id(request)

    @rpc_handler
    async def GetProviderGroupsByIds(self, request, context):
        app = ApplicationServices(self.container)
        return await app.grpc_provider.get_provider_groups_by_ids(request)
        # response = await use_case.get_provider_groups_by_ids(request)
        # if isinstance(response, str):
        #    response = json.loads(response)
        # return {
        #    "data": response["data"],
        #    "status": response["status"],
        #    "message": response["message"],
        # }

    @rpc_handler
    async def GetProviderGroupsByClient(self, request, context):
        app = ApplicationServices(self.container)
        return await app.grpc_provider.get_groups_by_external_id(request)
        # response = await use_case.get_groups_by_external_id(request)
        # if isinstance(response, str):
        #    response = json.loads(response)
        # return {
        #    "data": response["data"],
        #    "status": response["status"],
        #    "message": response["message"],
        # }
