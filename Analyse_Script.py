"""
-Actifs : LVMH (MC.PA, EUR) et NVIDIA (NVDA, USD), analysés séparément en monnaie locale
-Période : 28/10/2022 -> 30/10/2026 (données journalières)
-Source des données : historiques Excel téléchargés sur Investing.com, dans le même dossier que ce script
-Les Graphiques de chaque actif sont exportés dans ce dossier en png à l'execution du script
-Auteurs : M. YANNICK TCHALLA , M. FRANCKY BOUTING , M. YOHANN NINDJIN , M. CHRISTOPHE NINDJIN 

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#on remet donc l'ordre chronologique. Les dates servent d'index, puis on garde le prix de clôture.
def reset_index(df):
    df = df.iloc[::-1].reset_index(drop=True)  # Du plus ancien au plus récent
    return df["Dernier"]  # Prix de clôture

# Rendement simple jour par jour avec pct_change()
def rendement_journalier(prix):
    return prix.pct_change().dropna()  

def rendement_moyen(rend):
    moy = rend.mean()  # Rendement journalier moyen
    annuel = (1 + moy)**252 - 1  # Annualisation en intérêts composés (252 séances)
    return moy, annuel

#std() : Retourne l'écart type de la série de rendement : c'est le risque journalier.
def volatilite(rend):
    v = rend.std()  
    return v, v * np.sqrt(252)  # Annualisation par racine de 252

# Performance cumulative : acheter et conserver de la première à la dernière séance
def performance_cumulee(prix):
    return prix.iloc[-1] / prix.iloc[0] - 1  

# Lisse le bruit pour lire la tendance
def moyenne_mobile(prix, n=20):
    return prix.rolling(n).mean()  

#Calcul du drawdown: perte maximale qu'aurait subie un investisseur entre un sommet et un creux
# Similaire à la mesure centrale du risque de perte en gestion de portefeuille (~VaR)
def maximum_drawdown(rend):
    cumul = (1 + rend).cumprod()  # Courbe du capital cumulé
    drawdown = cumul / cumul.cummax() - 1  # Perte depuis le dernier sommet
    return drawdown.min()  # Pire perte sommet -> creux

#Le ratio de Sharpe mesure le rendement obtenu par unité de risque
def ratio_sharpe(rend, taux_sans_risque=0.0):
    exces = rend.mean() - taux_sans_risque / 252  # Rendement excédentaire journalier
    return (exces / rend.std()) * np.sqrt(252)  # Annualisé

def graphique(prix, mm, nom, devise):
    plt.figure(figsize=(9, 4.2))
    plt.plot(prix.index, prix.values, label="Prix journalier")
    plt.plot(mm.index, mm.values, label="Moyenne mobile sur 20 séances")
    plt.title(f"{nom} : prix et moyenne mobile 20 séances")
    plt.xlabel("Numéro de séance")
    plt.ylabel(f"Prix ({devise})")
    plt.legend(); plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"graphique_{nom}.png", dpi=150)  # Export pour le livrable
    plt.show()

# Un fichier par actif : (nom = nom de la feuille Excel, fichier, devise)
actifs = [("LVMH", "LVMH_oct_2022_2026.xlsx", "EUR"),
          ("NVDA", "NVDA_oct_2022_2026.xlsx", "USD")]
#print("=========1-Importation des données=========")
for nom, fichier, devise in actifs:
    print(f"\n=========== {nom} ===========")
    df = pd.read_excel(fichier, sheet_name=nom)
    df.columns = df.columns.str.strip() 
    print(df.columns)

    print(f"======== svvvvvv s=2-Statistiques de la série de prix {nom} =========")
    prix = reset_index(df)
    print("Nombre de séances : ", len(prix))
    print(prix.describe().round(2))

    print(f"=========3-Rendement journalier {nom} =========")
    rend = rendement_journalier(prix)
    print((rend.head(5) * 100).round(2))

    print("=========4-Rendement moyen et annualisé {nom} =========")
    m, ann = rendement_moyen(rend)
    print("Journalier moyen : ", round(m * 100, 4), "%")
    print("Annualisé : ", round(ann * 100, 2), "%")

    print(f"=========5-Volatilité journalière et annualisée {nom} =========")
    vj, va = volatilite(rend)
    print("Volatilité journalière : ", round(vj * 100, 3), "%")
    print("Volatilité annualisée : ", round(va * 100, 2), "%")

    print(f"=========6-Performance de l'action sur la période {nom} =========")
    perf = performance_cumulee(prix)
    print("Performance totale : ", round(perf * 100, 2), "%")

    print("=========7-Moyenne mobile sur 20 jours {nom} =========")
    mm = moyenne_mobile(prix, 20)
    print(mm.dropna().tail(4).round(2))

    print(f"=========8-Maximum drawdown {nom} =========")
    mdd = maximum_drawdown(rend)
    print("Maximum drawdown : ", round(mdd * 100, 2), "%")

    print(f"=========9-Ratio de Sharpe {nom}  =========")
    sharpe = ratio_sharpe(rend)
    print("Ratio de Sharpe : ", round(sharpe, 3))

    print(f"=========10-Visualisation {nom} =========")
    graphique(prix, mm, nom, devise)
    print("Analyse complète et terminée!")