import json
import socket
import os
import requests
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Inicializa colorama para colorir o terminal
init(autoreset=True)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações por ambiente
TIMEOUT = int(os.getenv("TIMEOUT", 5))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def log(message, level="INFO"):
    """Exibe logs conforme o nível configurado"""
    if LOG_LEVEL == "DEBUG" or level == LOG_LEVEL:
        print(f"[{level}] {message}")


def check_http_health(url):
    """Realiza verificação de status HTTP"""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return {
            "url": url,
            "status_code": response.status_code,
            "reason": response.reason
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "error": str(e)
        }


def check_connectivity(host, port):
    """Testa se o host:porta está acessível via socket"""
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return {"host": host, "port": port, "status": "reachable"}
    except socket.error as e:
        return {"host": host, "port": port, "status": "unreachable", "error": str(e)}


def print_result(result):
    """Imprime o resultado formatado para cada serviço"""
    print(f"\n🩺 Verificando serviço: {result['name']}")
    print("────────────────────────────────────────────")

    health = result["health"]
    conn = result["connectivity"]

    # HTTP Status
    if "status_code" in health:
        status_icon = "✅" if health["status_code"] == 200 else "❌"
        print(f"🌐 URL de saúde: {health['url']}")
        print(f"📶 Status HTTP: {status_icon} {health['status_code']} {health['reason']}")
    else:
        print(f"🌐 URL de saúde: {health['url']}")
        print(f"{Fore.RED}📶 Erro HTTP: {health['error']}")

    # Conectividade
    if conn["status"] == "reachable":
        print(f"🔌 Conectividade: ✅ Host {conn['host']}:{conn['port']} acessível")
    else:
        print(f"{Fore.RED}🔌 Conectividade: ❌ Host {conn['host']}:{conn['port']} inacessível")
        print(f"{Fore.YELLOW}ℹ️ Erro: {conn['error']}")


def main():
    # Lê os serviços do JSON
    try:
        with open("input.json", "r") as f:
            services = json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}[ERRO] Arquivo 'input.json' não encontrado.")
        return

    results = []

    for service in services:
        log(f"Verificando serviço: {service['name']}", "DEBUG")

        health = check_http_health(service["health_url"])
        connectivity = check_connectivity(service["host"], service["port"])

        results.append({
            "name": service["name"],
            "health": health,
            "connectivity": connectivity
        })

    # Exibe resultados formatados
    for result in results:
        print_result(result)

    # Interação com o usuário
    user_url = input("\n🔍 Digite uma URL para verificar o status HTTP: ").strip()
    if user_url:
        custom_check = check_http_health(user_url)
        print("\n🔍 Teste Manual")
        print("────────────────────────────────────────────")
        print(f"🌐 URL: {user_url}")
        if "status_code" in custom_check:
            icon = "✅" if custom_check["status_code"] == 200 else "❌"
            print(f"📶 Status HTTP: {icon} {custom_check['status_code']} {custom_check['reason']}")
        else:
            print(f"{Fore.RED}📶 Erro HTTP: {custom_check['error']}")


if __name__ == "__main__":
    main()