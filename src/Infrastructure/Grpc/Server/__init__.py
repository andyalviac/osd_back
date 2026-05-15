import asyncio
import grpc
from grpc_reflection.v1alpha import reflection
from src.Infrastructure.Grpc.Generated import (
    Catalog_pb2_grpc,
    Catalog_pb2,
    Provider_pb2,
    Provider_pb2_grpc,
)
from ..Servicer.ProviderServicer import ProviderServicer
from src.Infrastructure.Bootstrap.Container import Container


async def serve(container):
    server = grpc.aio.server()
    provider_servicer = ProviderServicer(container)

    # Catalog_pb2_grpc.add_CatalogServicer_to_server(catalog_servicer, server)
    Provider_pb2_grpc.add_ProviderServicer_to_server(provider_servicer, server)

    SERVICE_NAMES = (
        Provider_pb2.DESCRIPTOR.services_by_name["Provider"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("0.0.0.0:50052")
    await server.start()
    try:
        await server.wait_for_termination()
    except asyncio.CancelledError:
        await server.stop(grace=5)
        raise
