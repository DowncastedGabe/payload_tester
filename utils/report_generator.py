import json
from datetime import datetime
from typing import List, Dict
import os
from config import RESULTS_DIR


class ReportGenerator:
    """Gerador de relatórios de testes"""
    
    @staticmethod
    def generate_txt(results: List[Dict], target_url: str) -> str:
        """Gera relatório em formato texto"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = []
        report.append("=" * 80)
        report.append("RELATÓRIO DE TESTES DE SEGURANÇA")
        report.append("=" * 80)
        report.append(f"Data: {timestamp}")
        report.append(f"URL Alvo: {target_url}")
        report.append(f"Total de vulnerabilidades encontradas: {len(results)}")
        report.append("=" * 80)
        report.append("")
        
        for i, result in enumerate(results, 1):
            report.append(f"[{i}] VULNERABILIDADE DETECTADA")
            report.append(f"    Tipo: {', '.join(result['vulnerabilities']).upper()}")
            report.append(f"    Parâmetro: {result['param']}")
            report.append(f"    Payload: {result['payload']}")
            report.append(f"    Método: {result['method']}")
            report.append(f"    Status Code: {result['status_code']}")
            report.append(f"    Tempo de resposta: {result['response_time']}s")
            report.append(f"    Payload refletido: {'Sim' if result['reflected'] else 'Não'}")
            report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_json(results: List[Dict], target_url: str) -> str:
        """Gera relatório em formato JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'target_url': target_url,
            'total_vulnerabilities': len(results),
            'vulnerabilities': results
        }
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    @staticmethod
    def save_report(content: str, filename: str) -> str:
        """
        Salva relatório em arquivo
        
        Returns:
            Caminho do arquivo salvo
        """
        filepath = os.path.join(RESULTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath