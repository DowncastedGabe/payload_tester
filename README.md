**USO ÉTICO APENAS**

Ferramenta modular e profissional para testar payloads de segurança em aplicações web.

- **Arquitetura Modular**: Código organizado em classes e módulos reutilizáveis
- **Multi-threading**: Testes paralelos para melhor performance
- **Múltiplos Detectores**: XSS, SQLi, LFI e Command Injection
- **Relatórios Detalhados**: Exportação em TXT e JSON
- **Sistema de Logs**: Logging completo de todas as operações
- **Configurável**: Timeout, threads, delay e mais

🔧 Instalação

bash
# Clone ou crie a estrutura do projeto
mkdir payload_tester
cd payload_tester

# Crie os diretórios necessários
mkdir -p core detectors utils scripts payloads results

# Crie os arquivos __init__.py
touch core/__init__.py detectors/__init__.py utils/__init__.py

# Instale as dependências
pip install -r requirements.txt

# Crie os arquivos de payload de exemplo
python scripts/create_payload_files.py

# Testar XSS
python main.py -u "http://example.com/search?q=test" -p payloads/xss.txt

# Testar SQL Injection
python main.py -u "http://example.com/page?id=1" -p payloads/sqli.txt

# Testar LFI
python main.py -u "http://example.com/view?file=page.php" -p payloads/lfi.txt

Esta ferramenta foi criada para:
- Testes de segurança autorizados
- Bug bounty programs
- Pentesting com permissão
- Ambientes educacionais

**NÃO use esta ferramenta para:**
- Atacar sistemas sem autorização
- Atividades ilegais
- Causar danos a terceiros

O uso inadequado desta ferramenta pode resultar em consequências legais.

Contribuições são bem-vindas! Para adicionar novos detectores ou melhorias:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
