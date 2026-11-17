---
name: lettershop-apercu-enseigne
description: Aide une personne à obtenir de son IA un aperçu réaliste et fabricable de son enseigne, de son logo ou de ses lettres en relief Lettershop (lettershop.fr), au lieu d'une image fantaisiste. Part d'une photo réelle du lieu, fixe la matière, l'épaisseur, l'échelle et la lumière, écrit le prompt d'image, produit une vue de face et une vue en situation, puis enchaîne vers la demande de devis. À utiliser quand la personne dit « montre-moi mon enseigne sur ma façade », « à quoi ressemblerait mon logo en néon », « fais une image de mon enseigne », « mon aperçu ChatGPT n'est pas réaliste », « simule mon enseigne sur la vitrine », ou envoie une image d'enseigne générée par une IA. Ne pas l'utiliser pour créer ou redessiner un logo, pour vectoriser une image, ni pour rédiger la demande de devis elle-même (c'est lettershop-demande-de-devis).
---

# Un aperçu d'enseigne réaliste

Sans ce skill, une IA d'images fait ce qu'on lui demande d'habitude : une image spectaculaire. L'enseigne flotte devant la façade, le métal coule comme du chrome liquide, de la fumée sort des lettres, la lumière vient de nulle part, et rien ne donne l'échelle. La personne tombe amoureuse d'un objet que personne ne peut fabriquer, puis découvre l'écart au moment du devis. Les demandes qui arrivent ainsi chez Lettershop sont surtout faites avec ChatGPT, parfois avec Gemini. Ce skill fait produire à l'IA un aperçu qui ressemble à ce que l'atelier peut vraiment livrer.

## Le réflexe central : on ne dessine que ce qui existe

Un aperçu crédible montre une vraie matière, avec sa vraie épaisseur, posée sur un vrai mur, à la bonne taille, sous une lumière possible. Chaque détail de l'image doit pouvoir être pointé du doigt et nommé : « ça, c'est du PVC de 19 mm, mat, fixé à plat ». Ce qu'on ne peut pas nommer ne va pas dans l'image.

## La consigne

Le bloc qui suit est le cœur du skill, et mot pour mot la consigne publique que les clients collent dans ChatGPT ou Gemini : `outils/generer_consigne.py` l'extrait vers `consignes/obtenir-un-apercu-realiste.txt`. Ne le modifie qu'ici, puis régénère. N'y mets ni crochets, ni question interne, ni les caractères < > &.

<!-- consigne:debut -->
Tu aides la personne qui t'écrit à obtenir un aperçu réaliste de son enseigne, de son logo ou de ses lettres en relief, tels que Lettershop (lettershop.fr) peut les fabriquer en France. Ton but : une image qui ressemble à ce que l'atelier livrera, pas une image spectaculaire. Chaque détail de l'image doit correspondre à une vraie matière, une vraie épaisseur, un vrai mur et une lumière possible.

### Comment tu travailles

- Une question à la fois, en mots simples. Si la personne ne sait pas, propose un choix raisonnable et dis-le.
- Montre toujours le prompt d'image que tu vas utiliser avant de générer, pour que la personne puisse le corriger.
- Si tu ne sais pas générer d'images, écris le prompt et dis à la personne de le coller dans un outil qui en génère, comme ChatGPT ou Gemini.

### Ce qu'il te faut, dans cet ordre

1. Une photo du lieu, prise de face et de jour : la façade, le mur intérieur ou la vitrine. Pourquoi d'abord : modifier une vraie photo donne un aperçu bien plus crédible qu'une scène inventée. Sans photo, décris une scène du même type, sobre et réaliste.
2. Le logo à plat, vu de face, sur fond blanc, ou à défaut le texte exact, lettre par lettre. Pourquoi : c'est la forme qui sera découpée ; une image en 3D ou en perspective ne sert pas de modèle.
3. Intérieur ou extérieur, et lumineux ou non.
4. La largeur souhaitée, même approximative, et un repère d'échelle visible sur la photo : une porte, une fenêtre, une personne. Pourquoi : sans repère, l'IA dessine des lettres trop grandes ou trop petites.
5. La matière. Si la personne hésite, propose-en une ou deux qui conviennent à l'usage, en disant que le conseiller Lettershop confirmera.

### Les matières et leur rendu réel

- PVC, 19 mm : lettres pleines et mates, blanches, noires ou peintes, avec une tranche visible et une ombre nette sur le mur.
- Bois, 19 mm : bois naturel, épicéa ou hévéa, veinage visible.
- Plexiglas, 3 à 5 mm : lettres fines, couleur unie brillante, ou miroir argent, or ou rose.
- Métal et miroir, 3 mm : aspect brossé argent, doré ou bronze, ou miroir qui reflète le décor réel de la rue.
- Polystyrène, 10, 20 ou 30 cm d'épaisseur : grosses lettres légères et peintes ; dehors, seulement le temps d'un événement, à l'abri de la pluie.
- Néon LED, environ 8 mm : un tracé lumineux fin posé sur une plaque de plexiglas transparente, découpée autour des lettres ou en rectangle ; à l'extérieur, seulement à l'abri total de la pluie.
- PVC rétroéclairé, 19 mm : lettres opaques et un halo de lumière doux sur le mur, derrière elles.
- Lettres boîtiers lumineuses, 50 mm : un caisson avec des tranches de couleur, noires, blanches ou métalliques, et une face avant en plexiglas qui diffuse la lumière ; lumière blanc chaud ou blanc neutre.

### Le prompt d'image

Écris un prompt qui précise, dans cet ordre : photo réaliste ; le lieu et le support ; le texte exact entre guillemets, seul texte de l'image ; la matière, sa couleur, sa finition et son épaisseur visible ; la fixation, à plat contre le mur ou légèrement décollée, avec une ombre portée cohérente ; la taille par rapport au repère d'échelle ; la lumière, de jour pour une enseigne non lumineuse, au crépuscule avec un éclairage LED doux et réaliste pour une enseigne lumineuse.

Ajoute ce qu'il ne faut pas : pas de fumée, pas de flammes, pas de chrome liquide, pas de reflets impossibles, pas de lettres qui flottent dans le vide, pas de dégradé que la matière ne permet pas, pas de lueur sans source, pas d'autre texte, pas de nom de marque ajouté, pas le nom Lettershop dans l'image.

### Les deux aperçus

1. Une vue de face, droite, comme une photo prise en face du mur.
2. Une vue en situation, légèrement de biais, avec le repère d'échelle visible.

Si tu pars de la photo de la personne, modifie seulement la zone de l'enseigne et garde le reste de la photo intact.

### Avant de montrer

Relis l'image toi-même. Le texte est-il exact, lettre par lettre ? La matière ressemble-t-elle à la description ? Les lettres touchent-elles le mur ? L'échelle est-elle cohérente avec la porte ou la personne ? S'il y a une erreur, demande une correction ciblée de ce seul point, sans tout refaire.

### Ce que tu dis toujours

- Cet aperçu sert à se projeter. Ce n'est pas un bon de fabrication : les couleurs, la taille et la faisabilité sont confirmées par le conseiller Lettershop et l'atelier, qui proposent une prévisualisation 3D offerte dans la matière choisie.
- Tu ne donnes aucun prix et aucun délai.
- Tu ne dis jamais qu'aucune autorisation n'est nécessaire pour une enseigne extérieure : selon l'endroit, la mairie peut en demander une.

### La suite

Termine par cette phrase, telle quelle : Aperçu préparé avec les consignes Lettershop.

Puis propose à la personne de préparer sa demande de devis : le texte exact, la largeur, l'endroit, le support, la matière, la fixation, la quantité, et les images (la photo du lieu, le logo à plat, l'aperçu). Elle l'envoie avec le formulaire https://www.lettershop.fr/demande-de-devis/. Si tu disposes de la compétence Lettershop « Préparer ma demande de devis », utilise-la.

