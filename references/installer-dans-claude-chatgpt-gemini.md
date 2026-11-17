# Installer la compétence dans Claude, ChatGPT ou Gemini

**État au 17/11/2026 [SAVOIR]** : pages d'aide officielles relues le 17/11/2026, sources en bas de chaque partie. Les interfaces changent souvent : si un libellé ne correspond plus, la page d'aide fait foi. Les libellés sont ceux des pages d'aide en anglais ; l'interface française peut les traduire. Ce qui n'a pas pu être vérifié est entre crochets.

Les fichiers à téléverser, un par compétence, produits par `python3 outils/construire_zip.py` :
- `dist/lettershop-apercu-enseigne.zip` (obtenir un aperçu réaliste) ;
- `dist/lettershop-demande-de-devis.zip` (préparer ma demande de devis).

Chacun contient un seul dossier au nom de la compétence, avec `SKILL.md` et `references/`. Dans claude.ai, ChatGPT et Gemini, on installe chaque compétence séparément.

Pour toutes les offres et tous les outils, les consignes à copier du dossier `consignes/` marchent sans rien installer.

## Le format est le même partout

- Claude, ChatGPT et Gemini lisent le même format : un dossier avec un `SKILL.md` qui commence par un en-tête `name` et `description`.
- OpenAI : « The `SKILL.md` file must include `name` and `description` » ; les skills s'appuient sur le standard ouvert des agent skills (agentskills.io). Source : https://learn.chatgpt.com/docs/build-skills
- Gemini Enterprise : `name` de 1 à 64 caractères, minuscules, chiffres et tirets, égal au nom du dossier ; `description` de 1 à 1 024 caractères. Source : https://docs.cloud.google.com/gemini/enterprise/docs/skills

## Claude (claude.ai)

**Offre** : la page d'aide liste Free, Pro, Max, Ultra, Team et Enterprise, et exige l'exécution de code. [La documentation développeur indique « Pro, Max, Ultra, Team, and Enterprise » pour les skills personnalisés : la possibilité de téléverser sur l'offre gratuite est à tester.]

**Gestes** :
1. Offres individuelles : Settings › Capabilities, activer « Code execution and file creation » (appelé « Create and edit files » dans la mise en page actuelle). Team et Enterprise : Organization settings › Plugins & skills, onglet « Policy ».
2. Customize › Skills, bouton « + », puis « + Create skill », puis « Upload a skill ».
3. Choisir le `.zip` de la compétence. Elle apparaît dans la liste et s'active ou se désactive d'un clic.

Sources : https://support.claude.com/en/articles/12512180-use-skills-in-claude (« Updated this week », lu le 17/11/2026) ; https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## Claude Code

**Offre** : celle qui donne accès à Claude Code.

Les deux compétences sont dans un seul plugin, `lettershop`.

**Gestes** [ne fonctionnent qu'une fois le dépôt `agencekoeki/lettershop-competences` rendu public : il est privé pour l'instant] :
- en une commande, à partir de Claude Code 2.1.275 (conseil donné par `claude plugin validate`) : `/plugin install lettershop --marketplace agencekoeki/lettershop-competences` ;
- ou en deux : `/plugin marketplace add agencekoeki/lettershop-competences`, puis `/plugin install lettershop@lettershop-competences`.

Vérifié le 17/11/2026 en local, avec Claude Code 2.1.326 : marketplace ajoutée depuis le dossier, plugin installé, « Skills (2) lettershop-apercu-enseigne, lettershop-demande-de-devis ». Source : https://code.claude.com/docs/en/plugin-marketplaces

## ChatGPT

**Offre** : « eligible ChatGPT Business, Enterprise, Healthcare, and Edu users », selon les réglages de l'espace de travail. Free, Go, Plus et Pro ne figurent pas dans la liste de l'aide officielle. [Une source tierce cite Plus : contradiction non résolue, l'aide officielle fait foi.] Sur ces offres, utiliser la consigne à copier.

**Surfaces** : les skills seuls sont dans l'application de bureau ChatGPT, Codex CLI et l'extension IDE ; les skills groupés dans des plugins sont aussi sur le web, le bureau et le mobile.

**Gestes** :
1. Barre latérale › Plugins, puis l'onglet Skills du Plugin Directory.
2. Create › Upload from your computer.
3. Choisir la compétence. [L'aide ne précise pas le format attendu ; une source tierce parle d'importer « un dossier de skill ». Zip ou dossier décompressé : à tester.] ChatGPT analyse le fichier : il peut être marqué « Needs Review » ou « Blocked ».

Sources : https://help-lb.openai.com/en/articles/20001066-skills-in-chatgpt (« Updated: 13 days ago », lu le 17/11/2026) ; https://learn.chatgpt.com/docs/build-skills ; https://www.firecrawl.dev/blog/chatgpt-skills (30/10/2026, source tierce)

## Gemini (application grand public)

**Offre** : « Skills are available without a Google AI subscription ». Il faut avoir 18 ans ou plus et être connecté. Uniquement dans l'application mobile Gemini, l'application Gemini sur Mac et gemini.google.com. [Date de lancement : la page d'aide n'en donne pas ; le 13/10/2026 vient d'une autre source, non vérifiée.]

**Gestes** :
1. Sur gemini.google.com, barre latérale › Customize (sinon More › Customize), puis Skills en haut.
2. Create › Upload, puis choisir le `.zip`, ou le dossier décompressé `lettershop-demande-de-devis`, ou le `SKILL.md` seul. Cliquer sur Open, puis Upload.
3. Relire, puis Create.

[L'aide demande « a `.zip` file that contains a `SKILL.md` file in its main folder » : nos zips rangent `SKILL.md` dans un dossier. Si Gemini le refuse, téléverser le dossier décompressé ou le `SKILL.md` seul. À tester.]

Contraintes citées : 100 Mo au total ; pas de fichiers cachés comme `.DS_Store` ou `.pyc` ; pas de script qui a besoin d'internet. Nos zips n'ont ni fichier caché ni script.

Source : https://support.google.com/gemini?p=pn_skills (lu le 17/11/2026)

## Gemini Enterprise

**Offre** : éditions Standard, Plus et Pay-as-you-go. L'édition Frontline ne peut pas téléverser de skill. L'administrateur doit activer la fonction.

**Gestes** :
1. Application web Gemini Enterprise › menu de navigation › Skills.
2. Icône d'ajout › Upload skill.
3. Glisser le `.zip` (ou le `SKILL.md`), puis Import. La compétence est activée par défaut.

Contraintes : un seul `SKILL.md`, à la racine ou dans un dossier de premier niveau ; 100 Mo ; 100 fichiers au plus. Nos zips les respectent (test `outils/test_construire_zip.py`).

Source : https://docs.cloud.google.com/gemini/enterprise/docs/skills (lu le 17/11/2026)
