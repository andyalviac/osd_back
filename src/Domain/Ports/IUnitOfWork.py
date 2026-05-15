from abc import ABC, abstractmethod

from src.Domain.Interfaces.ProviderRepositoryInterface import (
    ProviderRepositoryInterface,
)


class IUnitOfWork(ABC):
    # Los repositorios son accesibles a través del UoW
    # audit: IAuditLogRepository
    # catalog: ICatalogRepository
    provider: ProviderRepositoryInterface
    # i_form: IIntegrationFormRepository

    # __aenter__ se ejecuta cuando pones: "async with uow:"
    async def __aenter__(self):
        return self

    # __aexit__ se ejecuta al salir del bloque "async with", incluso si hubo error
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Por defecto, si hay error, hacemos rollback
        pass

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
