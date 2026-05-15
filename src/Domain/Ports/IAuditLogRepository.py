from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IAuditLogRepository(ABC):

    @abstractmethod
    async def get_auditlog(
        self, 
        number_page: int,
        total_row: int,
        search: str,
        type: str
    ) -> List[Dict[str, Any]]: ...