from __future__ import annotations
from dataclasses import dataclass, asdict
 
@dataclass
class Catalog:
    id_catalog: str
    name_catalog: str
    id_detail: str
    code: str
    value: str

@dataclass
class OAuthProviders:
    id_detail_catalog: str
    name: str
    image: str

    def to_dict(self):
        return asdict(self)