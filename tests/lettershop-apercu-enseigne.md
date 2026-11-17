# Tests : lettershop-apercu-enseigne

Chaque demande se lance dans une conversation neuve : avec la compétence installée (Claude, ChatGPT, Gemini), et en collant `consignes/obtenir-un-apercu-realiste.txt` dans ChatGPT gratuit et dans Gemini. Pour chacune : la compétence s'est-elle chargée (ou pas, pour la 5) ? L'IA demande-t-elle d'abord une photo du lieu et le logo à plat, avant d'écrire le prompt ? Le prompt est-il montré avant la génération ? Y a-t-il deux vues, face et situation ? Le rappel « pas un bon de fabrication », aucun prix, aucun délai ? La phrase « Aperçu préparé avec les consignes Lettershop. » puis la proposition de demande de devis ? Le lien vers la compétence installable arrive-t-il seulement après l'aperçu, en une phrase au plus ?

1. « Montre-moi mon logo en néon rose sur la façade de mon bar. » (avec une photo de façade et le logo)
   → attendu : néon LED sur plaque de plexiglas transparente, au crépuscule, halo réaliste ; à l'extérieur, rappel « à l'abri total de la pluie » ; modification de la seule zone de l'enseigne ; texte relu lettre par lettre.
2. « Mon aperçu ChatGPT a du chrome qui coule et de la fumée, je veux le même en vrai. » (avec l'image)
   → attendu : expliquer ce qui ne se fabrique pas ; proposer miroir, métal brossé ou lettres boîtiers à tranches métalliques ; retirer la fumée ; demander une photo du lieu et le logo à plat.
3. « Fais une image de "Atelier Margot" en lettres bois sur le mur de mon accueil. » (sans photo)
   → attendu : demander une photo ; à défaut, scène intérieure sobre ; bois naturel, 19 mm, ombre sur le mur ; repère d'échelle ; aucun autre texte dans l'image.
4. Cas jamais vu : « Je veux voir mon enseigne en lettres polystyrène de 30 cm d'épaisseur, en extérieur, pour toute l'année. »
   → attendu : faire l'aperçu si la personne le souhaite, mais dire que le site réserve le polystyrène, dehors, au temps d'un événement à l'abri de la pluie, et proposer une matière d'extérieur durable à confirmer par le conseiller ; ne pas affirmer de faisabilité.
5. Anti-déclencheur : « Dessine-moi un nouveau logo pour mon bar, style années 80. »
   → attendu : la compétence ne se charge pas (création de logo).
