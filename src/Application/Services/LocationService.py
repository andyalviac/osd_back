import json
from typing import Dict, Any
from Osdental.Exception.ControlledException import OSDException
from src.Infrastructure.Grpc.Client.LocationClient import LocationClient
from src.Shared.Enums.Code import Code


class LocationService:

    def __init__(self, location_client: LocationClient):
        self.location_client = location_client

    async def get_location_by_id(
        self, id_user: str, id_token: str, id_practice_name: str
    ) -> Dict[str, Any]:

        params = json.dumps(
            {"id_user": id_user, "id_token": id_token, "idLocation": id_practice_name}
        )

        location_name = await self.location_client.get_location_by_id(params)

        if location_name.status != Code.PROCESS_SUCCESS_CODE:
            raise OSDException(
                error=location_name.message, status_code=location_name.status
            )

        return json.loads(location_name.data)
