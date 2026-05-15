from urllib import response

from Osdental.Models.Response import Response

# from Osdental.Decorators.AuditLog import handle_audit_and_exception
from src.Shared.Enums.Code import Code
from src.Application.UseCases.Graphql.ProviderUseCase import ProviderUseCase
from src.Infrastructure.Repositories.Provider.ProviderRepository import (
    ProviderRepository,
)
from Osdental.Decorators.SecureResolver import resolver
from graphql import GraphQLResolveInfo

from src.Infrastructure.Graphql.Context import GraphQLContext

use_case = "test"  # @' #.ProviderUseCase(repository=ProviderRepository())


class ProviderResolver:

    @staticmethod
    @resolver()
    async def resolve_get_all_providers(_, info: GraphQLResolveInfo, data):

        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_all_providers(token, data)

    @staticmethod
    @resolver()
    async def resolve_get_types(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_types(token, data)

    @staticmethod
    @resolver()
    async def resolve_get_provider_by_id(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_providers_by_id(token, data)

    @staticmethod
    @resolver()
    async def resolve_get_all_contracts(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_all_contracts(token, data)

        # response = await use_case.get_all_contracts(info=info, aes_data=data)
        # return Response(data=response).send()

    @staticmethod
    @resolver()
    async def resolve_get_contract_by_id(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_contract_by_id(token, data)

    # using a grpc method
    @staticmethod
    @resolver()
    async def resolve_get_users_by_group(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_users_by_group(token, data)

    # used for plataform
    @staticmethod
    @resolver()
    async def resolve_get_groups_by_external_id(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.get_groups_by_external_id(token, data)

    # CREATES

    @staticmethod
    @resolver()
    async def resolve_create_providers_group(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.create_providers_group(token, data)

    @staticmethod
    @resolver()
    async def resolve_save_by_group(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.save_by_group(token, data)

    @staticmethod
    @resolver()
    async def resolve_create_providers_group_contract(
        _, info: GraphQLResolveInfo, data
    ):
        print("teteanso")
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.create_providers_group_contract(
            token, data
        )

    # UPDATES

    @staticmethod
    @resolver()
    async def resolve_update_providers_group_contract(
        _, info: GraphQLResolveInfo, data
    ):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.update_providers_group_contract(
            token, data
        )

    @staticmethod
    @resolver()
    async def resolve_delete_providers_group_contract(
        _, info: GraphQLResolveInfo, data
    ):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.delete_providers_group_contract(
            token, data
        )

    @staticmethod
    @resolver()
    async def resolve_change_provider_status(_, info: GraphQLResolveInfo, data):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.change_provider_status(token, data)

    @staticmethod
    @resolver()
    async def resolve_update_providers_group_contract_status(
        _, info: GraphQLResolveInfo, data
    ):
        context: GraphQLContext = info.context
        token = context.token
        return await context.services.provider.update_providers_group_contract_status(
            token, data
        )
