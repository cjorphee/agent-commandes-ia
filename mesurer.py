import csv
import json
from pathlib import Path

DOSSIER = Path("projet2_donnees_test")
if (DOSSIER / "projet2_donnees_test").exists():
    DOSSIER = DOSSIER / "projet2_donnees_test"

attendu_lignes = {}
with open(DOSSIER / "verite_terrain" / "lignes.csv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        attendu_lignes.setdefault(r["fichier"], set()).add((r["reference"], int(r["quantite"])))

entetes = {}
with open(DOSSIER / "verite_terrain" / "entetes.csv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        entetes[r["fichier"]] = r

# Ce que l'agent a décidé : lu dans le fichier a_valider.csv
a_valider_agent = set()
with open("a_valider.csv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        a_valider_agent.add(r["fichier"])

parfaites = 0
lignes_attendues = 0
lignes_fausses = 0
fausses_alertes = []
pieges_detectes = 0
pieges_total = 0
erreurs = []

for n in range(1, 31):
    fichier = f"email_{n:02d}.txt"
    chemin = Path("resultats") / f"email_{n:02d}.json"
    if not chemin.exists():
        print(fichier, ": pas de résultat, ignoré")
        continue
    commande = json.loads(chemin.read_text(encoding="utf-8"))
    attendu = entetes[fichier]
    est_piege = attendu["a_valider"] == "oui"

    if est_piege:
        pieges_total += 1
        if fichier in a_valider_agent:
            pieges_detectes += 1
        continue

    obtenues = {(l["reference"], l["quantite"]) for l in commande["lignes"]}
    attendues = attendu_lignes.get(fichier, set())
    en_trop = obtenues - attendues
    manquantes = attendues - obtenues
    lignes_attendues += len(attendues)
    lignes_fausses += len(manquantes)
    date_ok = (commande["date_livraison"] or "") == attendu["date_livraison"]

    if not en_trop and not manquantes and date_ok:
        parfaites += 1
    else:
        erreurs.append((fichier, sorted(manquantes), sorted(en_trop), date_ok))
    if fichier in a_valider_agent:
        fausses_alertes.append(fichier)

normaux = 30 - pieges_total
print("=== RÉSULTATS ===")
print(f"Commandes parfaites (lignes et date exactes) : {parfaites} / {normaux}")
print(f"Lignes attendues retrouvées : {lignes_attendues - lignes_fausses} / {lignes_attendues}")
print(f"Taux d'erreur sur les lignes : {100 * lignes_fausses / lignes_attendues:.1f} %")
print(f"Pièges détectés : {pieges_detectes} / {pieges_total}")
print(f"Fausses alertes : {len(fausses_alertes)} / {normaux}  {fausses_alertes}")
if erreurs:
    print("\n=== DÉTAIL DES ERREURS ===")
    for fichier, manq, trop, date_ok in erreurs:
        print(fichier, "| manquantes:", manq, "| en trop:", trop, "| date ok:", date_ok)