import requests
from bs4 import BeautifulSoup
import json
import csv
import logging
from selenium import webdriver
import pandas as pd

# Configurar o sistema de logs
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl_website(url):
    try:
        # Enviar uma solicitação HTTP para a página
        response = requests.get(url)

        # Verificar se a solicitação foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Criar um dicionário para armazenar os dados
            data = {
                "site": url,
                "links": []
            }

            # Analisar o conteúdo da página com BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar todos os links na página
            links = soup.find_all('a')

            # Armazenar os links encontrados no dicionário
            for link in links:
                href = link.get('href')
                if href:
                    data["links"].append(href)

            # Converter o dicionário em JSON
            json_data = json.dumps(data, indent=4)

            pd.read_json(json_data).to_csv('output.csv')


            # Escrever os dados em um arquivo JSON
            with open('output.json', 'w') as json_file:
                json_file.write(json_data)

            # Capturar um screenshot
            driver = webdriver.Chrome()
            driver.get(url)
            driver.save_screenshot('screenshot.png')
            driver.quit()

            # Registar informações no sistema de logs
            logging.info(f"Extraídos dados da página: {url}")

        else:
            logging.error(f'Falha na solicitação. Código de status: {response.status_code}')

    except Exception as e:
        logging.error(f"Ocorreu um erro durante a execução: {str(e)}")

if __name__ == "__main__":
    url = input("Digite a URL que você deseja rastrear: ")
    crawl_website(url)
