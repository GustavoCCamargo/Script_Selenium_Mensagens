from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import time
import urllib.parse
import sys


# =========================
# CONFIGURAÇÕES
# =========================

WHATSAPP_WEB_URL = "https://web.whatsapp.com/"

TEMPO_ESPERA_LOGIN = 90
TEMPO_ESPERA_ENVIO = 30
TEMPO_ENTRE_MENSAGENS = 20

# Campo onde a mensagem é digitada no WhatsApp Web
XPATH_CAMPO_MENSAGEM = (
    '//*[@id="main"]/footer//div[@contenteditable="true"][@role="textbox"]'
)


def obter_mensagem_padrao():
    """
    Retorna a mensagem que será enviada.
    """

    return (
        "🎮 *Projeto de Extensão JogLog* 🎮\n\n"
        "Prezados pais e responsáveis,\n\n"
        "Gostaríamos de informar que, como parte das ações do Projeto de extensão JogLog, criamos um grupo de comunicação com os responsáveis pelos alunos.*\n\n"
        "O objetivo desse grupo é facilitar o compartilhamento de informações importantes e demais comunicados relacionados ao projeto.\n\n"
        "👉 *Entre no grupo pelo link abaixo:*\n"
        "https://chat.whatsapp.com/IUsnlg9TfLSFU8pqF9rAXk\n\n"
        "📅 *Início das aulas:* 06/08\n\n"
        "Pedimos, por gentileza, que ingressem no grupo o quanto antes para acompanhar todas as informações do projeto.\n\n"
        "Em caso de dúvidas, estamos à disposição.\n\n"
        "Atenciosamente,\n"
        "*Equipe JogLog* 🎮"
    )


def iniciar_navegador():
    """
    Abre o Google Chrome e acessa o WhatsApp Web.
    """

    chrome_options = Options()

    # Mantém o navegador aberto após o fim do programa
    chrome_options.add_experimental_option("detach", True)

    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    navegador.maximize_window()
    navegador.get(WHATSAPP_WEB_URL)

    return navegador


def aguardar_login(navegador):
    """
    Aguarda o usuário entrar no WhatsApp Web.
    """

    print("Aguardando o WhatsApp Web carregar...")
    print("Leia o QR Code caso seja solicitado.")

    try:
        WebDriverWait(
            navegador,
            TEMPO_ESPERA_LOGIN
        ).until(
            EC.presence_of_element_located((By.ID, "side"))
        )

        print("WhatsApp Web carregado com sucesso.")

    except TimeoutException:
        print("Tempo esgotado durante o login.")
        navegador.quit()
        sys.exit(1)


def enviar_mensagem(navegador, numero, mensagem):
    """
    Abre a conversa do número informado e envia a mensagem.
    """

    texto_codificado = urllib.parse.quote(mensagem)

    link = (
        "https://web.whatsapp.com/send"
        f"?phone={numero}&text={texto_codificado}"
    )

    navegador.get(link)

    try:
        campo_mensagem = WebDriverWait(
            navegador,
            TEMPO_ESPERA_ENVIO
        ).until(
            EC.element_to_be_clickable(
                (By.XPATH, XPATH_CAMPO_MENSAGEM)
            )
        )

        # Pequena espera para garantir que a mensagem carregou
        time.sleep(3)

        campo_mensagem.click()
        campo_mensagem.send_keys(Keys.ENTER)

        print(f"Mensagem enviada para {numero}.")

    except TimeoutException:
        print(
            f"Não foi possível abrir a conversa de {numero}.\n"
            "Confira se o número está correto."
        )

    except Exception as erro:
        print(f"Erro ao enviar mensagem para {numero}: {erro}")


def main():
    """
    Função principal do programa.
    """

    # Coloque os números aqui.
    # Formato: 55 + DDD + número
    contatos = [
        "5545999999999",
    ]
    mensagem = obter_mensagem_padrao()

    navegador = iniciar_navegador()

    aguardar_login(navegador)

    for numero in contatos:
        print(f"Processando o número {numero}...")

        enviar_mensagem(
            navegador=navegador,
            numero=numero,
            mensagem=mensagem
        )

        print(
            f"Aguardando {TEMPO_ENTRE_MENSAGENS} segundos..."
        )

        time.sleep(TEMPO_ENTRE_MENSAGENS)

    print("Todos os contatos foram processados.")


if __name__ == "__main__":
    main()