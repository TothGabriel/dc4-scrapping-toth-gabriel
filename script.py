import csv
import requests
from bs4 import BeautifulSoup

# Fct extraction des datas
def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lignes = soup.find_all('tr', class_='team')
    resultats = []
    
    for ligne in lignes:
        td_diff = ligne.find('td', class_='diff text-success')
        td_ga = ligne.find('td', class_='ga')
        
        if td_diff and td_ga:
            ga = int(td_ga.text.strip())
            
            if ga < 300:
                resultat = {
                    'nom': ligne.find('td', class_='name').text.strip(),
                    'annee': ligne.find('td', class_='year').text.strip(),
                    'victoires': ligne.find('td', class_='wins').text.strip(),
                    'defaites': ligne.find('td', class_='losses').text.strip(),
                    'ot_defaites': ligne.find('td', class_='ot-losses').text.strip(),
                    'pourcentage_victoires': ligne.find('td', class_='pct text-success').text.strip(),
                    'buts_pour': ligne.find('td', class_='gf').text.strip(),
                    'buts_contre': ligne.find('td', class_='ga').text.strip(),
                    'difference': td_diff.text.strip()
                }
                resultats.append(resultat)
    
    return resultats

