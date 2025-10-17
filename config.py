# Configuracoes da aplicacao

import os

#Configuracoes de rede

DEFAULT_TIMEOUT = 10
DEFAULT_MAX_WORKERS = 5
DEFAULT_DELAY = 0
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

#Diretorios

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOADS_DIR = os.path.join(BASE_DIR, 'payloads')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

#Criar diretorios se nao existirem

os.makedirs(PAYLOADS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

#Configuracoes de logging

LOG_LEVEL = 'INFO'
LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
