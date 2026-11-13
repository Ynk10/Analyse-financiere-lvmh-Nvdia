# Analyse financière comparée : LVMH vs NVIDIA

Projet Python for Finance, MBA 1 Finance & Data Performance, ESLSCA Business School.

Analyse du rendement, du risque et de la tendance de deux actions cotées, **LVMH** (MC.PA, EUR) et **NVIDIA** (NVDA, USD), à partir de leur historique journalier de prix, avec `pandas` et `matplotlib`.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `projet_python_LVMH_NVDA.py` | Script d'analyse (10 fonctions commentées) |
| `LVMH_oct_2022_2026.xlsx`, `NVDA_oct_2022_2026.xlsx` | Données de prix journalières (une feuille par actif) |
| `graphique_LVMH.png`, `graphique_NVDA.png` | Prix et moyenne mobile 20 séances (générés par le script) |
| `note_interpretation` | Note de lecture économique des résultats |

## Données

- **Période** : 28/10/2022 au 30/10/2026 (1 024 séances pour LVMH, 1 005 pour NVIDIA)
- **Fréquence** : journalière
- **Source** : historiques téléchargés au format Excel (Investing.com)
- **Colonnes utilisées** : `Date` et `Dernier` (prix de clôture)
- Chaque actif est analysé en **monnaie locale** (pas de conversion EUR/USD) ; taux sans risque fixé à **0**.

## Installation et utilisation

```bash
pip install pandas numpy matplotlib openpyxl python-pptx
python projet_python_LVMH_NVDA.py   # analyse + graphiques PNG

```

Les fichiers Excel doivent se trouver dans le même dossier que les scripts.

## Méthodologie

Le script suit 10 étapes, chacune écrite sous forme de fonction :

1. Importation et aperçu des colonnes
2. Remise en ordre chronologique et statistiques descriptives
3. Rendements journaliers : `P(t) / P(t-1) - 1`
4. Rendement moyen, annualisé en intérêts composés : `(1 + moyenne)^252 - 1`
5. Volatilité annualisée : `écart-type × √252`
6. Performance buy and hold : `P(fin) / P(début) - 1`
7. Moyenne mobile sur 20 séances
8. Maximum drawdown : plus forte baisse entre un sommet et un creux de la courbe de capital
9. Ratio de Sharpe annualisé : `(rendement moyen journalier - taux sans risque) / écart-type × √252`
10. Graphique prix et moyenne mobile

## Résultats

| Indicateur | LVMH | NVIDIA |
|---|---|---|
| Rendement annualisé | -8,2 % | +120,7 % |
| Volatilité annualisée | 29,0 % | 48,5 % |
| Performance buy and hold | -40,4 % | +1 379,7 % |
| Maximum drawdown | -58,0 % | -36,9 % |
| Ratio de Sharpe | -0,30 | 1,63 |

**À retenir** : NVIDIA a très bien rémunéré son risque, alors que LVMH a subi une chute de 58 % (24/04/2023 au 02/10/2026) sans retrouver son sommet.

## Limites

- Période de 4 ans seulement, avec un cycle exceptionnel pour NVIDIA (IA).
- Taux sans risque nul et absence de conversion de devises.
- L'annualisation composée d'une moyenne journalière surestime le rendement de NVIDIA (environ 96 % par an en buy and hold).
- Les performances passées ne préjugent pas des performances futures. Ce projet est académique et ne constitue pas un conseil en investissement.

## Auteur

Yannick TCHALLA, MBA 1 Finance & Data Performance, ESLSCA Business School
