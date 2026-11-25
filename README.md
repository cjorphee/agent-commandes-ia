# Agent de saisie de commandes par email (Claude API)

Un agent qui lit l'email d'un client, en extrait la commande (références, quantités, date de livraison) et la range dans un fichier prêt à saisir, ou la met de côté pour validation humaine quand il y a un doute.

> Projet de démonstration. L'entreprise (NormaTech Distribution), son catalogue, ses clients et les 30 emails sont **fictifs**.

## Le problème

Dans une PME de distribution, des commandes arrivent par email, écrites à la main : « 9 boites vis CHC M4x12 », « livraison vendredi ». Quelqu'un les ressaisit une à une dans l'outil de gestion. C'est long, et une erreur de référence ou de quantité coûte cher.

## La solution

```
email  →  Claude extrait la commande  →  contrôles en code  →  commandes_pretes.csv
                                                           →  a_valider.csv
```

1. **Client** : identifié par l'adresse de l'expéditeur, dans le code. Claude ne le devine jamais.
2. **Extraction** : Claude (modèle `claude-haiku-5-5`, SDK `anthropic`) reçoit l'email et le catalogue. Il renvoie une commande structurée (modèles Pydantic `Commande` et `Ligne`) avec, pour chaque ligne, une référence, une quantité et un niveau de confiance.
3. **Garde-fous** : le principe est « Claude propose, le code vérifie ». Une commande part en validation humaine si l'une de ces conditions est vraie : client inconnu, aucune ligne, signalement par l'agent, référence absente du catalogue, quantité absente ou hors de 1 à 50, confiance inférieure à 0,8.
4. **Sorties** : `commandes_pretes.csv` (une ligne par article, prêtes à saisir) et `a_valider.csv` (commande et motifs).

## Lancer le projet

Prérequis : Python 3 et une clé API Claude.

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY="ta-clé"      # PowerShell, dans le terminal où tu lances le script
python lancer.py                      # traite les 30 emails (quelques centimes)
python mesurer.py                     # compare avec la vérité terrain
```

La clé n'est lue que dans la variable d'environnement. Elle n'est écrite dans aucun fichier du dépôt.

## Résultats mesurés

30 emails de test : 26 commandes normales et 4 pièges (commande vague, article introuvable, information manquante...). Les bonnes réponses sont dans `projet2_donnees_test/projet2_donnees_test/verite_terrain/`. Le script `mesurer.py` les compare à ce que l'agent a produit.

| Indicateur | Avant | Après |
|---|---|---|
| Commandes parfaites (lignes et date exactes) | 25 / 26 (96,2 %) | 26 / 26 (100 %) |
| Lignes retrouvées | 103 / 104 | 104 / 104 |
| Pièges détectés | 4 / 4 | 4 / 4 |
| Fausses alertes (commandes normales envoyées en validation) | 3 / 26 (11,5 %) | 0 / 26 |

**Ce qui a changé entre « avant » et « après ».** Une règle générale a été ajoutée aux instructions : les clients emploient des termes familiers (« vis agglo » pour vis à bois, « TH » pour tête hexagonale), et si une seule référence correspond, l'agent doit la proposer. Elle ne cite aucun email du test.

**Pourquoi ces chiffres ne prouvent pas 100 % en conditions réelles :**
- La règle a été écrite après avoir vu les erreurs de ces mêmes 30 emails. Le résultat « après » est une mise au point, pas une mesure sur des données jamais vues.
- Avec zéro erreur sur 26 commandes, le taux d'échec réel peut encore être de l'ordre de 11 % (règle des trois : 3 / 26).
- Un modèle ne répond pas toujours à l'identique : un autre lancement peut donner un résultat légèrement différent.

## Limites connues

- Données fictives, emails courts, en français, sans pièce jointe ni PDF.
- Tout le catalogue (200 références) est envoyé dans chaque appel. Cela ne passerait pas à l'échelle avec des dizaines de milliers de références : il faudrait d'abord présélectionner les références proches.
- Pas d'interface de validation : les commandes à valider sont dans un fichier CSV.
- `lancer.py` n'efface pas le dossier `resultats` avant un nouveau lancement, donc un ancien fichier peut subsister si un appel échoue.
- Le dossier `resultats_avant` conserve les réponses brutes d'avant la modification pour 28 emails sur 30 (24 et 25 manquent). Les chiffres « avant » viennent de la mesure faite à ce moment-là.

## Pistes d'amélioration

1. Écrire 10 à 15 nouveaux emails jamais vus et mesurer sans modifier les instructions.
2. Présélectionner les références candidates avant l'appel à Claude pour les grands catalogues.
3. Lire les emails directement depuis une boîte mail, et gérer les pièces jointes.
4. Ajouter une interface pour valider les commandes, et suivre le coût par commande.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `agent.py` | Modèles `Commande` / `Ligne`, instructions, appel à Claude |
| `controles.py` | Garde-fous : décide « ok » ou « à valider » |
| `donnees.py` | Lecture du catalogue, des clients et des emails |
| `lancer.py` | Traite les 30 emails et écrit les deux CSV |
| `mesurer.py` | Calcule les indicateurs par rapport à la vérité terrain |
| `test_*.py` | Petits tests : connexion, contrôles, pièges |
| `resultats/`, `resultats_avant/` | Réponses brutes de l'agent après et avant la règle ajoutée |
| `projet2_donnees_test/` | Catalogue, clients, 30 emails et vérité terrain (fictifs) |