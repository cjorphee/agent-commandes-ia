from agent import extraire_commande
from donnees import charger_catalogue, charger_clients, lire_email, expediteur
from controles import controler

catalogue = charger_catalogue()
clients = charger_clients()

for n in (27, 28, 29, 30, 1, 3, 8):
    texte = lire_email(n)
    commande = extraire_commande(texte, catalogue)
    statut, motifs = controler(commande, expediteur(texte), catalogue, clients)
    print(f"Email {n} : {statut}")
    for m in motifs:
        print("   -", m)