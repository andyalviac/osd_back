from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy import RowMapping

# from src.Infrastructure.Schemas.Catalog import MasterCatalog, DetailCatalog, SearchCatalog


class ICatalogRepository(ABC):

    @abstractmethod
    async def get_catalog_data(self, catalog_name: str) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_all_master_catalog(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_conn_inputs_fields(
        self, id_providers: str
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_catalog_detail_by_master_id(
        self, master_catalog_id: str
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_catalog_detail_by_id(
        self, catalog_deatil_id: str
    ) -> Dict[str, Any]: ...

    @abstractmethod
    async def inactive_master_catalog(
        self, token_id: str, logged_in_user_id: str, master_catalog_id: str
    ) -> RowMapping: ...

    @abstractmethod
    async def inactive_detail_catalog(
        self, token_id: str, logged_in_user_id: str, detail_catalog_id: str
    ) -> RowMapping: ...

    @abstractmethod
    async def get_all_input_phone_code(self) -> List[Dict[str, Any]]: ...
