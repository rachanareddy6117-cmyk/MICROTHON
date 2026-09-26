from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScanner(ABC):
    @abstractmethod
    def scan_path(self, target_path: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        pass
