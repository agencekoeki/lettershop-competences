# Les compétences de Lettershop pour votre IA

Vous préparez une enseigne, un logo ou des lettres en relief avec ChatGPT, Gemini, Claude ou une autre IA. Ce dépôt donne à votre IA les consignes de Lettershop, pour qu'elle vous montre un aperçu qui ressemble à ce que l'atelier peut fabriquer, puis qu'elle prépare avec vous une demande de devis complète. Votre conseiller Lettershop vérifie tout et vous propose une prévisualisation 3D offerte.

Lettershop fabrique en France des enseignes, des logos et des lettres en relief sur mesure : https://www.lettershop.fr/

## Les compétences

| Compétence | Ce que fait votre IA | Consigne à copier | Fichier à installer |
|---|---|---|---|
| Obtenir un aperçu réaliste | Elle part d'une photo de votre façade et de votre logo à plat, choisit une vraie matière, sa vraie épaisseur, la bonne échelle et une lumière possible, puis montre une vue de face et une vue en situation. | [`consignes/obtenir-un-apercu-realiste.txt`](consignes/obtenir-un-apercu-realiste.txt) | [`dist/lettershop-apercu-enseigne.zip`](dist/lettershop-apercu-enseigne.zip) |
| Préparer ma demande de devis | Elle vous pose les questions d'un conseiller, une à la fois, puis rédige une demande prête à envoyer. | [`consignes/preparer-ma-demande-de-devis.txt`](consignes/preparer-ma-demande-de-devis.txt) | [`dist/lettershop-demande-de-devis.zip`](dist/lettershop-demande-de-devis.zip) |

Les deux s'enchaînent : l'aperçu se joint à la demande de devis.

## Le plus simple : copier une consigne

1. Ouvrez la consigne de votre choix et copiez tout le texte.
2. Collez-le dans une nouvelle conversation avec votre IA, puis répondez à ses questions.
3. Pour un devis, collez la demande rédigée dans le formulaire https://www.lettershop.fr/demande-de-devis/ et joignez vos images telles qu'elles sont.

Aucun compte payant n'est nécessaire. La consigne ne transmet rien à Lettershop : vous envoyez vous-même votre demande.

## Installer dans Claude, ChatGPT ou Gemini

Chaque compétence est un dossier avec un fichier `SKILL.md`, dans le format que lisent Claude, ChatGPT et Gemini. Téléchargez le fichier `.zip` de la compétence, puis suivez les gestes de votre outil. Le détail, les sources et ce qui reste à vérifier sont dans [`references/installer-dans-claude-chatgpt-gemini.md`](references/installer-dans-claude-chatgpt-gemini.md) (état au 17/11/2026).

**Claude (claude.ai)**, avec l'exécution de code activée :
1. Settings › Capabilities : activez « Code execution and file creation ».
2. Customize › Skills › « + » › « + Create skill » › « Upload a skill ».
3. Choisissez le fichier `.zip`. Recommencez pour la seconde compétence.

**Claude Code** : les deux compétences sont dans un seul plugin, `lettershop`. [Ces commandes ne fonctionnent qu'une fois le dépôt `agencekoeki/lettershop-competences` rendu public : il est privé pour l'instant.]

```
/plugin install lettershop --marketplace agencekoeki/lettershop-competences
```

ou, en deux temps :

```
/plugin marketplace add agencekoeki/lettershop-competences
/plugin install lettershop@lettershop-competences
```

Les compétences se déclenchent quand vous parlez de votre enseigne. Vous pouvez aussi les appeler : `/lettershop:lettershop-apercu-enseigne` et `/lettershop:lettershop-demande-de-devis`.

**ChatGPT**, offres Business, Enterprise, Healthcare et Edu :
1. Barre latérale › Plugins › onglet Skills.
2. Create › Upload from your computer.
3. Choisissez la compétence [zip ou dossier décompressé : à tester]. ChatGPT l'analyse avant de l'activer.

**Gemini**, sans abonnement, 18 ans ou plus, sur gemini.google.com, l'application mobile ou l'application Mac :
1. Customize (ou More › Customize) › Skills.
2. Create › Upload : choisissez le `.zip`, le dossier décompressé ou le `SKILL.md`, puis Open et Upload.
3. Relisez, puis Create.

Sur les offres gratuites de ChatGPT, ou si votre outil ne propose pas les compétences, copiez simplement la consigne : elle fait le même travail.

## Ce que les compétences ne font pas

- Elles ne donnent aucun prix ni aucun délai : seul votre devis les donne.
- Elles ne disent pas à la place de l'atelier ce qui est faisable : l'aperçu sert à se projeter, votre conseiller confirme.
- Elles ne créent pas votre logo et ne fabriquent pas de fichier vectoriel : Lettershop accepte votre image telle quelle, même un JPEG.
- Elles ne disent jamais qu'une enseigne extérieure n'a besoin d'aucune autorisation : renseignez-vous auprès de votre mairie.

## Pour les personnes qui maintiennent ce dépôt

- **Une seule source par compétence.** La consigne publique est le bloc entre `<!-- consigne:debut -->` et `<!-- consigne:fin -->` de son `SKILL.md`, dans `plugins/lettershop/skills/<compétence>/`. Ne modifiez jamais un `.txt` de `consignes/` à la main. La liste des compétences, leur fichier, leur phrase-repère et l'id de leur texte sur la page du site sont dans `COMPETENCES`, en tête de `outils/generer_consigne.py`.
- **Après chaque modification d'un SKILL.md** :
  ```
  python3 outils/generer_consigne.py
  python3 outils/construire_zip.py
  python3 -m unittest discover -s outils -p "test_*.py" -v
  claude plugin validate .
  ```
- **Les zips** de `dist/` sont reproductibles : le test vérifie, octet pour octet, qu'ils correspondent aux dossiers des compétences.
- **La page du site** doit afficher les mêmes consignes. Pour le vérifier : `python3 outils/generer_consigne.py --verifier-html chemin/vers/la-page.html`.
- **Les phrases-repères** (« Demande préparée avec les consignes Lettershop. », « Aperçu préparé avec les consignes Lettershop. ») servent à compter ce qui arrive grâce aux consignes. Ne les modifiez pas.
- **L'URL du dépôt** citée dans les consignes (https://github.com/agencekoeki/lettershop-competences) est provisoire : le dépôt est privé, il sera publié plus tard. Le script le rappelle à chaque génération (`URL_DEPOT_PROVISOIRE` dans `outils/generer_consigne.py`). Quand le dépôt devient public, passez-la à `False`.
- **Pas de numéro de version** dans `plugin.json` ni dans `marketplace.json` : Claude Code suit alors les commits.
- **Une nouvelle compétence** : un dossier dans `plugins/lettershop/skills/`, une entrée dans `COMPETENCES`, un fichier de scénarios dans `tests/`. Le test refuse un dossier de compétence sans entrée.

## Licence

[Licence à choisir avec Lettershop. Proposition : CC BY 4.0 pour les textes, qui permet de les reprendre en citant Lettershop, et MIT pour les scripts du dossier `outils/`.]
