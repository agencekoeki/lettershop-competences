#!/usr/bin/env python3
"""Produit les consignes publiques à partir des SKILL.md, pour que les deux ne divergent jamais.

Pour chaque compétence de la liste COMPETENCES, la consigne est le bloc compris entre
les marqueurs <!-- consigne:debut --> et <!-- consigne:fin --> de son SKILL.md.
Le script le transforme en texte brut (sans balisage Markdown) et l'écrit dans consignes/.

Usage, depuis la racine du dépôt :
  python3 outils/generer_consigne.py                      écrit tous les fichiers .txt
  python3 outils/generer_consigne.py --verifier           échoue si un .txt n'est pas à jour
  python3 outils/generer_consigne.py --verifier-html page.html
                                                          échoue si la page affiche un autre texte
                                                          (chaque compétence a son id dans la page)
"""

import argparse
import html
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_SKILLS = RACINE / "plugins/lettershop/skills"

DEBUT = "<!-- consigne:debut -->"
FIN = "<!-- consigne:fin -->"
CARACTERES_INTERDITS = "[]<>&"

# Passage qui parle de la compétence installable à l'IA du client, présent dans chaque consigne.
TITRE_PASSAGE_SKILL = "La version installable de ces consignes"
# URL du dépôt public. Si le dépôt redevient privé, repasser URL_DEPOT_PROVISOIRE à True :
# le script rappellera alors, à chaque génération, que le lien donné aux clients ne marche pas.
URL_DEPOT = "https://github.com/agencekoeki/lettershop-competences"
URL_DEPOT_PROVISOIRE = False


@dataclass(frozen=True)
class Competence:
    nom: str  # nom du dossier et du champ name du SKILL.md
    fichier: str  # nom du fichier écrit dans consignes/
    phrase_repere: str  # phrase qui permet à Lettershop de compter les demandes
    id_html: str  # id de l'élément qui affiche la consigne sur la page du site

    @property
    def skill(self) -> Path:
        return DOSSIER_SKILLS / self.nom / "SKILL.md"

    @property
    def sortie(self) -> Path:
        return RACINE / "consignes" / self.fichier


COMPETENCES = [
    Competence(
        nom="lettershop-demande-de-devis",
        fichier="preparer-ma-demande-de-devis.txt",
        phrase_repere="Demande préparée avec les consignes Lettershop.",
        id_html="texte-consigne",
    ),
    Competence(
        nom="lettershop-apercu-enseigne",
        fichier="obtenir-un-apercu-realiste.txt",
        phrase_repere="Aperçu préparé avec les consignes Lettershop.",
        id_html="texte-consigne-apercu",
    ),
]


class ErreurConsigne(Exception):
    """La consigne ne peut pas être produite telle quelle."""


def extraire_bloc(texte_skill: str) -> str:
    """Rend le bloc entre les marqueurs, qui doivent être présents une seule fois chacun."""
    if texte_skill.count(DEBUT) != 1 or texte_skill.count(FIN) != 1:
        raise ErreurConsigne(
            f"Il faut exactement un marqueur {DEBUT} et un marqueur {FIN} dans le SKILL.md."
        )
    debut = texte_skill.index(DEBUT) + len(DEBUT)
    fin = texte_skill.index(FIN)
    if fin < debut:
        raise ErreurConsigne("Le marqueur de fin précède le marqueur de début.")
    return texte_skill[debut:fin]


def en_texte_brut(bloc: str) -> str:
    """Retire le balisage Markdown que le client n'a pas à voir."""
    lignes = []
    for ligne in bloc.strip("\n").splitlines():
        ligne = ligne.rstrip()
        ligne = re.sub(r"^#{1,6}\s+", "", ligne)  # titres
        ligne = ligne.replace("**", "").replace("`", "")  # gras, code
        lignes.append(ligne)
    texte = "\n".join(lignes)
    texte = re.sub(r"\n{3,}", "\n\n", texte)  # pas plus d'une ligne vide
    return texte.strip() + "\n"


