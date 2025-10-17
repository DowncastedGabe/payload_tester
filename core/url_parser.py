# Parser e manipulador de URLs

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Dict, Tuple

class URLParser:

    @staticmethod
    def extract_parameters(url: str) -> Dict[str, str]:
        """Extrai os parametros de uma URL"""

        parsed = urlparse(url)
        params = parse_qs(parsed.query, keep_blank_values=True)
        return {k: v[0] if v else '' for k, v in params.items()}

    @staticmethod
    def build_url(base_url: str, params: Dict[str, str]) -> str:
        """Constrói uma URL com os parametros"""

        parsed = urlparse(base_url)
        query = urlencode(params)
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment
        ))

    @staticmethod
    def get_base_url(url: str) -> str:
        """Obtém a URL base de uma URL completa"""
        parsed = urlparse(url)
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            '', '', ''
        ))

    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """Valida uma URL"""
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False, "URL deve conter scheme e netloc"
            if result.scheme not in ['http', 'https']:
                return False, "Scheme deve ser http ou https"
            return True, ""
        except Exception as e:
            return False, str(e)