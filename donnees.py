import csv
import re
from pathlib import Path

DOSSIER = Path("projet2_donnees_test") / "projet2_donnees_test"

def charger_catalogue():
    with open(DOSSIER / "catalogue.csv", encoding="utf-8", newline="") as f:
        return {ligne["reference"]: ligne for ligne in csv.DictReader(f)}

def charger_clients():
    with open(DOSSIER / "clients.csv", encoding="utf-8", newline="") as f:
        return {ligne["email"]: ligne for ligne in csv.DictReader(f)}

def lire_email(numero):
    chemin = DOSSIER / "emails" / f"email_{numero:02d}.txt"
    return chemin.read_text(encoding="utf-8")

def expediteur(texte):
    return re.search(r"<(.+?)>", texte).group(1)

if __name__ == "__main__":
    catalogue = charger_catalogue()
    clients = charger_clients()
    texte = lire_email(14)
    print(len(catalogue), "références")
    print(clients[expediteur(texte)]["raison_sociale"])