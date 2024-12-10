import requests
import time
from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv() 
# URLs da API pública para as builds específicas
BUILD_API_URLS  = os.getenv("BUILD_API_URLS")

RELEASES_API_URL = os.getenv("RELEASES_API_URL")

NOTIFICATION_WEBHOOK = os.getenv("NOTIFICATION_WEBHOOK")

def send_notification(message):
    """Envia notificação para o webhook configurado."""
    payload = {"content": message}  # Formato para webhook do Discord
    response = requests.post(NOTIFICATION_WEBHOOK, json=payload)
    if response.status_code == 204:  # Sucesso no Discord
        print("Notificação enviada com sucesso!")
    else:
        print(f"Erro ao enviar notificação: {response.status_code} - {response.text}")

def check_build_status(url):
    """Obtém o status da build no GitHub Actions."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Erro ao acessar a API de builds: {response.status_code}")
    return None


def monitor_builds(last_build_status):
    """Monitora o status das builds especificadas."""
    for url in BUILD_API_URLS:
        build_data = check_build_status(url)
        if build_data:
            run_id = build_data["id"]
            current_status = build_data["status"]  # Ex.: 'queued', 'in_progress', 'completed'
            conclusion = build_data["conclusion"]  # Ex.: 'success', 'failure', 'cancelled', ou None

            if run_id not in last_build_status or current_status != last_build_status[run_id]:
                if current_status == "in_progress":
                    send_notification(f"⏳ Build {run_id} está em execução.")
                elif current_status == "queued":
                    send_notification(f"📋 Build {run_id} está na fila.")
                elif current_status == "completed":
                    if conclusion == "success":
                        send_notification(f"✅ Build {run_id} concluída com sucesso!")
                    elif conclusion == "failure":
                        send_notification(f"❌ Build {run_id} falhou!")
                    else:
                        send_notification(f"⚠️ Build {run_id} concluída com status: {conclusion}")
                last_build_status[run_id] = current_status





def get_latest_release():
    """Obtém a release mais recente do repositório."""
    response = requests.get(RELEASES_API_URL)
    if response.status_code == 200:
        releases = response.json()
        if releases:
            latest_release = releases[0]  # A release mais recente é a primeira
            return latest_release
        else:
            print("Nenhuma release encontrada.")
            return None
    print(f"Erro ao acessar a API de releases: {response.status_code}")
    return None

def monitor_releases(last_release_id):
    """Monitora novas releases do repositório verificando a tag `latest`."""
    latest_release = get_latest_release()
    if latest_release:
        release_id = latest_release["id"]
        release_tag = latest_release["tag_name"]
        release_name = latest_release["name"]
        release_url = latest_release["html_url"]

        if release_id != last_release_id:
            if release_tag != "twilight":
                message = f"🚀 Nova release disponível: **{release_name}**\nTag: `{release_tag}`\nVeja mais: {release_url}"
                send_notification(message)
                return release_id
            else:
                print(f"Nenhuma nova release `latest`. A tag mais recente é `{release_tag}`.")
                send_notification(f"🔍 Nenhuma nova release `latest`. A tag mais recente é `{release_tag}`.")
    return last_release_id

def main():
    """Loop principal para monitorar builds e releases."""
    last_build_status = {}
    last_release_id = None

    while True:
        # Monitorar builds
        monitor_builds(last_build_status)

        # Monitorar releases
        last_release_id = monitor_releases(last_release_id)

        # Espera antes de próxima verificação
        time.sleep(600)

if __name__ == "__main__":
    main()