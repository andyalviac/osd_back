from sqlalchemy.ext.asyncio import AsyncSession
from src.Infrastructure.Repositories.Provider.ProviderRepository import (
    ProviderRepository,
)
from src.Domain.Ports.IUnitOfWork import IUnitOfWork


class UnitOfWork(IUnitOfWork):

    def __init__(self, session_factory):

        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._provider = None

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
    def provider(self):
        if not self._provider:
            self._provider = ProviderRepository(self._session)

        return self._provider
