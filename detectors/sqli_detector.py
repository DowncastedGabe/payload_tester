from detectors.base_detector import BaseDetector


class SQLiDetector(BaseDetector):
    """Detector de vulnerabilidades SQL Injection"""
    
    def __init__(self):
        super().__init__()
        self.patterns = [
            # MySQL
            r'SQL syntax.*?MySQL',
            r'Warning.*?\Wmysqli?_',
            r'valid MySQL result',
            r'MySqlClient\.',
            r'com\.mysql\.jdbc',
            
            # PostgreSQL
            r'PostgreSQL.*?ERROR',
            r'Warning.*?\Wpg_',
            r'valid PostgreSQL result',
            r'Npgsql\.',
            
            # SQL Server
            r'Driver.*? SQL[\-\_\ ]*Server',
            r'OLE DB.*? SQL Server',
            r'SQLServer JDBC Driver',
            r'SqlClient\.',
            r'Microsoft SQL Native Client error',
            
            # Oracle
            r'Oracle error',
            r'Oracle.*?Driver',
            r'Warning.*?\Woci_',
            r'Warning.*?\Wora_',
            
            # Genérico
            r'SQL error',
            r'mysql_fetch',
            r'num_rows',
            r'SQLException',
            r'Unclosed quotation mark',
            r'quoted string not properly terminated',
        ]
    
    def detect(self, response_text: str, payload: str) -> bool:
        """Detecta SQL Injection"""
        return self._match_patterns(response_text)