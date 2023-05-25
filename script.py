import csv
import requests
from bs4 import BeautifulSoup

# Fct extraction des datas
def extract_data(url):
    response = requests.post(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    lignes = soup.find_all('tr', class_='team')
    resultats = []

    for ligne in lignes:
        td_diff = ligne.find('td', class_='diff text-success')
        td_ga = ligne.find('td', class_='ga')

        if td_diff and td_ga:
            ga = int(td_ga.text.strip()) if td_ga.text.strip() else 0

            if ga < 300:
                resultat = {
                    'Team name': ligne.find('td', class_='name').text.strip() if ligne.find('td', class_='name') else '',
                    'Year': ligne.find('td', class_='year').text.strip() if ligne.find('td', class_='year') else '',
                    'Wins': ligne.find('td', class_='wins').text.strip() if ligne.find('td', class_='wins') else '',
                    'Losses': ligne.find('td', class_='losses').text.strip() if ligne.find('td', class_='losses') else '',
                    'OT Losses': ligne.find('td', class_='ot-losses').text.strip() if ligne.find('td', class_='ot-losses') else '',
                    'Win %': ligne.find('td', class_='pct text-success').text.strip() if ligne.find('td', class_='pct text-success') else '',
                    'Goals For (GF)	': ligne.find('td', class_='gf').text.strip() if ligne.find('td', class_='gf') else '',
                    'Goals Against (GA)': ligne.find('td', class_='ga').text.strip() if ligne.find('td', class_='ga') else '',
                    '+ / -': td_diff.text.strip()
                }
                resultats.append(resultat)

    return resultats

# Fonction de parcours des pages + création du fichier csv
def save_csv():
    base_url = 'https://www.scrapethissite.com/pages/forms/'
    resultats_finaux = []

    for page_num in range(1, 11):
        url = f"{base_url}?page_num={page_num}"
        resultats_page = extract_data(url)
        resultats_finaux.extend(resultats_page)

    # Enregistrement des résultats dans un fichier CSV
    with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=resultats_finaux[0].keys())
        writer.writeheader()
        writer.writerows(resultats_finaux)


save_csv()