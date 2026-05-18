import uuid
from dataclasses import dataclass, field

@dataclass(frozen=True)
class TicketCode:
    value: str = field(default_factory=lambda: uuid.uuid4().hex[:10].upper())

    def __str__(self) -> str:
        return self.value