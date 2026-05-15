import json
from typing import Dict, Any, List, Callable
from Osdental.Models.Token import AuthToken
from Osdental.Shared.Utils.DataUtils import DataUtils
from src.Shared.Enums.Code import Code
from src.Shared.Enums.Constant import Constant
from src.Shared.Instances import aes, redis  # , db_providers   ,
from src.Shared.Utils import decriptar, get_id_external, custom_serializer
from src.Infrastructure.Grpc.Client.UserClient import UserClient
from src.Infrastructure.Grpc.Client.CatalogClient import CatalogClient
from src.Infrastructure.Grpc.Client.ConnectionClient import ConnectionClient
from src.Application.Services.ConnectionService import ConnectionService
from src.Application.Services.CatalogService import CatalogService
from src.Application.Services.UserService import UserService
from src.Application.Interfaces.ProviderUseCaseInterface import ProviderUseCaseInterface
from src.Domain.Interfaces.ProviderRepositoryInterface import (
    ProviderRepositoryInterface,
)

from Osdental.Models.Response import Response
from Osdental.Helpers.KeyVaultService import AzureKeyVaultSecretProvider

from src.Domain.Ports.IUnitOfWork import IUnitOfWork


class ProviderUseCase(ProviderUseCaseInterface):

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        key_vault: AzureKeyVaultSecretProvider,
    ):
        self.aes = aes
        self.uow_factory = uow_factory
        self.key_vault = key_vault
        self.redis = redis

    async def fill_providers(self, providers: List[Dict[str, Any]]) -> None:
        specialties_cache = {}
        for provider in providers:
            # Fill specialty name
            specialty = provider.get(Constant.SPECIALTY)
            if specialty and specialty not in specialties_cache:
                async with CatalogClient() as catalog_client:
                    catalog_service = CatalogService(catalog_client)
                    detail_item = await catalog_service.get_catalog_detail_by_id(
                        specialty
                    )
                    specialties_cache[specialty] = detail_item.get(
                        Constant.CATALOG_FIELD_VALUE
                    )
            if specialty:
                provider[Constant.SPECIALTY] = specialties_cache[specialty]

        # Fill pms names
        pms_sources = {provider.get(Constant.PMS_SOURCE) for provider in providers}
        pms_sources.discard(None)

        # if not pms_sources:
        #    return
        # async with ConnectionClient() as connection_client:
        #    connection_service = ConnectionService(connection_client)
        #    pms_list = await connection_service.get_all_providers_by_ids(
        #        list(pms_sources)
        #    )
        #    if pms_list and isinstance(pms_list, List):
        #        for pms in pms_list:
        #            for provider in providers:
        #                if provider.get(Constant.PMS_SOURCE) == pms.get(
        #                    Constant.ID_PROVIDER
        #                ):
        #                    provider[Constant.PMS_NAME] = pms.get("name")

    async def get_all_providers(
        self, token: AuthToken, data: Dict[str, str], **kwargs
    ) -> Response:

        redis_key = Constant.REDIS_PROVIDERS_KEY
        id_external_enterprise = get_id_external(token, data)
        page_number = data.get(Constant.REQUEST_PAGE_NUMBER, 1)
        page_size = data.get(Constant.REQUEST_PAGE_SIZE)
        search = data.get(Constant.REQUEST_SEARCH, "")
        provider_type = data.get(Constant.REQUEST_TYPE, "")
        status = data.get(Constant.REQUEST_STATUS, "")
        order = data.get(Constant.REQUEST_ORDER, "")
        field = data.get(Constant.REQUEST_FIELD, "")
        cache_key = f"{redis_key}:{id_external_enterprise}:{page_number}:{search}:{provider_type}:{status}:{order}:{field}"
        response_cache = await self.redis.exists(cache_key)

        if response_cache:
            return Response(data=await self.redis.get_str(cache_key))
        async with self.uow_factory() as uow:
            all_providers = await uow.provider.get_all_providers(
                id_external_enterprise,
                page_number,
                page_size,
                search,
                provider_type,
                status,
                order,
                field,
            )

        if all_providers:
            await self.fill_providers(all_providers)
            all_providers = json.dumps(all_providers, default=custom_serializer)
            all_providers = self.aes.encrypt(token.aes_key_auth, all_providers)
            await self.redis.set_str(cache_key, all_providers, Constant.REDIS_TTL)

        return Response(data=all_providers)

    async def get_types(self, token: AuthToken, data: Dict[str, str]) -> Response:
        id_external_enterprise = get_id_external(token, data)
        async with self.uow_factory() as uow:
            specialty_types_existing = await uow.provider.get_types(
                id_external_enterprise
            )
            specialty_types_existing = self.aes.encrypt(
                token.aes_key_auth, specialty_types_existing
            )
        return Response(data=specialty_types_existing)

    async def get_providers_by_id(
        self, token: AuthToken, data: Dict[str, str]
    ) -> Response:

        if data.get(Constant.ID_PROVIDER_GROUP):
            async with self.uow_factory() as uow:

                provider_group = await uow.provider.get_group_by_id(
                    data.get(Constant.ID_PROVIDER_GROUP)
                )

                providers_in_group = await uow.provider.get_providers_by_group(
                    data.get(Constant.ID_PROVIDER_GROUP)
                )

            provider_group["providersOfGroup"] = providers_in_group

            response = self.aes.encrypt(token.aes_key_auth, provider_group)
        else:
            async with self.uow_factory() as uow:

                provider = await uow.provider.get_providers_by_id(
                    data.get("idProvider")
                )
            response = self.aes.encrypt(token.aes_key_auth, provider)
        return Response(data=response)

    async def get_all_contracts(
        self, token: AuthToken, data: Dict[str, str]
    ) -> Response:
        redis_key = Constant.REDIS_CONTRACTS_KEY
        id_provider_group = data.get(Constant.ID_PROVIDER_GROUP, "")
        cache_key = f"{redis_key}:{id_provider_group}"
        response_cache = await self.redis.exists(cache_key)
        if response_cache:
            return Response(data=await self.redis.get_str(cache_key))
        async with self.uow_factory() as uow:
            all_contracts = await uow.provider.get_all_contracts(id_provider_group)

            all_contracts = self.aes.encrypt(token.aes_key_auth, all_contracts)
            await self.redis.set_str(cache_key, all_contracts, Constant.REDIS_TTL)

        return Response(data=all_contracts)

    async def get_contract_by_id(
        self, token: AuthToken, data: Dict[str, str]
    ) -> Response:
        redis_key = Constant.REDIS_CONTRACT_KEY
        id_contract = data.get(Constant.ID_CONTRACT, "")
        cache_key = f"{redis_key}:{id_contract}"
        response_cache = await self.redis.exists(cache_key)
        if response_cache:
            return Response(data=await self.redis.get_str(cache_key))
        async with self.uow_factory() as uow:
            contract = await uow.provider.get_contract_by_id(id_contract)
            contracts_rules = await uow.provider.get_all_contracts_rules(id_contract)
        contract["contractsRules"] = contracts_rules
        if contract:
            contract = self.aes.encrypt(token.aes_key_auth, contract)
            await self.redis.set_str(cache_key, contract, Constant.REDIS_TTL)
        return Response(data=contract)

    async def get_groups_by_external_id(
        self, token: AuthToken, data: Dict[str, str]
    ) -> Response:
        async with self.uow_factory() as uow:
            groups = await uow.provider.get_groups_by_external_id(
                token.id_external_enterprise
            )
            groups = self.aes.encrypt(token.aes_key_auth, groups)
        return Response(data=groups)

    async def get_users_by_group(
        self, token: AuthToken, data: Dict[str, str]
    ) -> Response:

        id_external = token.base_id_external_enterprise
        async with UserClient() as user_client:
            user_service = UserService(user_client)
            all_users = await user_service.get_users_by_client(id_external)
        async with self.uow_factory() as uow:
            overlapped_users = await uow.provider.get_overlapped_users_by_group(data)
            overlapped_user_ids = {ou[Constant.ID_USER] for ou in overlapped_users}
            users = [
                user
                for user in all_users
                if user.get(Constant.DROPDOWN_FIELD_VALUE) not in overlapped_user_ids
            ]
            return Response(data=self.aes.encrypt(token.aes_key_auth, users))

    async def _clear_providers_cache(self):
        await self.redis.clear_cache(f"{Constant.REDIS_PROVIDERS_KEY}:")

    async def create_providers_group(
        self, token: AuthToken, data: Dict[str, Any]
    ) -> Response:
        await self._clear_providers_cache()
        async with self.uow_factory() as uow:
            providers = data.get("providersOfGroup", [])
            data["idsProviders"] = ",".join(
                [provider[Constant.ID_PROVIDER] for provider in providers]
            )
            name_exist = await uow.provider.validate_name(
                data.get(Constant.GROUP_NAME),
                token.id_external_enterprise,
                data["formOrigin"],
                data.get(Constant.ID_PROVIDER_GROUP),
            )

            if name_exist["STATUS_CODE"] != Code.PROVIDER_NAME_NO_EXIST:
                return Response(
                    data=self.aes.encrypt(
                        token.aes_key_auth,
                        {Constant.ID_PROVIDER_GROUP: name_exist["DATA"]},
                    ),
                    status=name_exist["STATUS_CODE"],
                    message=name_exist["STATUS_MESSAGE"],
                )

            if data["formOrigin"] == "update":
                await uow.provider.delete_group_of_providers(
                    data[Constant.ID_PROVIDER_GROUP], token.id_user
                )

                new_id_provider_group = None
            else:
                new_group_id = await uow.provider.create_new_group_id(
                    data, token.id_user, token.id_external_enterprise
                )
                new_id_provider_group = new_group_id.get("DATA")
            if providers:

                for provider in providers:
                    data_copy = data.copy()
                    data_copy["idsProviders"] = provider[Constant.ID_PROVIDER]
                    data_copy["newIdProviderGroup"] = new_id_provider_group
                    provider = await uow.provider.create_providers_group(
                        token.id_user, token.id_external_enterprise, data_copy
                    )

            if data.get("formOrigin") == "new":
                return Response(
                    data=self.aes.encrypt(
                        token.aes_key_auth,
                        {Constant.ID_PROVIDER_GROUP: provider["DATA"]},
                    ),
                    status=provider["STATUS_CODE"],
                    message=provider["STATUS_MESSAGE"],
                )
            else:
                return Response(
                    data=self.aes.encrypt(
                        token.aes_key_auth, {Constant.ID_PROVIDER_GROUP: ""}
                    ),
                    status=provider["STATUS_CODE"],
                    message=provider["STATUS_MESSAGE"],
                )

    async def save_by_group(self, token: AuthToken, data: Dict[str, Any]) -> Response:

        user_id = token.id_user
        await self._clear_providers_cache()
        async with self.uow_factory() as uow:
            if isinstance(data, str):
                data_dict = json.loads(data)
            elif isinstance(data, dict):
                data_dict = data
            providers_data = data_dict.get("providersData", [])
            for item in providers_data:
                id_provider = item.get("idProvider", Constant.GUID_EMPTY)
                id_provider_group = item.get(
                    Constant.ID_PROVIDER_GROUP, Constant.GUID_EMPTY
                )
                result = await uow.provider.save_by_group(
                    id_provider, id_provider_group, user_id
                )

            return Response(status=Code.CREATE_PROVIDER_GROUPS, message=result)

    async def create_providers_group_contract(
        self, token: AuthToken, data: str
    ) -> Response:
        print("////////////////////aqui ")
        print(type(data))
        if isinstance(data, str):
            data_dict = json.loads(data)
        elif isinstance(data, dict):
            data_dict = data
        providers_data = data_dict.get("contractsRules", [])
        async with self.uow_factory() as uow:
            print(data)
            all_contracts = await uow.provider.get_all_contracts(
                data.get("idProviderGroup")
            )
            all_contracts = [
                contract
                for contract in all_contracts
                if contract[Constant.CONTRACT_STATUS] == True
            ]

            print("all_contracts", all_contracts)
            all_contracts.append(data)
            print("all_contracts2", all_contracts)
            status = True
            if len(all_contracts) > 1:
                exceed_max = await self.exceed_max_active_contracts(all_contracts)
                print("exceed_max", exceed_max)
                if exceed_max:
                    status = False

            result_data = await uow.provider.create_providers_group_contract(
                token.id_user, data, status
            )
            redis_key = Constant.REDIS_CONTRACTS_KEY
            id_provider_group = data_dict.get(Constant.ID_PROVIDER_GROUP, "")
            cache_key = f"{redis_key}:{id_provider_group}"
            await self.redis.delete(cache_key)

            if isinstance(result_data, str):
                result_data = json.loads(result_data)
            if (
                result_data["STATUS_CODE"] == Code.PROVIDER_GORUP_NAME_ALREADY_EXISTS
                or result_data["STATUS_CODE"] == Code.CONTRACT_DATES_ALREADY_EXISTS
            ):
                return Response(
                    data=self.aes.encrypt(token.aes_key_auth, {"data": ""}),
                    status=result_data["STATUS_CODE"],
                    message=result_data["STATUS_MESSAGE"],
                )
            result_id = result_data["DATA"]
            for item in providers_data:
                item[Constant.ID_CONTRACT] = result_id
                await uow.provider.create_providers_group_contract_rule(
                    token.id_user, item
                )
            return Response(
                data=self.aes.encrypt(
                    token.aes_key_auth,
                    {Constant.ID_PROVIDER_GROUP: result_data["DATA"]},
                ),
                status=result_data["STATUS_CODE"],
                message=result_data["STATUS_MESSAGE"],
            )

    async def update_providers_group_contract(
        self, token: AuthToken, data: str, **kwargs
    ) -> Response:

        data_dict = json.loads(data) if isinstance(data, str) else data

        providers_data = data_dict.get("contractsRules", [])
        redis_key = Constant.REDIS_CONTRACTS_KEY
        id_provider_group = data_dict.get(Constant.ID_PROVIDER_GROUP, "")
        cache_key = f"{redis_key}:{id_provider_group}"
        await self.redis.delete(cache_key)
        await self.redis.delete(
            f"{Constant.REDIS_CONTRACT_KEY}:{data_dict.get(Constant.ID_CONTRACT)}"
        )
        async with self.uow_factory() as uow:
            result = await uow.provider.update_providers_group_contract(
                token.id_user, data
            )
            result_data = result
            if isinstance(result_data, str):
                result_data = json.loads(result_data)
            if (
                result_data["STATUS_CODE"] == Code.CONTRACT_NAME_ALREADY_EXISTS
                or result_data["STATUS_CODE"] == Code.CONTRACT_DATES_ALREADY_EXISTS
            ):
                return Response(
                    data=self.aes.encrypt(token.aes_key_auth, {"data": ""}),
                    status=result_data["STATUS_CODE"],
                    message=result_data["STATUS_MESSAGE"],
                )
            await uow.provider.delete_all_contract_rule(
                token.id_user, data_dict.get(Constant.ID_CONTRACT)
            )

            for item in providers_data:
                if item.get(Constant.ID_RULE):
                    exist_rule = await uow.provider.get_contract_rule_by_id(
                        item.get(Constant.ID_RULE)
                    )

                    if isinstance(exist_rule, str):
                        exist_rule = json.loads(exist_rule)
                    if exist_rule["STATUS_CODE"] == Code.PROCESS_EXECUTED_SUCCESSFULLY:
                        await uow.provider.update_providers_group_contract_rules(
                            token.id_user, item
                        )

                    else:
                        item[Constant.ID_CONTRACT] = data_dict.get(Constant.ID_CONTRACT)
                        await uow.provider.create_providers_group_contract_rule(
                            token.id_user, item
                        )
                else:
                    item[Constant.ID_CONTRACT] = data_dict.get(Constant.ID_CONTRACT)
                    await uow.provider.create_providers_group_contract_rule(
                        token.id_user, item
                    )

                return Response(
                    data="",
                    status=result_data["STATUS_CODE"],
                    message=result_data["STATUS_MESSAGE"],
                )

    async def delete_providers_group_contract(
        self, token: AuthToken, data: str, **kwargs
    ) -> Response:
        async with self.uow_factory() as uow:
            result = await uow.provider.delete_providers_group_contract(
                token.id_user, data
            )

        await self.redis.clear_cache(f"{Constant.REDIS_CONTRACTS_KEY}:")
        return Response(status=result["STATUS_CODE"], message=result["STATUS_MESSAGE"])

    async def change_provider_status(
        self, token: AuthToken, data, **kwargs
    ) -> Response:
        await self._clear_providers_cache()

        async with self.uow_factory() as uow:
            response = await uow.provider.change_provider_status(data, token.id_user)
            return Response(
                status=response["STATUS_CODE"], message=response["STATUS_MESSAGE"]
            )

    async def exceed_max_active_contracts(self, all_contracts: Dict[str, Any]) -> bool:
        async with CatalogClient() as catalog_client:
            catalog_service = CatalogService(catalog_client)
            catalog = await catalog_service.get_catalog_data(
                Constant.CATALOG_CONTRACT_TYPES
            )
            has_1099 = False
            has_w2 = False
            has_true_up = False
            has_deduction = False
            for contract in all_contracts:
                id_type = contract[Constant.CONTRACT_TYPE]
                contract_type = next(
                    (
                        item
                        for item in catalog
                        if item[Constant.CATALOG_FIELD_ID] == id_type
                    ),
                    None,
                )
                if (
                    not (has_1099)
                    and contract_type[Constant.CATALOG_FIELD_CODE].find("1099") != -1
                ):
                    has_1099 = True
                elif (
                    not (has_w2)
                    and contract_type[Constant.CATALOG_FIELD_CODE].find("W2") != -1
                ):
                    has_w2 = True
                elif (
                    not (has_true_up)
                    and contract_type[Constant.CATALOG_FIELD_CODE].find(
                        Constant.CODE_TRUE_UP
                    )
                    != -1
                ):
                    has_true_up = True
                elif (
                    not (has_deduction)
                    and contract_type[Constant.CATALOG_FIELD_CODE].find("DEDUCTION")
                    != -1
                ):
                    has_deduction = True
                else:
                    return True
            return False

    async def update_providers_group_contract_status(
        self, token: AuthToken, data, **kwargs
    ) -> Response:

        id_provider_group = data.get(Constant.ID_PROVIDER_GROUP)
        id_contract = data.get(Constant.ID_CONTRACT)
        contract_new_status = data.get(Constant.CONTRACT_STATUS)
        cache_key = f"{Constant.REDIS_CONTRACTS_KEY}:{id_provider_group}"
        await self.redis.delete(cache_key)
        cache_key_id_provider_group_contract = (
            f"{Constant.REDIS_CONTRACT_KEY}:{id_contract}"
        )
        await self.redis.delete(cache_key_id_provider_group_contract)
        async with self.uow_factory() as uow:

            if contract_new_status:
                all_contracts = await uow.provider.get_all_contracts(id_provider_group)
                # all_contracts = await self.repository.get_all_contracts(id_provider_group)
                # Filter out ACTIVE contracts including the one trying to update
                all_contracts = [
                    contract
                    for contract in all_contracts
                    if contract[Constant.CONTRACT_STATUS] == True
                    or contract[Constant.ID_CONTRACT] == id_contract
                ]
                if len(all_contracts) > 1:
                    exceed_max = await self.exceed_max_active_contracts(all_contracts)
                    if exceed_max:
                        return Response(
                            data="",
                            status=Code.UPDATE_CONTRACT_STATUS_MAX_CONTRACTS_CODE,
                            message=Code.UPDATE_CONTRACT_STATUS_MAX_CONTRACTS_MSG,
                        )

            result = await uow.provider.update_providers_group_contract_status(
                token.id_user, data
            )
            result_data = result
            if isinstance(result_data, str):
                result_data = json.loads(result_data)

            return Response(
                data="",
                status=result_data["STATUS_CODE"],
                message=result_data["STATUS_MESSAGE"],
            )
