import json
from typing import Dict, Any, List
from src.Shared.Enums.Code import Code
from src.Shared.Enums.Constant import Constant
from src.Infrastructure.Grpc.Client.CatalogClient import CatalogClient
from Osdental.Exception.ControlledException import OSDException


class CatalogService:

    def __init__(self, catalog_client: CatalogClient):
        self.catalog_client = catalog_client

    async def get_catalog_detail_by_id(self, key: str) -> Dict[str, Any]:
        req = json.dumps({Constant.ID_DETAIL_CATALOG: key})
        res = await self.catalog_client.get_catalog_detail_by_id(req)
        if res.status != Code.PROCESS_SUCCESS_CODE:
            raise OSDException(error=res.message, status_code=res.status)
        return json.loads(res.data)

    async def get_catalog_data(self, key: str) -> List[Dict[str, Any]]:
        req = json.dumps({Constant.CATALOG_FIELD_NAME: key})
        res = await self.catalog_client.get_catalog_data(req)
        if res.status != Code.PROCESS_SUCCESS_CODE:
            raise OSDException(error=res.message, status_code=res.status)
        return json.loads(res.data)
