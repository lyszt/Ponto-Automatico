import os
import time

import requests, pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import easygui
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()
    login = os.getenv("LOGIN")
    senha = os.getenv("PASSWORD")
    if login is None or senha is None:
        dados = easygui.multpasswordbox("Insira o usuário e a senha.", "Bater ponto automático", ["Login", "Senha"])
        login = dados[0]
        senha = dados[1]

    # settar entrada ou saída
    tipo = easygui.buttonbox('Bater entrada ou saida?', 'Bater ponto automático', ['Entrada', 'Saida'])
    tipo = tipo.lower()



    ua = UserAgent(os='windows')
    userAgent = ua.chrome
    print(userAgent)


    options = Options()
    #options.add_argument('--headless')
    options.add_experimental_option("detach", True)
    options.add_argument(f'user-agent={userAgent}')

    driver = webdriver.Chrome(options=options)
    driver.get("https://sigrh.uffs.edu.br/")
    driver.maximize_window()
    try:
        username = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "login")))
        password = driver.find_element(By.ID, "senha")
        username.send_keys(login)
        password.send_keys(senha)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "logar"))).click()

    except TimeoutException:
        print("Took to much time to find element.")


    driver.get("https://sigrh.uffs.edu.br/sigrh/frequencia/ponto_eletronico/cadastro_ponto_eletronico.jsf")

    cookies = driver.get_cookies()
    cookies = {cookie["name"]: cookie["value"] for cookie in cookies}

    url = "https://sigrh.uffs.edu.br/sigrh/frequencia/ponto_eletronico/cadastro_ponto_eletronico.jsf"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "sigrh.uffs.edu.br",
        "Origin": "https://sigrh.uffs.edu.br",
        "Referer": "https://sigrh.uffs.edu.br/sigrh/frequencia/ponto_eletronico/cadastro_ponto_eletronico.jsf",
        "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    tipoEntradaSaida = "Registrar Saída" if "saida" in tipo else "Registrar Entrada"
    tipoBotao = "RegistrarSaida" if "saida" in tipo else "RegistrarEntrada"
    data = {
        "idFormDadosEntradaSaida": "idFormDadosEntradaSaida",
        "idFormDadosEntradaSaida:observacoes": "",
        f"idFormDadosEntradaSaida:idBtn{tipoBotao}": f"{tipoEntradaSaida}",
        "javax.faces.ViewState": "j_id3"
    }

    response = requests.post(url, headers=headers, data=data, cookies=cookies, allow_redirects=True)

    print(response.status_code)
