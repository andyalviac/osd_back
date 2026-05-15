from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

# from src.Infrastructure.Schemas.IntegrationForm import IntegrationForm


class IIntegrationFormRepository(ABC):

    @abstractmethod
    async def get_integration_form_resource_by_provider_id(
        self, provider_id: str, form_type: Optional[str] = None
    ) -> List[Dict[str, Any]]: ...

    # @abstractmethod
    # async def create_integration_provider_form(self, user_id: str, data: List[IntegrationForm], provider_id: str = None) -> None: ...

    @abstractmethod
    async def provider_has_integration_form(self, provider_id: str) -> bool: ...
