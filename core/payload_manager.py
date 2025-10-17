import os
from typing import List
from config import PAYLOADS_DIR


class PayloadManager:
    #Gerenciador para carregar e manipular payloads

    @staticmethod
    def load_from_file(filepath: str) -> List[str]:

        if not os.path.isabs(filepath):
            filepath = os.path.join(PAYLOADS_DIR, filepath)

        try:
            with open(filepath, 'r', encoding='utf-8', errors ='ignore') as f:
                payloads = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith('#')
                ]
            return payloads
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de payloads nao encontrado: {filepath}")
        except Exception as e:
            raise Exception(f"Erro ao carregar payloads: {e}")
    
    @staticmethod
    def load_from_list(payloads: List[str]) -> List[str]:
        #Retorna lista de payloads ja processada
        return [p.strip() for p in payloads if p.strip()]

    @staticmethod
    def get_available_payloads() -> List[str]:
        #Lista de arquivos de payloads disponiveis
        if not os.path.exists(PAYLOADS_DIR):
            return []
        
        return [
            f for f in os.listdir(PAYLOADS_DIR)
            if f.endswith('.txt')
        ]