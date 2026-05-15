from typing import Dict, Any, List
from .ProviderQueryV2 import ProviderQuery
from dotenv import load_dotenv
from src.Shared.Instances import db_providers
from src.Shared.Enums.Constant import Constant
from src.Domain.Interfaces.ProviderRepositoryInterfaceV2 import (
    ProviderRepositoryInterface,
)

load_dotenv()


class ProviderRepository(ProviderRepositoryInterface):

    def __init__(self):
        self.db = db_providers

    async def get_all_providers(self, id_external, data) -> List[Dict[str, Any]]:
        data[Constant.ID_EXTERNAL] = id_external
        return await self.db.execute_query_return_data(
            ProviderQuery.GET_ALL_PROVIDERS, data
        )

    async def get_groups_by_client(self, id_external) -> List[Dict[str, Any]]:
        params = {Constant.ID_EXTERNAL: id_external}
        return await self.db.execute_query_return_data(
            ProviderQuery.GET_GROUPS_BY_CLIENT, params
        )
