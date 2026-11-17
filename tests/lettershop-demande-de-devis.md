# Tests : lettershop-demande-de-devis

Chaque demande se lance dans une conversation neuve, une fois avec le skill installé dans Claude Code, une fois en collant `consignes/preparer-ma-demande-de-devis.txt` dans ChatGPT gratuit. Pour chacune : le skill s'est-il chargé (ou pas, pour la 5) ? Les questions arrivent-elles une à la fois, dans l'ordre usage, lieu, texte, taille, image ? Aucun prix, aucun délai, aucune faisabilité affirmée ? La demande finit-elle par la phrase-repère ? Le lien vers la compétence installable arrive-t-il seulement après la demande, en une phrase au plus, sans que l'IA ouvre le lien elle-même ?

1. « J'ai fait mon logo avec ChatGPT, je voudrais une enseigne avec ce logo pour ma boulangerie. » (avec une image en 3D, reflets chromés)
   → attendu : question sur l'usage, puis le lieu ; le chromé et la perspective signalés comme non fabricables tels quels ; aide pour obtenir un logo à plat ; demande complète avec « reflets chromés » dans les points à vérifier.
2. « Combien pour une enseigne de 2 mètres en néon ? »
   → attendu : aucun prix ni fourchette ; explication en une phrase (le prix dépend de la forme, du texte, des options) ; les questions pour compléter la demande.
3. « Voici notre logo en .ai et les cotes : 80 × 30 cm, pour l'accueil. » (un service communication)
   → attendu : pas d'interrogatoire complet ; seulement ce qui manque (support, fixation, quantité, date) ; demande rédigée.
4. Cas jamais vu : « Je veux mettre mon logo sur la façade de mon restaurant, c'est dans le centre historique, à côté de la cathédrale. Pas besoin d'autorisation, hein ? »
   → attendu : ne pas dire qu'aucune autorisation n'est nécessaire ; renvoyer vers la mairie ; continuer la demande normalement (lieu extérieur, support façade).
5. Anti-déclencheur : « Crée-moi un logo pour ma boulangerie, style rétro. »
   → attendu : le skill ne se charge pas (création de logo).
