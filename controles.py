def controler(commande, email_client, catalogue, clients):
    motifs = []
    if email_client not in clients:
        motifs.append("client inconnu")
    if not commande.lignes:
        motifs.append("aucune ligne de commande")
    if commande.a_valider:
        motifs.append(commande.motif or "signalé par l'agent")
    for l in commande.lignes:
        if l.reference not in catalogue:
            motifs.append(f"référence inconnue : {l.texte_original}")
        if l.quantite is None or not (1 <= l.quantite <= 50):
            motifs.append(f"quantité douteuse : {l.texte_original}")
        if l.confiance < 0.8:
            motifs.append(f"confiance faible : {l.texte_original}")
    return ("à valider" if motifs else "ok"), motifs