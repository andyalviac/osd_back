import json
from typing import Dict
from Osdental.Models.Response import Response
from src.Shared.Enums.Constant import Constant
from src.Application.Interfaces.ProviderUseCaseInterface import ProviderUseCaseInterface
from src.Domain.Interfaces.ProviderRepositoryInterface import (
    ProviderRepositoryInterface,
)
from src.Domain.Ports.IUnitOfWork import IUnitOfWork
from typing import Dict, Callable


class ProviderUseCase:

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]):
        self.uow_factory = uow_factory

    async def get_provider_group_data_by_id(self, request) -> str:
        if isinstance(request, str):
            request = json.loads(request)
        async with self.uow_factory() as uow:
            provider_group_data = await uow.provider.get_provider_group_data_by_id(
                request[Constant.ID_PROVIDER_GROUP]
            )
            print("providers", provider_group_data)
            return Response(data=json.dumps(provider_group_data)).send()

    async def get_provider_groups_by_ids(self, request) -> str:
        if isinstance(request, str):
            request = json.loads(request)
        async with self.uow_factory() as uow:
            provider_group_data = await uow.provider.get_provider_groups_by_ids(
                request[Constant.IDS_PROVIDERS_GROUPS]
            )
            return Response(data=json.dumps(provider_group_data)).send()

    async def get_groups_by_external_id(self, request, **kwargs) -> str:
        if isinstance(request, str):
            request = json.loads(request)
        async with self.uow_factory() as uow:
            groups = await uow.provider.get_groups_by_external_id(
                request.get(Constant.ID_EXTERNAL)
            )
            return Response(data=json.dumps(groups)).send()

    async def get_all_providers(self, *args, **kwargs) -> str: ...

    async def get_groups_by_logged_user(self, *args) -> str: ...

    async def get_providers_by_id(self, *args, **kwargs) -> str: ...

    async def get_types(self, *args, **kwargs) -> str: ...

    async def create_providers_group(self, *args, **kwargs) -> Dict[str, str]: ...

    async def save_by_group(self, *args, **kwargs) -> str: ...

    async def change_provider_status(self, *args, **kwargs) -> str: ...

    async def get_all_contracts(self, *args, **kwargs) -> str: ...

    async def get_contract_by_id(self, *args, **kwargs) -> str: ...

    async def create_providers_group_contract(
        self, *args, **kwargs
    ) -> Dict[str, str]: ...

    async def update_providers_group_contract(
        self, *args, **kwargs
    ) -> Dict[str, str]: ...

    async def delete_providers_group_contract(self, *args, **kwargs) -> str: ...

    async def update_providers_group_contract_status(
        self, *args, **kwargs
    ) -> Dict[str, str]: ...

    async def get_provider_groups_by_client(self, request) -> str: ...
