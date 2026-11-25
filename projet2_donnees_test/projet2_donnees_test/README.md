# Données de test — Projet 2 : agent d'extraction de commandes

Contexte : NormaTech Distribution (entreprise fictive, voir l'audit IA). Ses clients envoient leurs commandes par email, des collègues les ressaisissent à la main. Ton agent doit lire chaque email et produire une commande structurée.

## Contenu
- `catalogue.csv` : 200 références (reference, designation, famille, unite_vente, prix_ht)
- `clients.csv` : 15 clients (code_client, raison_sociale, contact, email, ville)
- `emails/` : 30 emails de commande (email_01.txt à email_30.txt)
- `verite_terrain/entetes.csv` : pour chaque email, la bonne réponse (client, date de livraison, à valider ou non)
- `verite_terrain/lignes.csv` : pour chaque email, les bonnes lignes (référence, quantité)

## Les 30 emails
- 01 à 12 : références écrites telles quelles (3 mises en forme différentes)
- 13 à 22 : seulement des désignations, parfois familières ou sans accents (il faut retrouver la référence dans le catalogue)
- 23 à 26 : commandes présentées en tableau texte (le 26 sans références, uniquement des désignations)
- 27 à 30 : cas à faire valider par un humain (quantité manquante, article absent du catalogue, commande non détaillée, référence ambiguë)

## Règles à connaître
- Les quantités sont exprimées dans l'unité de vente du catalogue (boîtes, paires, pièces, sachets).
- Les dates relatives (« demain », « vendredi ») se calculent à partir de la date de l'email (ligne `Date:`). « Vendredi » = le premier vendredi après la date de l'email.
- « dès que possible » = pas de date de livraison (champ vide).
- Dans `verite_terrain`, `a_valider = oui` signifie que l'agent ne doit pas valider la commande tout seul. Pour ces emails, `lignes.csv` ne contient que les lignes claires.

## À quoi sert la vérité terrain
À l'étape « Mesures » : tu compares la sortie de ton agent avec ces fichiers pour calculer le taux de commandes sans correction, le taux d'erreurs et le taux de bonnes détections « à valider ».
