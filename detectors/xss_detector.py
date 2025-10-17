from detectors.base_detector import BaseDetector

class XSSDetector(BaseDetector):

    def __init__(self):
        super().__init__()
        self.patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'onerror\s*=',
            r'onload\s*=',
            r'<svg[^>]*onload',
            r'<img[^>]*onerror',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',           
        ]

    def detect(self, response_text: str, payload: str) -> bool:

        if payload in response_text:
            
            if self._match_patterns(response_text):
                return True
            
            dangerous_chars = ['<', '>', '"', "'", 'javascript:', 'on']
            if any(char in payload for char in dangerous_chars):
                return True
        
        return False