def controler(consigne: str, competence: Competence) -> None:
    """Refuse une consigne qui exposerait au client une note interne ou casserait la mesure."""
    interdits = sorted({c for c in consigne if c in CARACTERES_INTERDITS})
    if interdits:
        raise ErreurConsigne(
            f"{competence.nom} : la consigne contient des caractères réservés aux notes internes ou au HTML : "
            + " ".join(interdits)
        )
    if consigne.count(competence.phrase_repere) != 1:
        raise ErreurConsigne(f"{competence.nom} : la phrase-repère « {competence.phrase_repere} » doit figurer une seule fois.")
    if consigne.count(TITRE_PASSAGE_SKILL) != 1:
        raise ErreurConsigne(f"{competence.nom} : le passage « {TITRE_PASSAGE_SKILL} » doit figurer une seule fois.")
    if consigne.count(URL_DEPOT) != 1:
        raise ErreurConsigne(f"{competence.nom} : l'URL du dépôt ({URL_DEPOT}) doit figurer une seule fois.")
    urls_github = re.findall(r"https://github\.com/\S+", consigne)
    if any(u.rstrip(".,;:") != URL_DEPOT for u in urls_github):
        raise ErreurConsigne(f"{competence.nom} : la consigne cite une autre URL GitHub que URL_DEPOT.")
    autres_reperes = [c.phrase_repere for c in COMPETENCES if c is not competence and c.phrase_repere in consigne]
    if autres_reperes:
        raise ErreurConsigne(f"{competence.nom} : la consigne contient la phrase-repère d'une autre compétence.")


def avertissements(consigne: str) -> list:
    """Ce qui n'empêche pas de produire la consigne, mais doit se voir à chaque génération."""
    messages = []
    if URL_DEPOT_PROVISOIRE and URL_DEPOT in consigne:
        messages.append(
            f"URL provisoire : le dépôt {URL_DEPOT} n'est pas public. "
            "Les liens donnés aux clients ne marcheront qu'une fois le dépôt public."
        )
    return messages


def produire(competence: Competence) -> str:
    consigne = en_texte_brut(extraire_bloc(competence.skill.read_text(encoding="utf-8")))
    controler(consigne, competence)
    return consigne


class _LecteurElement(HTMLParser):
    """Récupère le texte de l'élément dont l'id est donné."""

    def __init__(self, ident: str):
        super().__init__(convert_charrefs=True)
        self.ident = ident
        self.profondeur = 0
        self.morceaux: list = []
        self.trouve = False

    def handle_starttag(self, tag, attrs):
        if self.profondeur:
            self.profondeur += 1
        elif dict(attrs).get("id") == self.ident:
            self.profondeur = 1
            self.trouve = True

    def handle_endtag(self, tag):
        if self.profondeur:
            self.profondeur -= 1

    def handle_data(self, data):
        if self.profondeur:
            self.morceaux.append(data)


def texte_dans_html(page: str, ident: str) -> str:
    lecteur = _LecteurElement(ident)
    lecteur.feed(page)
    if not lecteur.trouve:
        raise ErreurConsigne(f"Aucun élément avec l'id « {ident} » dans la page.")
    return html.unescape("".join(lecteur.morceaux)).strip() + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", action="store_true", help="vérifie que les .txt sont à jour, sans les écrire")
    parser.add_argument("--verifier-html", metavar="PAGE", help="vérifie le texte affiché par une page HTML")
    args = parser.parse_args(argv)

    consignes = {}
    try:
        for competence in COMPETENCES:
            consignes[competence.nom] = produire(competence)
    except ErreurConsigne as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 2
    messages = {m for c in consignes.values() for m in avertissements(c)}
    for message in sorted(messages):
        print(f"Attention : {message}", file=sys.stderr)

    if args.verifier_html:
        page = Path(args.verifier_html).read_text(encoding="utf-8")
        resultat = 0
        for competence in COMPETENCES:
            try:
                affiche = texte_dans_html(page, competence.id_html)
            except ErreurConsigne as erreur:
                print(f"Erreur : {competence.nom} : {erreur}", file=sys.stderr)
                resultat = max(resultat, 2)
                continue
            if affiche != consignes[competence.nom]:
                print(f"{competence.nom} : la page n'affiche pas la consigne du SKILL.md. Régénère-la.", file=sys.stderr)
                resultat = max(resultat, 1)
            else:
                print(f"{competence.nom} : la page affiche exactement la consigne du SKILL.md.")
        return resultat

    if args.verifier:
        resultat = 0
        for competence in COMPETENCES:
            consigne = consignes[competence.nom]
            actuel = competence.sortie.read_text(encoding="utf-8") if competence.sortie.exists() else ""
            if actuel != consigne:
                print(f"{competence.sortie.relative_to(RACINE)} n'est pas à jour. Lance : python3 outils/generer_consigne.py", file=sys.stderr)
                resultat = 1
            else:
                print(f"{competence.sortie.relative_to(RACINE)} est à jour ({len(consigne)} caractères).")
        return resultat

    for competence in COMPETENCES:
        consigne = consignes[competence.nom]
        competence.sortie.parent.mkdir(parents=True, exist_ok=True)
        competence.sortie.write_text(consigne, encoding="utf-8", newline="\n")
        print(f"Écrit : {competence.sortie.relative_to(RACINE)} ({len(consigne)} caractères).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
