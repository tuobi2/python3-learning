from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=False)
class Notification:
    """通知实体"""
    bill_id: str
    employee_name: str
    message: str
    notify_time: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
