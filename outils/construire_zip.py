#!/usr/bin/env python3
"""Fabrique un zip par compétence, prêt à téléverser dans Claude, ChatGPT ou Gemini.

Chaque zip contient un seul dossier au nom de la compétence, avec SKILL.md et references/.
C'est la forme que demande claude.ai (« un fichier ZIP contenant le dossier du skill »,
le dossier portant le nom du skill) et que Gemini Enterprise accepte (SKILL.md dans un
dossier de premier niveau). Les fichiers cachés et compilés sont exclus, comme Gemini le demande.

Chaque zip est reproductible, octet pour octet, sur Linux, macOS et Windows :
- entrées triées sur leur chemin en « / », jamais sur l'ordre du système de fichiers ;
- fins de ligne des fichiers texte ramenées à LF (Git sous Windows peut les convertir en CRLF) ;
- date, permissions et « système d'origine » fixés (zipfile met 0 sous Windows, 3 ailleurs) ;
- pas de compression (ZIP_STORED) : la sortie ne dépend pas de la version de zlib.
Le test peut donc vérifier que dist/ est à jour, quelle que soit la plateforme.

Usage, depuis la racine du dépôt :
  python3 outils/construire_zip.py              écrit dist/<compétence>.zip pour chaque compétence
  python3 outils/construire_zip.py --verifier   échoue si un zip de dist/ n'est pas à jour
"""

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_SKILLS = RACINE / "plugins/lettershop/skills"
DIST = RACINE / "dist"

DATE_FIXE = (1980, 1, 1, 0, 0, 0)
EXCLUS = re.compile(r"(^|/)(\.[^/]*|__pycache__)(/|$)|\.pyc$")
EXTENSIONS_TEXTE = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".py", ".html"}
SYSTEME_UNIX = 3
TAILLE_MAX = 100 * 1024 * 1024  # 100 Mo, limite citée par Gemini
FICHIERS_MAX = 100  # limite citée par Gemini Enterprise


class ErreurZip(Exception):
    """Le zip ne serait pas accepté tel quel."""


def competences() -> list:
    """Les noms des compétences : chaque dossier de DOSSIER_SKILLS qui contient un SKILL.md."""
    return sorted(p.parent.name for p in DOSSIER_SKILLS.glob("*/SKILL.md"))


def sortie(nom: str) -> Path:
    return DIST / f"{nom}.zip"


def fichiers_a_inclure(nom: str, dossier_skills: Path = None) -> list:
    dossier = (dossier_skills or DOSSIER_SKILLS) / nom
    if not (dossier / "SKILL.md").is_file():
        raise ErreurZip(f"SKILL.md introuvable dans {dossier}")
    fichiers = []
    for chemin in dossier.rglob("*"):
        relatif = chemin.relative_to(dossier).as_posix()
        if chemin.is_file() and not EXCLUS.search(relatif):
            fichiers.append((f"{nom}/{relatif}", chemin))
    # Tri sur le chemin en « / », identique sur toutes les plateformes.
    return [(chemin, nom_zip) for nom_zip, chemin in sorted(fichiers, key=lambda f: f[0])]


def contenu_normalise(chemin: Path) -> bytes:
    """Les octets du fichier, avec des fins de ligne LF pour les fichiers texte."""
    donnees = chemin.read_bytes()
    if chemin.suffix.lower() in EXTENSIONS_TEXTE:
        donnees = donnees.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return donnees


def nom_du_frontmatter(texte: str) -> str:
    bloc = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    if not bloc:
        raise ErreurZip("SKILL.md doit commencer par un frontmatter entre deux lignes ---")
    nom = re.search(r"^name:\s*(\S+)\s*$", bloc.group(1), re.M)
    if not nom:
        raise ErreurZip("Le frontmatter n'a pas de champ name")
    return nom.group(1)


def construire(nom: str, dossier_skills: Path = None) -> bytes:
    racine = dossier_skills or DOSSIER_SKILLS
    declare = nom_du_frontmatter(contenu_normalise(racine / nom / "SKILL.md").decode("utf-8"))
    if declare != nom:
        raise ErreurZip(f"Le name du SKILL.md ({declare}) doit être le nom du dossier ({nom})")
    fichiers = fichiers_a_inclure(nom, racine)
    if len(fichiers) > FICHIERS_MAX:
        raise ErreurZip(f"{len(fichiers)} fichiers : la limite est {FICHIERS_MAX}")
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, "w", compression=zipfile.ZIP_STORED) as archive:
        for chemin, nom_dans_zip in fichiers:
            info = zipfile.ZipInfo(nom_dans_zip, date_time=DATE_FIXE)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = SYSTEME_UNIX
            info.external_attr = (0o100644 << 16)
            archive.writestr(info, contenu_normalise(chemin))
    contenu = tampon.getvalue()
    if len(contenu) > TAILLE_MAX:
        raise ErreurZip("Le zip dépasse 100 Mo")
    return contenu


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", action="store_true", help="vérifie que dist/ est à jour, sans l'écrire")
    args = parser.parse_args(argv)
    resultat = 0
    for nom in competences():
        try:
            contenu = construire(nom)
        except ErreurZip as erreur:
            print(f"Erreur : {nom} : {erreur}", file=sys.stderr)
            return 2
        cible = sortie(nom)
        if args.verifier:
            actuel = cible.read_bytes() if cible.exists() else b""
            if actuel != contenu:
                print(f"{cible.relative_to(RACINE)} n'est pas à jour. Lance : python3 outils/construire_zip.py", file=sys.stderr)
                resultat = 1
            else:
                print(f"{cible.relative_to(RACINE)} est à jour ({len(contenu)} octets).")
            continue
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_bytes(contenu)
        print(f"Écrit : {cible.relative_to(RACINE)} ({len(contenu)} octets).")
    if not args.verifier:
        attendus = {sortie(n).name for n in competences()}
        for orphelin in sorted(p for p in DIST.glob("*.zip") if p.name not in attendus):
            orphelin.unlink()
            print(f"Supprimé : {orphelin.relative_to(RACINE)} (plus de compétence de ce nom).")
    return resultat


if __name__ == "__main__":
    sys.exit(main())
