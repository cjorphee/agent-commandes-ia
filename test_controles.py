from agent import Commande, Ligne
from donnees import charger_catalogue, charger_clients
from controles import controler

catalogue = charger_catalogue()
clients = charger_clients()
email = "david@carrosserie-bertin.fr"

bonne = Commande(
    date_livraison="2026-11-03",
    lignes=[Ligne(texte_original="5 x LUN-INC", reference="LUN-INC",
                  quantite=5, confiance=1.0, remarque=None)],
    a_valider=False,
    motif=None,
)

mauvaise = Commande(
    date_livraison=None,
    lignes=[Ligne(texte_original="4 tendeurs à lanterne M12", reference=None,
                  quantite=4, confiance=0.3, remarque=None)],
    a_valider=False,
    motif=None,
)

print("Bonne commande :", controler(bonne, email, catalogue, clients))
print("Mauvaise commande :", controler(mauvaise, email, catalogue, clients))