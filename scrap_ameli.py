
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extraire_donnees(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Referer": "http://annuairesante.ameli.fr/recherche.html",
        "Cookie": "infosoins=35i39qqc9rv0t93jdo9jqfovp3; AmeliDirectPersist=1265688887.42527.0000; xtvrn=$475098$; TS01b76c1f=0139dce0d20ceeaa3ff1ffa93b1e9984166d956aa5ab6b3a31f91906cb199e2cc35142679b59774e4adeeaf977887b7021164c2707"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("div", class_="item-professionnel")

    resultats = []

    for item in items:
        numero = item.find("span", class_="num").text.strip()
        nom = item.find("h2").strong.text.strip()
        specialite = item.find("div", class_="specialite").text.strip()
        honoraires = item.find("div", class_="type_honoraires").text.strip()
        adresse = item.find("div", class_="adresse").text.strip()

        resultats.append([numero, nom, specialite, honoraires, adresse])

    return resultats


def parcourir_pages():
    base_url = "http://annuairesante.ameli.fr"
    payload = {
        "type": "ps",
        "ps_nom": "",
        "ps_profession": "34",
        "ps_profession_label": "Médecin généraliste",
        "ps_acte": "",
        "ps_acte_label": "",
        "ps_type_honoraire": "indifferent",
        "ps_carte_vitale": "2",
        "ps_sexe": "2",
        "es_nom": "",
        "es_specialite": "",
        "es_specialite_label": "",
        "es_actes_maladies": "",
        "es_actes_maladies_label": "",
        "es_type": "3",
        "ps_localisation": "HERAULT (34)",
        "ps_proximite": "on",
        "localisation_category": "departements",
        "submit_final": "Rechercher"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Referer": "http://annuairesante.ameli.fr/recherche.html",
        "Cookie": "infosoins=35i39qqc9rv0t93jdo9jqfovp3; AmeliDirectPersist=1265688887.42527.0000; xtvrn=$475098$; TS01b76c1f=0139dce0d20ceeaa3ff1ffa93b1e9984166d956aa5ab6b3a31f91906cb199e2cc35142679b59774e4adeeaf977887b7021164c2707"
    }

    resultats = []

    page = 1
    while True:
        payload["page"] = str(page)

        response = requests.get(base_url, params=payload, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        items = soup.find_all("div", class_="item-professionnel")

        if not items:
            break

        for item in items:
            numero = item.find("span", class_="num").text.strip()
            nom = item.find("h2").strong.text.strip()
            specialite = item.find("div", class_="specialite").text.strip()
            honoraires = item.find("div", class_="type_honoraires").text.strip()
            adresse = item.find("div", class_="adresse").text.strip()

            resultats.append([numero, nom, specialite, honoraires, adresse])

        page += 1

    return resultats

# Exemple d'utilisation
donnees = parcourir_pages()

# Convertir les données en DataFrame pandas
df = pd.DataFrame(donnees, columns=["Numero", "Nom", "Specialite", "Honoraires", "Adresse"])
print(df)

