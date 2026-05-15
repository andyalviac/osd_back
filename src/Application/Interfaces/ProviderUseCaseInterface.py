from abc import ABC, abstractmethod
from typing import Dict, Union, Any
from uuid import UUID
from Osdental.Models.Token import AuthToken


class ProviderUseCaseInterface(ABC):

    @abstractmethod
    async def get_all_providers(
        self, token: AuthToken, data: Dict[str, str], **kwargs
    ) -> str: ...

    @abstractmethod
    async def get_types(self, token: AuthToken, data: Dict[str, str]) -> str: ...
