import json
from typing import Dict, Any, List
from src.Shared.Enums.Code import Code
from src.Infrastructure.Grpc.Client.ConnectionClient import ConnectionClient
from Osdental.Exception.ControlledException import OSDException
from Osdental.Shared.Utils.DataUtils import DataUtils


class ConnectionService:

    def __init__(self, connection_client: ConnectionClient):
        self.connection_client = connection_client

    async def get_all_providers_by_ids(
        self, ids_list: List[str]
    ) -> List[Dict[str, Any]]:
        req = json.dumps({"idsProvider": ids_list})
        res = await self.connection_client.get_all_providers_by_ids(req)
        if res.status != Code.PROCESS_SUCCESS_CODE:
            raise OSDException(error=res.message, status_code=res.status)
        raw_data = json.loads(res.data)
        data = []
        for item in raw_data:
            item = DataUtils.normalize_uuids_dict(item)
            data.append(item)
        return data
