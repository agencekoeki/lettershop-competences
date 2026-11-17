"""Tests de outils/construire_zip.py.

Lancer depuis la racine du dépôt :
  python3 -m unittest discover -s outils -p "test_*.py" -v
"""

import io
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import construire_zip as cz  # noqa: E402


class TestZips(unittest.TestCase):
    def test_au_moins_deux_competences(self):
        self.assertGreaterEqual(len(cz.competences()), 2)

    def test_dist_ne_contient_que_les_zips_attendus(self):
        attendus = {cz.sortie(n).name for n in cz.competences()}
        self.assertEqual({p.name for p in cz.DIST.glob("*.zip")}, attendus)

    def test_chaque_zip(self):
        for nom in cz.competences():
            with self.subTest(nom):
                contenu = cz.construire(nom)
                archive = zipfile.ZipFile(io.BytesIO(contenu))
                noms = archive.namelist()
                # à jour et reproductible
                self.assertEqual(cz.sortie(nom).read_bytes(), contenu)
                self.assertEqual(cz.construire(nom), contenu)
                # un seul dossier, au nom du skill, avec un seul SKILL.md
                self.assertEqual({n.split("/")[0] for n in noms}, {nom})
                self.assertIn(f"{nom}/SKILL.md", noms)
                self.assertEqual(sum(n.endswith("SKILL.md") for n in noms), 1)
                # le name du frontmatter est le nom du dossier, et le SKILL.md est celui du dépôt
                skill = archive.read(f"{nom}/SKILL.md")
                self.assertEqual(cz.nom_du_frontmatter(skill.decode("utf-8")), nom)
                self.assertEqual(skill, (cz.DOSSIER_SKILLS / nom / "SKILL.md").read_bytes())
                # ni fichier caché, ni compilé, ni remontée
                for n in noms:
                    morceaux = n.split("/")
                    self.assertFalse(any(m.startswith(".") for m in morceaux), n)
                    self.assertNotIn("..", morceaux, n)
                    self.assertFalse(n.endswith(".pyc"), n)
                # limites citées par Gemini
                self.assertLessEqual(len(noms), cz.FICHIERS_MAX)
                self.assertLessEqual(len(contenu), cz.TAILLE_MAX)
                self.assertLessEqual(max(n.count("/") for n in noms), 10)

    def test_exclusion(self):
        for chemin in (".DS_Store", "references/.cache", "__pycache__/x.pyc", "a.pyc"):
            self.assertTrue(cz.EXCLUS.search(chemin), chemin)
        for chemin in ("SKILL.md", "references/faits-lettershop.md"):
            self.assertFalse(cz.EXCLUS.search(chemin), chemin)


if __name__ == "__main__":
    unittest.main()
