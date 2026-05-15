from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from Osdental.Database.BaseRepository import BaseRepository
from src.Domain.Ports.IAuditLogRepository import IAuditLogRepository
from . import DashQuery

class AuditLogRepository(BaseRepository, IAuditLogRepository):

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_auditlog(
        self, 
        number_page: int,
        total_row: int,
        search: str,
        type: str
    ) -> List[Dict[str, Any]]:
        params = {
            'numberPage': number_page,
            'totalRow': total_row,
            'search': search,
            'type': type
        }

        return await self._execute_query(
            DashQuery.GET_AUDIT_LOG,
            params=params,
            many=True,
            as_dict=True
        )        