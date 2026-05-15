from fastapi import Request
from Osdental.Graphql.Models import BaseGraphQLContext
from src.Infrastructure.Bootstrap.Container import Container
from src.Application.Services.ApplicationServices import ApplicationServices


class GraphQLContext(BaseGraphQLContext):

    def __init__(self, request: Request, container: Container, access_token: str):
        super().__init__(request, container)
        self.services = ApplicationServices(container)
        self.access_token = access_token


def get_context_value(request: Request, _: dict):
    container = request.app.state.container
    access_token: str = request.headers.get("accesstoken")
    # print(f"Access token in context: {access_token}")
    # print(f"Container in context: {container}")
    return GraphQLContext(
        request=request, container=container, access_token=access_token
    )
