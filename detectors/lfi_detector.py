from detectors.base_detector import BaseDetector


class LFIDetector(BaseDetector):
    """Detector de vulnerabilidades LFI"""
    
    def __init__(self):
        super().__init__()
        self.patterns = [
            r'root:.*:0:0:',  # /etc/passwd
            r'\[boot loader\]',  # boot.ini
            r'<\?xml version=',  # XML files
            r'\[extensions\]',  # php.ini
            r'for 16-bit app support',  # win.ini
            r'C:\\\\Windows',  # Windows paths
            r'/var/www/',  # Linux paths
        ]
    
    def detect(self, response_text: str, payload: str) -> bool:
        """Detecta LFI"""
        return self._match_patterns(response_text)


# ====================================================================
# detectors/__init__.py
# ====================================================================

"""Módulo de detectores de vulnerabilidades"""

from detectors.xss_detector import XSSDetector
from detectors.sqli_detector import SQLiDetector
from detectors.lfi_detector import LFIDetector

__all__ = ['XSSDetector', 'SQLiDetector', 'LFIDetector']