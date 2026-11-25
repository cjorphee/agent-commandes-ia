import csv
import json
from pathlib import Path

from agent import extraire_commande
from donnees import charger_catalogue, charger_clients, lire_email, expediteur
from controles import controler

catalogue = charger_catalogue()
clients = charger_clients()

Path("resultats").mkdir(exist_ok=True)
pretes = []
a_valider = []

for n in range(1, 31):
    fichier = f"email_{n:02d}.txt"
    texte = lire_email(n)
    email_client = expediteur(texte)
    try:
        commande = extraire_commande(texte, catalogue)
    except Exception as erreur:
        a_valider.append([fichier, f"erreur technique : {erreur}"])
        print(fichier, "erreur")
        continue

    Path("resultats", f"email_{n:02d}.json").write_text(
        commande.model_dump_json(indent=2), encoding="utf-8")

    statut, motifs = controler(commande, email_client, catalogue, clients)
    if statut == "ok":
        code = clients[email_client]["code_client"]
        for l in commande.lignes:
            pretes.append([fichier, code, commande.date_livraison or "",
                           l.reference, l.quantite])
    else:
        a_valider.append([fichier, " | ".join(motifs)])
    print(fichier, statut)

with open("commandes_pretes.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["fichier", "code_client", "date_livraison", "reference", "quantite"])
    w.writerows(pretes)

with open("a_valider.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["fichier", "motifs"])
    w.writerows(a_valider)

print("Terminé :", len(pretes), "lignes prêtes,", len(a_valider), "commandes à valider")