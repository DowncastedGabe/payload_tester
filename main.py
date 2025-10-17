import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import time

from core.http_client import HTTPClient
from core.url_parser import URLParser
from core.payload_manager import PayloadManager
from detectors import XSSDetector, SQLiDetector, LFIDetector
from utils.logger import Logger
from utils.colors import Colors
from utils.report_generator import ReportGenerator
from config import DEFAULT_MAX_WORKERS, DEFAULT_TIMEOUT


class PayloadTester:
    """Classe principal para testes de payloads"""
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT, 
                 max_workers: int = DEFAULT_MAX_WORKERS, delay: float = 0):
        """Inicializa o testador"""
        self.http_client = HTTPClient(timeout=timeout, delay=delay)
        self.url_parser = URLParser()
        self.logger = Logger()
        self.max_workers = max_workers
        
        # Inicializa detectores
        self.detectors = [
            XSSDetector(),
            SQLiDetector(),
            LFIDetector()
        ]
        
        self.results = []
        self.tested_count = 0
    
    def test_single_payload(self, url: str, param: str, 
                           payload: str, method: str = 'GET') -> Optional[Dict]:
        """Testa um único payload"""
        try:
            params = self.url_parser.extract_parameters(url)
            params[param] = payload
            
            start_time = time.time()
            
            if method.upper() == 'GET':
                test_url = self.url_parser.build_url(url, params)
                response = self.http_client.get(test_url)
            else:
                base_url = self.url_parser.get_base_url(url)
                response = self.http_client.post(base_url, data=params)
            
            response_time = round(time.time() - start_time, 2)
            
            # Detecta vulnerabilidades
            vulnerabilities = []
            for detector in self.detectors:
                if detector.detect(response.text, payload):
                    vulnerabilities.append(detector.name.replace('Detector', ''))
            
            reflected = payload in response.text
            
            if vulnerabilities or reflected:
                return {
                    'url': url,
                    'param': param,
                    'payload': payload,
                    'method': method,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'response_length': len(response.content),
                    'vulnerabilities': vulnerabilities,
                    'reflected': reflected
                }
        
        except Exception as e:
            self.logger.debug(f"Erro ao testar {param} com payload: {str(e)[:50]}")
        
        return None
    
    def run(self, url: str, payloads: List[str], 
            method: str = 'GET', specific_param: Optional[str] = None) -> List[Dict]:
        """
        Executa os testes
        
        Args:
            url: URL alvo
            payloads: Lista de payloads
            method: Método HTTP
            specific_param: Parâmetro específico (opcional)
        """
        # Valida URL
        is_valid, error = self.url_parser.validate_url(url)
        if not is_valid:
            self.logger.error(f"URL inválida: {error}")
            return []
        
        # Extrai parâmetros
        params = self.url_parser.extract_parameters(url)
        if not params:
            self.logger.error("Nenhum parâmetro encontrado na URL")
            return []
        
        # Filtra parâmetros
        if specific_param:
            if specific_param not in params:
                self.logger.error(f"Parâmetro '{specific_param}' não encontrado")
                return []
            params_to_test = {specific_param: params[specific_param]}
        else:
            params_to_test = params
        
        self.logger.info(Colors.info(f"URL: {url}"))
        self.logger.info(f"Parâmetros: {', '.join(params_to_test.keys())}")
        self.logger.info(f"Payloads: {len(payloads)}")
        self.logger.info(f"Método: {method}")
        print("=" * 70)
        
        start_time = time.time()
        total_tests = len(params_to_test) * len(payloads)
        
        # Executa testes em paralelo
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for param in params_to_test.keys():
                for payload in payloads:
                    future = executor.submit(
                        self.test_single_payload,
                        url, param, payload, method
                    )
                    futures.append(future)
            
            for future in as_completed(futures):
                self.tested_count += 1
                result = future.result()
                
                if result:
                    self._print_finding(result)
                    self.results.append(result)
                
                if self.tested_count % 50 == 0:
                    progress = (self.tested_count / total_tests) * 100
                    print(f"[*] Progresso: {progress:.1f}% ({self.tested_count}/{total_tests})", end='\r')
        
        elapsed = time.time() - start_time
        self._print_summary(total_tests, elapsed)
        
        return self.results
    
    def _print_finding(self, result: Dict) -> None:
        """Imprime descoberta"""
        if result['vulnerabilities']:
            print(Colors.error("\n[!] VULNERABILIDADE DETECTADA!"))
            vuln_types = ', '.join(result['vulnerabilities']).upper()
            print(Colors.error(f"    Tipo: {vuln_types}"))
        else:
            print(Colors.warning("\n[!] PAYLOAD REFLETIDO"))
        
        print(f"    Parâmetro: {result['param']}")
        print(f"    Payload: {result['payload'][:80]}")
        print(f"    Status: {result['status_code']}")
        print(f"    Tempo: {result['response_time']}s")
    
    def _print_summary(self, total: int, elapsed: float) -> None:
        """Imprime resumo"""
        print("\n" + "=" * 70)
        print(Colors.info("[*] RESUMO DOS TESTES"))
        print("=" * 70)
        print(f"Total de testes: {total}")
        print(Colors.success(f"Vulnerabilidades encontradas: {len(self.results)}"))
        print(f"Tempo total: {elapsed:.2f}s")
        print(f"Taxa: {total/elapsed:.2f} testes/segundo")
        print("=" * 70)
    
    def cleanup(self) -> None:
        """Limpa recursos"""
        self.http_client.close()


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Ferramenta de Teste de Payloads em URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:
  %(prog)s -u "http://example.com/page?id=1" -p payloads/xss.txt
  %(prog)s -u "http://example.com/search?q=test" -p payloads/sqli.txt --method POST
  %(prog)s -u "http://example.com/page?id=1&cat=2" -p payloads/xss.txt --param id
  %(prog)s -u "http://example.com/page?id=1" -p payloads/xss.txt --threads 20 --output report.json
        '''
    )
    
    parser.add_argument('-u', '--url', required=True, help='URL alvo com parâmetros')
    parser.add_argument('-p', '--payloads', required=True, help='Arquivo de payloads')
    parser.add_argument('-m', '--method', default='GET', choices=['GET', 'POST'], help='Método HTTP')
    parser.add_argument('--param', help='Testar apenas este parâmetro')
    parser.add_argument('--threads', type=int, default=DEFAULT_MAX_WORKERS, help='Número de threads')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='Timeout em segundos')
    parser.add_argument('--delay', type=float, default=0, help='Delay entre requisições')
    parser.add_argument('-o', '--output', help='Salvar relatório (formato: .txt ou .json)')
    
    args = parser.parse_args()
    
    try:
        # Carrega payloads
        print(Colors.info("[*] Carregando payloads..."))
        payloads = PayloadManager.load_from_file(args.payloads)
        print(Colors.success(f"[+] {len(payloads)} payloads carregados\n"))
        
        # Inicializa tester
        tester = PayloadTester(
            timeout=args.timeout,
            max_workers=args.threads,
            delay=args.delay
        )
        
        # Executa testes
        results = tester.run(
            url=args.url,
            payloads=payloads,
            method=args.method,
            specific_param=args.param
        )
        
        # Gera relatório se solicitado
        if args.output and results:
            print(f"\n[*] Gerando relatório...")
            
            if args.output.endswith('.json'):
                content = ReportGenerator.generate_json(results, args.url)
            else:
                content = ReportGenerator.generate_txt(results, args.url)
            
            filepath = ReportGenerator.save_report(content, args.output)
            print(Colors.success(f"[+] Relatório salvo em: {filepath}"))
        
        tester.cleanup()
        
    except KeyboardInterrupt:
        print(Colors.warning("\n\n[!] Interrompido pelo usuário"))
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"\n[!] Erro: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
