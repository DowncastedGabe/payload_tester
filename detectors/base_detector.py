from abc import ABC, abstractmethod
from typing import List
import re

class BaseDetector(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        self.patterns: List[str] = []
    
    @abstractmethod
    def detect(self, response_text: str, payload: str) -> bool:
        pass

    def _match_patterns(self, text: str) -> bool:
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                return True
        return False
        