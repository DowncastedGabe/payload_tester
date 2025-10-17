#CLIENTE PARA REALIZAR REQUISICOES HTTP

import requests
from typing import Dict, Optional
import time
from config import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT
import urllib3


class HTTPClient:
    #CLIENTE HTTP COM SUPORTE A SESSOES E CONFIG

    def __init__(self, timeout: int = DEFAULT_TIMEOUT,
                delay: float = 0, user_agent: str = DEFAULT_USER_AGENT):

        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.session.verify = False

        #Desabilita avisos de SSL
        urllib3.disable_warnings()
    
    def get(self, url: str, params: Optional[Dict] = None) -> requests.Response:

        if self.delay > 0:
            time.sleep(self.delay)
        
        return self.session.get(url, params=params, timeout=self.timeout)
    
    def post(self, url: str, data: Optional[Dict] = None) -> requests.Response:

        if self.delay > 0:
            time.sleep(self.delay)
        
        return self.session.post(url, data=data, timeout=self.timeout)
    
    def close(self) -> None:
        self.session.close()