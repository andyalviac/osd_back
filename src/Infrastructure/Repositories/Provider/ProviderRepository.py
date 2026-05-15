import json
from uuid import UUID
from typing import Dict, Any, List

from fastapi import params
from . import ProviderQuery
from sqlalchemy import text
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from Osdental.Exception.ControlledException import DatabaseException
from src.Shared.Enums.Code import Code
from src.Shared.Enums.Constant import Constant
from src.Shared.Instances import db_providers
from src.Domain.Interfaces.ProviderRepositoryInterface import (
    ProviderRepositoryInterface,
)

from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()
from Osdental.Database.BaseRepository import BaseRepository


class ProviderRepository(BaseRepository, ProviderRepositoryInterface):

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

        # super().__init__(async_session)
        # self.db = db_providers

    async def get_all_providers(
        self,
        external_enterprise_id,
        number_pages,
        total_row,
        search,
        types,
        status,
        order,
        field,
    ) -> List[Dict[str, Any]]:
        if types == "":
            types = None
        params = {
            "external_enterprise_id": external_enterprise_id,
            "number_pages": number_pages,
            "total_row": total_row,
            "search": search,
            "type": types,
            "status": status,
            "order": order,
            "field": field,
        }
        return await self._execute_query(
            ProviderQuery.GET_ALL_PROVIDERS, params=params, many=True, as_dict=True
        )

    async def get_types(self, external_enterprise_id: UUID) -> str:
        params = {
            "external_enterprise_id": external_enterprise_id,
        }

        return await self._execute_query(
            ProviderQuery.GET_TYPES, params=params, many=True, as_dict=True
        )

    async def get_group_by_id(self, id_provider_group: UUID) -> str:
        params = {
            Constant.ID_PROVIDER_GROUP: id_provider_group,
        }
        data = await self._execute_query(
            ProviderQuery.GET_GROUP_BY_ID, params=params, as_dict=True
        )
        if "providersOfGroup" in data and isinstance(data["providersOfGroup"], str):
            try:
                data["providersOfGroup"] = json.loads(data["providersOfGroup"])
            except json.JSONDecodeError:
                data["providersOfGroup"] = []
        return data  # json.dumps(, default=str)

    async def get_providers_by_group(self, id_provider_group: UUID) -> str:
        params = {
            Constant.ID_PROVIDER_GROUP: id_provider_group,
        }

        return await self._execute_query(
            ProviderQuery.GET_PROVIDERS_BY_GROUP, params=params, many=True, as_dict=True
        )

    async def get_providers_by_id(self, id_provider: UUID) -> str:
        params = {"id_provider": id_provider}

        return await self._execute_query(
            ProviderQuery.GET_PROVIDER_BY_ID, params=params
        )

    async def get_all_contracts(self, id_provider_group: UUID) -> List[Dict[str, Any]]:
        params = {Constant.ID_PROVIDER_GROUP: id_provider_group}
        return await self._execute_query(
            ProviderQuery.GET_ALL_CONTRACTS, params=params, many=True, as_dict=True
        )

    async def get_contract_by_id(
        self, id_provider_group_contract: UUID
    ) -> List[Dict[str, Any]]:
        params = {Constant.ID_CONTRACT: id_provider_group_contract}

        return await self._execute_query(
            ProviderQuery.GET_CONTRACT_BY_ID, params=params, as_dict=True
        )

    async def get_all_contracts_rules(self, id_provider_group_contract: UUID) -> str:
        params = {Constant.ID_CONTRACT: id_provider_group_contract}
        return await self._execute_query(
            ProviderQuery.GET_ALL_CONTRACTS_RULES,
            params=params,
            many=True,
            as_dict=True,
        )

    async def get_groups_by_external_id(self, id_external_id: UUID) -> str:
        params = {
            "idExternal": id_external_id,
        }

        return await self._execute_query(
            ProviderQuery.GET_GROUPS_BY_EXTERNAL_ID,
            params=params,
            many=True,
            as_dict=True,
        )

    async def get_overlapped_users_by_group(
        self, data: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        params = {
            Constant.ID_EXTERNAL: data.get(Constant.ID_EXTERNAL),
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
        }
        return await self._execute_query(
            ProviderQuery.GET_OVERLAPPED_USERS_BY_GROUP,
            params=params,
            many=True,
            as_dict=True,
        )

    async def validate_name(
        self,
        group_name: str,
        id_external_enterprise: UUID,
        form_origin: str,
        id_provider_group: UUID,
    ) -> str:

        params = {
            "group_name": group_name,
            Constant.ID_EXTERNAL: id_external_enterprise,
            "formOrigin": form_origin,
            Constant.ID_PROVIDER_GROUP: id_provider_group,
        }

        return await self._execute_query(
            ProviderQuery.VALIDATE_NAME,
            params=params,
            as_dict=True,
        )

    async def delete_group_of_providers(  # session: Session,
        self, id_provider_group: str, user_id: UUID
    ) -> RowMapping:
        params = {
            Constant.ID_PROVIDER_GROUP: id_provider_group,
            "user_id": user_id,
        }

        row = await self._execute_command(
            ProviderQuery.DELETE_GROUP_OF_PROVIDERS, params=params
        )

        ##############################################################################33

        # result = await session.execute(
        #    text(ProviderQuery.DELETE_GROUP_OF_PROVIDERS), params
        # )
        # row = result.fetchone()
        return row

    async def create_new_group_id(
        self,
        data: Dict[str, str],
        user_id: UUID,
        external_enterprise_id: UUID,
    ) -> RowMapping:
        params = {
            "user_id": data.get(Constant.ID_USER),
            "group_name": data.get(Constant.GROUP_NAME),
            "os_type": data.get("osType"),
            "os_specialty": data.get(Constant.SPECIALTY),
            "os_start_date": data.get(Constant.START_DATE),
            "os_end_date": data.get(Constant.END_DATE),
            "payroll_reference_id": data.get("payrollReferenceId"),
            "notes": data.get("notes"),
            "ids_providers": data.get("idsProviders"),
            "formOrigin": data.get("formOrigin"),
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
            "user_id_log": user_id,
            "external_enterprise_id": data.get(Constant.ID_EXTERNAL)
            or external_enterprise_id,
        }
        # result = await session.execute(text(ProviderQuery.CREATE_NEW_GROUP_ID), params)
        # row = result.fetchone()
        # locations_ids_array = dict(zip(result.keys(), row))
        # return locations_ids_array

        row = await self._execute_command(
            ProviderQuery.CREATE_NEW_GROUP_ID, params=params
        )

        print("/////////////", row)

        return row

    async def create_providers_group(
        self,  # session: Session,
        user_id: UUID,
        external_enterprise_id: UUID,
        data: Dict[str, str],
    ) -> RowMapping:
        # Dict
        params = {
            "user_id": data.get(Constant.ID_USER),
            "group_name": data.get(Constant.GROUP_NAME),
            "os_type": data.get("osType"),
            "os_specialty": data.get(Constant.SPECIALTY),
            "os_start_date": data.get(Constant.START_DATE),
            "os_end_date": data.get(Constant.END_DATE),
            "payroll_reference_id": data.get("payrollReferenceId"),
            "notes": data.get("notes"),
            "ids_providers": data.get("idsProviders"),
            "formOrigin": data.get("formOrigin"),
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
            "newIdProviderGroup": data.get("newIdProviderGroup"),
            "user_id_log": user_id,
            "external_enterprise_id": external_enterprise_id,
        }

        # result = await session.execute(
        #    text(ProviderQuery.CREATE_PROVIDERS_GROUP), params
        # )

        provider_group = await self._execute_command(
            ProviderQuery.CREATE_PROVIDERS_GROUP, params=params, as_dict=True
        )
        print("provider_group", provider_group)
        # row = result.fetchone()
        # provider_group = dict(zip(result.keys(), row))
        print("type", type(provider_group))
        if provider_group["STATUS_CODE"] != Code.CREATE_PROVIDER_GROUP:
            raise DatabaseException(
                error=provider_group["STATUS_MESSAGE"],
                status_code=provider_group["STATUS_CODE"],
            )

        return provider_group

    async def save_by_group(
        self, id_provider: str, id_provider_group: str, user_id: UUID
    ) -> RowMapping:

        params = {
            "idProvider": id_provider,
            Constant.ID_PROVIDER_GROUP: id_provider_group,
            "user_id": user_id,
        }

        provider_group = await self._execute_command(
            ProviderQuery.SAVE_BY_GROUP, params=params
        )
        return provider_group

        # return await self.db.execute_query_return_message(
        #    ProviderQuery.SAVE_BY_GROUP, params, Code.CREATE_PROVIDER_GROUPS
        # )

    async def create_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str], status: bool
    ) -> RowMapping:
        params = {
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
            "description": data.get("description"),
            "contractType": data.get("contractType"),
            "cycleFrequency": data.get("cycleFrequency"),
            "startDate": None if not data.get("startDate") else data.get("startDate"),
            "endDate": None if not data.get("endDate") else data.get("endDate"),
            "osCompType": data.get("osCompType"),
            "isDeleted": 0,
            "user_id": user_id,
            "status": status,
        }

        result = await self._execute_command(
            ProviderQuery.CREATE_PROVIDERS_GROUP_CONTRACT,
            params=params,
            as_dict=True,
        )

        if result["STATUS_CODE"] != Code.CREATE_PROVIDER_GROUP_CONTRACT:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"],
                status_code=result["STATUS_CODE"],
                message=result["STATUS_MESSAGE"],
            )

        return result

    async def create_providers_group_contract_rule(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        params = {
            Constant.ID_CONTRACT: data.get(Constant.ID_CONTRACT),
            "rulePriority": data.get("rulePriority"),
            "ruleType": data.get("ruleType"),
            Constant.RULE_PERC: data.get(Constant.RULE_PERC),
            Constant.RULE_AMOUNT: data.get(Constant.RULE_AMOUNT),
            "ruleMin": data.get("ruleMin"),
            "ruleMax": data.get("ruleMax"),
            "ruleFrequency": data.get("ruleFrequency"),
            "startDate": None if not data.get("startDate") else data.get("startDate"),
            "endDate": None if not data.get("endDate") else data.get("endDate"),
            "user_id": user_id,
        }

        result = await self._execute_command(
            ProviderQuery.CREATE_PROVIDERS_GROUP_CONTRACT_RULE,
            params=params,
            as_dict=True,
        )

        if result["STATUS_CODE"] != Code.CREATE_PROVIDER_GROUP:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"], status_code=result["STATUS_CODE"]
            )

    async def update_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str]
    ) -> Dict:
        params = {
            Constant.ID_CONTRACT: data.get(Constant.ID_CONTRACT),
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
            "description": data.get("description"),
            "contractType": data.get("contractType"),
            "cycleFrequency": data.get("cycleFrequency"),
            "startDate": None if not data.get("startDate") else data.get("startDate"),
            "endDate": None if not data.get("endDate") else data.get("endDate"),
            "osCompType": data.get("osCompType"),
            "user_id": user_id,
        }

        result = await self._execute_command(
            ProviderQuery.UPDATE_PROVIDER_GROUP_CONTRACT, params=params, as_dict=True
        )

        if result["STATUS_CODE"] != Code.UPDATE_PROVIDER_GROUPS_CONTRACTS:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"],
                status_code=result["STATUS_CODE"],
                message=result["STATUS_MESSAGE"],
            )
        return result

    async def delete_all_contract_rule(
        self, user_id: UUID, id_provider_group_contract: UUID
    ) -> str:
        params = {
            Constant.ID_CONTRACT: id_provider_group_contract,
            "user_id": user_id,
        }
        result = await self._execute_command(
            ProviderQuery.DELETE_ALL_CONTRACT_RULES, params=params, as_dict=True
        )

        if result["STATUS_CODE"] != Code.DELETE_PROVIDER_GROUPS_CONTRACTS:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"], status_code=result["STATUS_CODE"]
            )

        return result["STATUS_CODE"]

    async def get_contract_rule_by_id(
        self, id_provider_group_contract_rule: UUID
    ) -> RowMapping:
        params = {Constant.ID_RULE: id_provider_group_contract_rule}
        data = await self._execute_query(
            ProviderQuery.GET_CONTRACT_RULE_BY_ID, params=params, as_dict=True
        )
        return data

    async def update_providers_group_contract_rules(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        params = {
            Constant.ID_RULE: data.get(Constant.ID_RULE),
            "rulePriority": data.get("rulePriority"),
            "ruleType": data.get("ruleType"),
            Constant.RULE_PERC: data.get(Constant.RULE_PERC),
            Constant.RULE_AMOUNT: data.get(Constant.RULE_AMOUNT),
            "ruleMin": data.get("ruleMin"),
            "ruleMax": data.get("ruleMax"),
            "ruleFrequency": data.get("ruleFrequency"),
            "startDate": None if not data.get("startDate") else data.get("startDate"),
            "endDate": None if not data.get("endDate") else data.get("endDate"),
            "user_id": user_id,
        }
        result = await self._execute_command(
            ProviderQuery.UPDATE_PROVIDER_GROUP_CONTRACT_RULES,
            params=params,
            as_dict=True,
        )

        if result["STATUS_CODE"] != Code.UPDATE_PROVIDER_GROUPS_CONTRACTS:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"], status_code=result["STATUS_CODE"]
            )

    async def delete_all_contract_rule(
        self, user_id: UUID, id_provider_group_contract: UUID
    ) -> str:
        params = {
            Constant.ID_CONTRACT: id_provider_group_contract,
            "user_id": user_id,
        }
        result = await self._execute_command(
            ProviderQuery.DELETE_ALL_CONTRACT_RULES, params=params, as_dict=True
        )

        if result["STATUS_CODE"] != Code.DELETE_PROVIDER_GROUPS_CONTRACTS:
            raise DatabaseException(
                error=result["STATUS_MESSAGE"], status_code=result["STATUS_CODE"]
            )

        return result

    async def delete_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        params = {
            Constant.ID_CONTRACT: data.get(Constant.ID_CONTRACT),
            "user_id": user_id,
        }
        return await self._execute_command(
            ProviderQuery.DELETE_PROVIDER_GROUP_CONTRACT, params=params
        )

    async def change_provider_status(self, data: Dict[str, str], user_id: UUID) -> str:
        params = {
            "id_provider": data.get("idProvider"),
            "status": data.get("status"),
            "user_id": user_id,
        }
        return await self._execute_command(
            ProviderQuery.CHANGE_PROVIDER_STATUS, params=params
        )

    async def update_providers_group_contract_status(
        self, user_id: UUID, data: Dict[str, str | bool]
    ) -> str:
        params = {
            Constant.ID_CONTRACT: data.get(Constant.ID_CONTRACT),
            Constant.ID_PROVIDER_GROUP: data.get(Constant.ID_PROVIDER_GROUP),
            Constant.CONTRACT_STATUS: data.get(Constant.CONTRACT_STATUS),
            "userId": user_id,
        }
        return await self._execute_command(
            ProviderQuery.UPDATE_PROVIDER_GROUP_CONTRACT_STATUS,
            params=params,
        )

    #######################################################older

    # include GRPC
    async def get_provider_group_data_by_id(self, id_provider_group: UUID) -> str:
        return await self._execute_query(
            ProviderQuery.GET_PROVIDER_GROUP_DATA_BY_ID,
            params={Constant.ID_PROVIDER_GROUP: id_provider_group},
            as_dict=True,
        )

    async def get_provider_groups_by_ids(self, ids_providers_groups: str) -> str:
        return await self._execute_query(
            ProviderQuery.GET_PROVIDERS_GROUPS_BY_IDS,
            params={Constant.IDS_PROVIDERS_GROUPS: ids_providers_groups},
            many=True,
            as_dict=True,
        )
