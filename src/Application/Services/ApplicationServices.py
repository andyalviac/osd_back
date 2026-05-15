from src.Infrastructure.Bootstrap.Container import Container

from src.Application.UseCases.Graphql.ProviderUseCase import ProviderUseCase
from src.Application.UseCases.Grpc.ProviderUseCase import (
    ProviderUseCase as GrpcProviderUseCase,
)


class ApplicationServices:

    def __init__(self, container: Container):
        self._provider = None
        self._grpc_provider = None
        self.container = container

    @property
    def provider(self):
        if not self._provider:
            self._provider = ProviderUseCase(
                uow_factory=self.container.uow_factory,
                key_vault=self.container.key_vault,
            )
        return self._provider

    @property
    def grpc_provider(self):
        if not self._grpc_provider:
            self._grpc_provider = GrpcProviderUseCase(
                uow_factory=self.container.uow_factory
            )
        return self._grpc_provider
