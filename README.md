## Projeto: health_check

Este script em Python realiza verificação "health check" de serviços definidos em um arquivo JSON.


## Funcionalidades

- Verifica o status HTTP (ex: `/health`) de serviços.
- Testa a conectividade com IP e porta usando sockets (mecanismo que permite a comunicação entre diferentes processos).
- Permite inserção de URL manual pelo usuário (interação com usuário).
- Utiliza variáveis de ambiente para configurar tempo limite e nível de log.


## Exemplo de uso

1. Edite o arquivo `input.json` com seus serviços.
2. Configure `.env` com:
    ```
    TIMEOUT=5
    LOG_LEVEL=DEBUG
    ```
3. Execute o script:
    ```
    python health_check.py
    ```

4. Você verá os resultados e poderá testar uma URL manualmente.

(A configuração de timeout e log level debug são dois conceitos importantes no desenvolvimento de software que afetam o comportamento do sistema. O timeout controla o tempo máximo que uma operação pode durar antes de ser interrompida, enquanto o log level debug determina o nível de detalhes das mensagens de log geradas.)


## Exemplo de saída

🩺 Verificando serviço: Google
────────────────────────────────────────────
🌐 URL de saúde: https://www.google.com/health  
📶 Status HTTP: ❌ 404 Not Found  
🔌 Conectividade: ✅ Host www.google.com:443 acessível

🩺 Verificando serviço: Serviço Local
────────────────────────────────────────────
🌐 URL de saúde: http://localhost:8080/health  
📶 Status HTTP: ✅ 200 OK  
🔌 Conectividade: ✅ Host localhost:8080 acessível

🔍 Teste Manual
────────────────────────────────────────────
🌐 URL: https://exemplo.com/api/health  
📶 Status HTTP: ❌ 503 Service Unavailable