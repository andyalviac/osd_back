from abc import ABC, abstractmethod
from typing import Dict, Union, List, Any
from uuid import UUID


class ProviderRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_providers(
        self,
        external_enterprise_id: UUID,
        number_pages: Union[int, None],
        total_row: Union[int, None],
        search: Union[str, None],
        types: Union[str, None],
        status: Union[str, None],
        order: Union[str, None],
        field: Union[str, None],
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_providers_by_id(self, id_provider: UUID) -> str: ...

    @abstractmethod
    async def get_group_by_id(self, id_provider_group: UUID) -> str: ...

    @abstractmethod
    async def get_groups_by_external_id(self, id_external_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_providers_by_group(self, id_provider_group: UUID) -> str:
        pass

    @abstractmethod
    async def get_types(self, external_enterprise_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_overlapped_users_by_group(
        self, data: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def delete_group_of_providers(
        self, id_provider_group: str, user_id: UUID
    ) -> str:
        pass

    @abstractmethod
    async def create_new_group_id(
        self, data: Dict[str, str], user_id: UUID, external_enterprise_id: UUID
    ) -> str:
        pass

    @abstractmethod
    async def create_providers_group(
        self, user_id: UUID, external_enterprise_id: UUID, data: Dict[str, str]
    ) -> str:
        pass

    @abstractmethod
    async def validate_name(
        self,
        group_name: str,
        id_external_enterprise: UUID,
        form_origin: str,
        id_provider_group: UUID,
    ) -> str:
        pass

    @abstractmethod
    async def save_by_group(
        self, id_provider: str, id_provider_group: str, user_id: UUID
    ) -> str:
        pass

    @abstractmethod
    async def change_provider_status(self, data: Dict[str, str], user_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_all_contracts(self, id_provider_group: UUID) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_contract_by_id(self, id_provider_group_contract: UUID) -> str:
        pass

    @abstractmethod
    async def get_all_contracts_rules(self, id_provider_group_contract: UUID) -> str:
        pass

    @abstractmethod
    async def get_contract_rule_by_id(
        self, id_provider_group_contract_rule: UUID
    ) -> str:
        pass

    @abstractmethod
    async def create_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str], status: bool
    ) -> str:
        pass

    @abstractmethod
    async def create_providers_group_contract_rule(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        pass

    @abstractmethod
    async def update_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        pass

    @abstractmethod
    async def update_providers_group_contract_rules(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        pass

    @abstractmethod
    async def delete_providers_group_contract(
        self, user_id: UUID, data: Dict[str, str]
    ) -> str:
        pass

    @abstractmethod
    async def delete_all_contract_rule(
        self, user_id: UUID, id_provider_group_contract: UUID
    ) -> str:
        pass

    @abstractmethod
    async def update_providers_group_contract_status(
        self, user_id: UUID, data: Dict[str, Union[str, bool]]
    ) -> str:
        pass

    # with grpc
    @abstractmethod
    async def get_provider_group_data_by_id(self, id_provider_group: UUID) -> str:
        pass

    @abstractmethod
    async def get_provider_groups_by_ids(self, id_provider_group: str) -> str:
        pass
