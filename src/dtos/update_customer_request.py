from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateCustomerRequest:
    name: Optional[str]
    phone: Optional[str] = None
    address: Optional[str] = None
