from typing import Optional
from pydantic import BaseModel

class Ligne(BaseModel):
    texte_original: str          # la ligne telle qu'écrite par le client
    reference: Optional[str]     # référence du catalogue, ou None si introuvable
    quantite: Optional[int]      # None si le client ne l'a pas précisée
    confiance: float             # de 0 à 1
    remarque: Optional[str]      # ce qui pose problème, sinon None

class Commande(BaseModel):
    date_livraison: Optional[str]   # AAAA-MM-JJ, None si « dès que possible »
    lignes: list[Ligne]
    a_valider: bool
    motif: Optional[str]

INSTRUCTIONS = """Tu es l'assistant de saisie des commandes de NormaTech Distribution.
Tu reçois l'email d'un client et le catalogue des produits.
Extrais la commande en respectant ces règles :
1. N'invente jamais un article, une quantité ou une date.
2. Chaque référence doit exister dans le catalogue. Sinon, mets reference à null.
3. Si une information manque, si plusieurs références sont possibles ou si la commande n'est pas détaillée, mets a_valider à true et explique dans motif.
4. Les quantités sont exprimées dans l'unité de vente du catalogue.
5. La date de livraison est calculée à partir de la ligne Date de l'email, au format AAAA-MM-JJ. Pour « dès que possible », mets null.
6. confiance va de 0 à 1 : 1 si la référence est écrite telle quelle dans l'email, moins si tu as dû deviner.
7. Une date de livraison vide (« dès que possible ») est normale : ne mets pas a_valider à true pour cette raison.
8. Mets a_valider à true seulement si une ligne est ambiguë, introuvable, sans quantité, ou si la commande n'est pas détaillée. Ne demande pas de confirmation sur des quantités claires.
9. Les clients utilisent des termes familiers : « vis agglo » désigne une vis à bois, « CHC » une vis à tête cylindrique six pans creux, « TH » une tête hexagonale. Quand une seule référence du catalogue correspond au produit et au format demandés, propose-la avec une confiance d'au moins 0,85 et explique ton choix dans remarque. Ne laisse reference vide que si plusieurs références sont possibles ou si aucune ne correspond."""

def construire_prompt(texte_email, catalogue):
    lignes = [f"{c['reference']} | {c['designation']} | {c['unite_vente']}"
              for c in catalogue.values()]
    return "CATALOGUE\n" + "\n".join(lignes) + "\n\nEMAIL\n" + texte_email

import anthropic

client_ia = anthropic.Anthropic()
MODELE = "claude-haiku-5-5"

def extraire_commande(texte_email, catalogue):
    reponse = client_ia.messages.parse(
        model=MODELE,
        max_tokens=2000,
        system=INSTRUCTIONS,
        messages=[{"role": "user",
                   "content": construire_prompt(texte_email, catalogue)}],
        output_format=Commande,
    )
    return reponse.parsed_output

if __name__ == "__main__":
    from donnees import charger_catalogue, lire_email
    catalogue = charger_catalogue()
    for n in (26,):
        print(f"--- email {n} ---")
        print(extraire_commande(lire_email(n), catalogue))