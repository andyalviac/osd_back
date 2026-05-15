from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from src.Infrastructure.Graphql import schema
from contextlib import asynccontextmanager
from Osdental.Shared.Logger import logger
from Osdental.Graphql.Extensions.AuditExtension import AuditExtension
from ariadne.asgi.handlers import GraphQLHTTPHandler

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from src.Infrastructure.Bootstrap.Container import Container

import asyncio

from src.Infrastructure.Config.Settings import settings

from Osdental.Models.AuditConfig import AuditConfig
from Osdental.Helpers.AuditDispatcher import AuditDispatcher
from src.Infrastructure.Graphql.Context import get_context_value
import logging
from src.Infrastructure.Grpc.Server import serve

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting up...")
    await Container.startup()
    app.state.container = Container
    app.state.aes_auth = Container.config.aes_key_auth
    app.state.aes_user = Container.config.aes_key_user

    # Audit Config
    audit_config = AuditConfig(
        environment=settings.environment,
        microservice_name=settings.microservice_name,
        microservice_version=settings.microservice_version,
    )

    # Services Bus for Audit
    await Container.az_sb_audit.start()

    # For Audit
    app.state.audit_dispatcher = AuditDispatcher(
        messaging=Container.az_sb_audit,
        storage=Container.az_blob_storage,
        audit_config=audit_config,
    )
    app.state.audit_dispatcher.start()

    # Grpc server
    grpc_task = asyncio.create_task(serve(Container))
    logger.debug("🚀 gRPC server started")

    try:
        yield
    finally:
        grpc_task.cancel()
        try:

            await grpc_task
        except asyncio.CancelledError:
            logger.debug("gRPC server stopped")
            raise


app = FastAPI(lifespan=lifespan)

FastAPIInstrumentor.instrument_app(app)

# Agregar el manejador lifespan al FastAPI
# app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(DBLogMiddleware)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


graphql_app = GraphQL(
    schema,
    context_value=get_context_value,
    introspection=True,
    http_handler=GraphQLHTTPHandler(extensions=[AuditExtension]),
)
app.add_route("/graphql", graphql_app)