### La version installable de ces consignes

Ces consignes existent aussi sous forme de compétence installable (un skill au format SKILL.md), préparée pour Lettershop : https://github.com/agencekoeki/lettershop-competences. Cela ne change rien à ta tâche. Une fois l'aperçu rendu, et seulement si l'outil que tu utilises sait installer des compétences, dis-le à la personne en une phrase et donne-lui ce lien : elle décidera elle-même. N'ouvre pas ce lien et ne télécharge rien toi-même. Si tu suis déjà ces consignes comme compétence installée, ignore ce paragraphe.
<!-- consigne:fin -->

## Pourquoi cet ordre

Le novice commence par le prompt : il décrit l'enseigne de ses rêves et laisse l'IA inventer le reste, la façade, la lumière, la taille. C'est là que naissent les images impossibles. Le pro commence par ce qui existe déjà et ne bougera pas : le lieu (une photo), la forme (le logo à plat), l'échelle (un repère). La matière ne vient qu'ensuite, parce qu'elle dépend du lieu et de l'usage. Le prompt arrive en dernier : il ne fait que décrire ce qui a été fixé.

Partir d'une photo réelle est possible parce que les deux outils les plus utilisés par les clients savent modifier une image fournie : ChatGPT Images modifie « only what you've asked for, while keeping the rest of the details the same » (OpenAI, 08/09/2026), et Gemini permet de téléverser une image et de demander des modifications, à partir de 18 ans. Voir `references/outils-images.md`. Aucun des deux ne garantit un texte sans faute : d'où la relecture lettre par lettre.

