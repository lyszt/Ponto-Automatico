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

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    login = os.getenv("LOGIN")
    senha = os.getenv("PASSWORD")

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get("https://sigrh.uffs.edu.br/")
    try:
        username = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "login")))
        password = driver.find_element(By.ID, "senha")
        username.send_keys(login)
        password.send_keys(senha)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "logar"))).click()

    except TimeoutException:
        print("Took to much time to find element.")


    driver.get("https://sigrh.uffs.edu.br/sigrh/frequencia/ponto_eletronico/cadastro_ponto_eletronico.jsf")

    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "idFormDadosEntradaSaida:idBtnRegistrarEntrada"))).click()
    except TimeoutException:
        print("Took to much time to find element.")