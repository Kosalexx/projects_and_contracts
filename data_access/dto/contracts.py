from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ContractsDTO:
    name: str
    status: str = "draft"
    id: Optional[int] = None
    signing_date: Optional[datetime] = None
    creation_date: datetime = datetime.now(tz=timezone.utc)
    project_id: Optional[int] = None
