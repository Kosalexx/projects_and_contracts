from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ProjectsDTO:
    name: str
    contract_id: Optional[int] = None
    id: Optional[int] = None
    creation_date: datetime = datetime.now(tz=timezone.utc)
