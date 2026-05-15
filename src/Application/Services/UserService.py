import json
from typing import List, Dict, Any
from src.Shared.Enums.Constant import Constant
from src.Infrastructure.Grpc.Client.UserClient import UserClient


class UserService:

    def __init__(self, user_client: UserClient):
        self.user_client = user_client

    async def get_user_by_id(self, id_user: str) -> Dict[str, Any]:
        params = json.dumps({Constant.ID_USER: id_user})
        user = await self.user_client.get_user_by_id(params)
        if user.data:
            data = json.loads(user.data)
            name = data.get("userFullName")
            return name
        return None

    async def get_users_by_client(self, id_client: str) -> List[Dict[str, Any]]:
        params = {
            Constant.ID_EXTERNAL: id_client,
        }
        # data.get(Constant.ID_EXTERNAL)
        print(f"Getting users for client with params: {params}")
        params = json.dumps(params)
        users = await self.user_client.get_users_by_client(params)
        data = json.loads(users.data)
        return data
