from src.Domain.Interfaces.CycleRepositoryInterface import CycleRepositoryInterface
from typing import Dict, List, Any
from src.Shared.Enums.Constant import (
    Constant,
    CYCLE_STATUS_CODES,
    CYCLE_STATUS_CODES_REVERSE,
)

from src.Infrastructure.Grpc.Client.UserClient import UserClient

from src.Application.Services.UserService import UserService
import json
from src.Shared.Utils import custom_serializer


class CycleService:
    def __init__(self, repository: CycleRepositoryInterface, queue, connection_string):
        self.repository = repository
        self.queue = queue
        self.connection_string = connection_string

    async def get_all_cycles_by_external(self, data):

        all_cycles_by_external = await self.repository.get_all_cycles_by_external(data)
        if isinstance(all_cycles_by_external, List):
            user_names_cache = {}
            for item in all_cycles_by_external:
                await CycleService._format_cycle(self, item, user_names_cache)

        all_cycles_by_external = json.dumps(
            all_cycles_by_external, default=custom_serializer
        )
        return all_cycles_by_external

    async def get_all_cycles_by_externalv2(self, data):

        status = data.get(Constant.CYCLE_STATUS, 0)

        if isinstance(status, bool):
            # Caso True / False
            data[Constant.REQUEST_STATUS] = 0 if status else 7
        elif isinstance(status, int) and 0 <= status <= 7:
            # Ya es un número válido, lo dejamos igual
            data[Constant.REQUEST_STATUS] = status
        else:
            # Si viene otra cosa (string, None, etc.), usamos default 0 (ALL)
            data[Constant.REQUEST_STATUS] = 0

        all_cycles_by_external = await self.repository.get_all_cycles_by_externalv2(
            data
        )
        if isinstance(all_cycles_by_external, List):
            user_names_cache = {}
            for item in all_cycles_by_external:
                await CycleService._format_cyclev2(self, item, user_names_cache)

        all_cycles_by_external = json.dumps(
            all_cycles_by_external, default=custom_serializer
        )
        return all_cycles_by_external

    async def _format_cycle(self, item: Dict, user_names_cache: Dict) -> None:
        """
        Enrich a cycle item with resolved display values for rendering.
        """
        ids_for_send = [
            type_id.strip()
            for type_id in str(item.get(Constant.ID_CYCLE_TYPES, "")).split(",")
            if type_id.strip()
        ]
        item[Constant.ID_CYCLE_TYPES] = ids_for_send
        await CycleService._fill_author_fields(self, item, user_names_cache)

    async def _format_cyclev2(self, item: Dict, user_names_cache: Dict) -> None:
        """
        Enrich a cycle item with resolved display values for rendering.
        """
        ids_for_send = [
            type_id.strip()
            for type_id in str(item.get(Constant.ID_CYCLE_TYPES, "")).split(",")
            if type_id.strip()
        ]
        item[Constant.ID_CYCLE_TYPES] = ids_for_send
        await CycleService._fill_author_fields(self, item, user_names_cache)
        CycleService._set_codes_for_status_cycle(self, item)

    async def _fill_author_fields(self, item: Dict, cache: Dict) -> None:
        async with UserClient() as user_client:
            user_service = UserService(user_client)
            for field in self.author_fields:
                id_user = item.get(field)
                if id_user:
                    if id_user not in cache:
                        cache[id_user] = await user_service.get_user_by_id(id_user)
                    item[field] = cache[id_user]

    def _set_codes_for_status_cycle(self, item: Dict) -> None:
        """
        replace the status codes with the corresponding code in CYCLE_STATUS_CODES
        """
        status_code = item.get(Constant.CYCLE_STATUS)
        if status_code in CYCLE_STATUS_CODES:
            item[Constant.CYCLE_STATUS] = CYCLE_STATUS_CODES[status_code]
        else:
            item[Constant.CYCLE_STATUS] = "Unknown"
