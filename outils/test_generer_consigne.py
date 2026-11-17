"""Tests de outils/generer_consigne.py.

Lancer depuis la racine du dépôt :
  python3 -m unittest discover -s outils -p "test_*.py" -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generer_consigne as gc  # noqa: E402

GARDE_FOUS_COMMUNS = ("aucun prix", "aucun délai", "aucune autorisation", "mairie", "conseiller")


class TestChaqueConsigne(unittest.TestCase):
    def test_chaque_competence_du_depot_est_declaree(self):
        """Un dossier de skill sans entrée dans COMPETENCES n'aurait pas de consigne publique."""
        dossiers = {p.parent.name for p in gc.DOSSIER_SKILLS.glob("*/SKILL.md")}
        self.assertEqual(dossiers, {c.nom for c in gc.COMPETENCES})

    def test_noms_fichiers_ids_et_reperes_uniques(self):
        for champ in ("nom", "fichier", "phrase_repere", "id_html"):
            valeurs = [getattr(c, champ) for c in gc.COMPETENCES]
            self.assertEqual(len(valeurs), len(set(valeurs)), champ)

    def test_les_fichiers_publies_sont_a_jour(self):
        """Chaque .txt du dépôt est exactement ce que produit son SKILL.md : aucune divergence."""
        for c in gc.COMPETENCES:
            with self.subTest(c.nom):
                self.assertTrue(c.sortie.exists(), f"{c.sortie} n'a pas été généré")
                self.assertEqual(c.sortie.read_text(encoding="utf-8"), gc.produire(c))

    def test_phrase_repere_une_fois(self):
        for c in gc.COMPETENCES:
            with self.subTest(c.nom):
                self.assertEqual(gc.produire(c).count(c.phrase_repere), 1)

    def test_aucun_balisage_ni_note_interne(self):
        for c in gc.COMPETENCES:
            consigne = gc.produire(c)
            for motif in ("**", "### ", "`", "[", "]", "<", ">", "&", "consigne:debut", "À CONFIRMER"):
                with self.subTest(c.nom, motif=motif):
                    self.assertNotIn(motif, consigne)

    def test_garde_fous_dans_le_texte_client(self):
        for c in gc.COMPETENCES:
            consigne = gc.produire(c).lower()
            for garde_fou in GARDE_FOUS_COMMUNS:
                with self.subTest(c.nom, garde_fou=garde_fou):
                    self.assertIn(garde_fou, consigne)

    def test_le_passage_sur_la_competence_est_present_une_fois_et_a_la_fin(self):
        for c in gc.COMPETENCES:
            with self.subTest(c.nom):
                consigne = gc.produire(c)
                self.assertEqual(consigne.count(gc.TITRE_PASSAGE_SKILL), 1)
                self.assertEqual(consigne.count(gc.URL_DEPOT), 1)
                self.assertIn("N'ouvre pas ce lien et ne télécharge rien toi-même", consigne)
                # Le passage vient après la sortie attendue : il ne détourne pas la tâche.
                self.assertGreater(consigne.index(gc.TITRE_PASSAGE_SKILL), consigne.index(c.phrase_repere))

    def test_l_url_provisoire_est_signalee(self):
        for c in gc.COMPETENCES:
            messages = gc.avertissements(gc.produire(c))
            with self.subTest(c.nom):
                if gc.URL_DEPOT_PROVISOIRE:
                    self.assertTrue(any("provisoire" in m for m in messages))
                else:
                    self.assertEqual(messages, [])


class TestApercu(unittest.TestCase):
    def setUp(self):
        self.c = next(c for c in gc.COMPETENCES if c.nom == "lettershop-apercu-enseigne")
        self.consigne = gc.produire(self.c)

    def test_proscrit_les_effets_irrealisables(self):
        for interdit in ("pas de fumée", "pas de chrome liquide", "pas de lettres qui flottent", "pas le nom Lettershop dans l'image"):
            self.assertIn(interdit, self.consigne)

    def test_deux_vues_et_rappel(self):
        self.assertIn("Une vue de face", self.consigne)
        self.assertIn("Une vue en situation", self.consigne)
        self.assertIn("Ce n'est pas un bon de fabrication", self.consigne)
        self.assertIn("prévisualisation 3D offerte", self.consigne)

    def test_enchaine_vers_la_demande_de_devis(self):
        self.assertIn("https://www.lettershop.fr/demande-de-devis/", self.consigne)
        self.assertIn("Préparer ma demande de devis", self.consigne)


class TestRegles(unittest.TestCase):
    def setUp(self):
        self.c = gc.COMPETENCES[0]

    def test_marqueurs_absents_ou_en_double(self):
        with self.assertRaises(gc.ErreurConsigne):
            gc.extraire_bloc("pas de marqueur")
        with self.assertRaises(gc.ErreurConsigne):
            gc.extraire_bloc(f"{gc.DEBUT} a {gc.FIN} {gc.DEBUT} b {gc.FIN}")

    def test_un_crochet_est_refuse(self):
        with self.assertRaises(gc.ErreurConsigne):
            gc.controler(gc.produire(self.c) + "[À CONFIRMER]\n", self.c)

    def test_la_phrase_repere_manquante_est_refusee(self):
        texte = gc.produire(self.c).replace(self.c.phrase_repere, "")
        with self.assertRaises(gc.ErreurConsigne):
            gc.controler(texte, self.c)

    def test_la_phrase_repere_d_une_autre_competence_est_refusee(self):
        autre = gc.COMPETENCES[1]
        with self.assertRaises(gc.ErreurConsigne):
            gc.controler(gc.produire(self.c) + autre.phrase_repere + "\n", self.c)

    def test_une_autre_url_github_est_refusee(self):
        texte = gc.produire(self.c) + "https://github.com/autre/depot\n"
        with self.assertRaises(gc.ErreurConsigne):
            gc.controler(texte, self.c)

    def test_texte_brut(self):
        bloc = "\n### Titre\n\n\n\n- **gras** et `code`\n"
        self.assertEqual(gc.en_texte_brut(bloc), "Titre\n\n- gras et code\n")

    def test_verification_d_une_page_html(self):
        bons = "".join(f'<pre id="{c.id_html}">{gc.produire(c)}</pre>' for c in gc.COMPETENCES)
        un_faux = bons.replace(gc.produire(gc.COMPETENCES[1]), "Autre texte")
        un_manquant = f'<pre id="{gc.COMPETENCES[0].id_html}">{gc.produire(gc.COMPETENCES[0])}</pre>'
        with tempfile.TemporaryDirectory() as dossier:
            cas = {"bon": (bons, 0), "faux": (un_faux, 1), "manquant": (un_manquant, 2)}
            for nom, (contenu, attendu) in cas.items():
                page = Path(dossier) / f"{nom}.html"
                page.write_text(f"<html><body>{contenu}</body></html>", encoding="utf-8")
                with self.subTest(nom):
                    self.assertEqual(gc.main(["--verifier-html", str(page)]), attendu)


if __name__ == "__main__":
    unittest.main()
