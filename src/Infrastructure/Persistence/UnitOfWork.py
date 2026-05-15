from sqlalchemy.ext.asyncio import AsyncSession
from src.Infrastructure.Repositories.Provider.ProviderRepository import (
    ProviderRepository,
)
from src.Domain.Ports.IUnitOfWork import IUnitOfWork
from src.Infrastructure.Repositories.AuditLog.AuditLogRepository import (
    AuditLogRepository,
)

# from src.Infrastructure.Repositories.Catalog.CatalogRepository import CatalogRepository
from src.Infrastructure.Repositories.IntegrationForm.IntegrationFormRepository import (
    IntegrationFormRepository,
)


class UnitOfWork(IUnitOfWork):

    def __init__(self, session_factory):

        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._provider = None
        self._audit = None
        self._catalog = None
        self._i_form = None

    async def __aenter__(self):

        self._session = self._session_factory()

        return self

    async def __aexit__(self, exc_type, exc, tb):

        try:

            if exc:
                await self.rollback()
            else:
                await self.commit()

        finally:

            await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    @property
    def audit(self):
        if not self._audit:
            self._audit = AuditLogRepository(self._session)

        return self._audit

    @property
    def catalog(self):
        if not self._provider:
            self._catalog = ProviderRepository(self._session)

        return self._catalog

    @property
    def provider(self):
        if not self._provider:
            self._provider = ProviderRepository(self._session)

        return self._provider

    @property
    def i_form(self):
        if not self._i_form:
            self._i_form = IntegrationFormRepository(self._session)

        return self._i_form