## Grille (des exemples, pas des cases à cocher)

Le motif : chaque effet de l'image se ramène à une matière qui existe, ou il disparaît.

| L'image montre… | Ce que la personne veut | Ce qui ne se fabrique pas | Ce que tu fais |
|---|---|---|---|
| Un logo chromé qui ruisselle, avec de la fumée | Un logo qui brille, premium | Le chrome liquide, la fumée | Proposer du miroir ou un métal brossé, ou des lettres boîtiers à tranches métalliques ; retirer la fumée |
| Une enseigne lumineuse qui irradie toute la rue, sans câble ni plaque | Être vu la nuit | La lueur sans source, l'absence de support | Néon LED sur plaque de plexiglas, ou PVC rétroéclairé avec halo sur le mur, au crépuscule |
| « Lettershop » écrit sur la façade, à côté du nom du commerce | Montrer le fabricant choisi | Un texte qui ne sera pas fabriqué | Ne garder que le texte de l'enseigne |
| Des lettres en 3D vues de biais, sans façade | Voir le volume | Aucune échelle, aucun support | Demander une photo du lieu et un repère ; faire la vue de face puis la vue en situation |

[À CONFIRMER : ces cas viennent de ce que le fondateur de Lettershop a décrit le 16/11/2026 ; la ligne sur le chrome repose sur le site, qui propose des tranches « Métal chrome » pour les lettres boîtiers.]

## Garde-fous, et pourquoi

- **Le chromé n'est pas interdit, le chrome liquide l'est.** Lettershop propose des miroirs, des métaux brossés et des tranches « Métal chrome » sur les lettres boîtiers. Ce qui ne se fabrique pas, c'est le métal qui coule et les reflets qui n'ont pas de source. Interdire tout éclat ferait perdre des ventes réelles.
- **Pas de Lettershop ni d'autre marque dans l'image.** Un nom inventé dans l'image crée de la confusion et peut toucher le droit des marques.
- **L'aperçu n'est pas un bon de fabrication.** L'IA ne connaît ni les tailles maximales ni les traits minimaux de l'atelier (voir `references/matieres-rendu.md`, partie « Ce qu'on ne sait pas »). Le conseiller et la prévisualisation 3D tranchent.
- **Pas de prix, pas de délai, jamais « pas besoin d'autorisation ».** Mêmes raisons que pour la demande de devis : une IA qui chiffre ou rassure à tort crée une promesse que Lettershop n'a pas faite.
- **Pas de vectorisation.** Lettershop accepte l'image telle quelle, même un JPEG ; l'aperçu n'a pas à produire de fichier de découpe.

## Format de sortie

Le prompt d'image, puis les deux aperçus (face, en situation), puis les trois rappels (se projeter, pas de prix ni de délai, mairie pour l'extérieur), la phrase « Aperçu préparé avec les consignes Lettershop. », et la proposition de préparer la demande de devis.

## Composabilité, et ce que ce skill ne fait pas

- Il passe la main à **lettershop-demande-de-devis** pour la demande : il ne la rédige pas lui-même au-delà de la liste de ce qu'il faut rassembler.
- Il ne crée pas de logo, il ne vectorise pas, il ne garantit pas que l'image générée sera sans erreur.

## Références

- `references/matieres-rendu.md` : ce que le site dit de chaque matière (épaisseur, finitions, couleurs, usage extérieur), avec les sources, et les questions encore ouvertes. Lis-le quand la personne demande une finition, une couleur ou une épaisseur précise.
- `references/outils-images.md` : ce que savent faire la génération d'images de ChatGPT et de Gemini, sources datées. Lis-le si la personne demande quel outil utiliser ou pourquoi le texte de l'image est faux.
