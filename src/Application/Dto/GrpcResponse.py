from dataclasses import dataclass
from typing import Any

@dataclass
class GrpcResponse:
    status: str
    message: str
    data: Any