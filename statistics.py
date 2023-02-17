#In[]
import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from matplotlib import style
from time import process_time

startTime = process_time()

# Ausreißer
from statsmodels import robust

# Datensatz generieren
data = pd.read_excel("Datensatz.xlsx")
G1 = data["Gruppe_1/Zeitpunkt_1"]; G2 = data["Gruppe_2/Zeitpunkt_2"]; G3 = data["Gruppe_3/Zeitpunkt_3"]
automatic_Groupsize = data.shape[1]
alpha = 0.05
independence = 2 # 1 = verbunden/abhängig, 2 = unverbunden/unabhängig
number_Groups = 3 # Anzahl der Gruppen

# Überprüfung der Normalverteilung
from scipy.stats import shapiro
from scipy.stats import kstest
sampleSize = min(len(G1),len(G2),len(G3)) # Größer der Stichprobe ermitteln von allen eingelesenen Daten der Gruppen/Zeitpunkte
resultNV = []
if number_Groups == 2:
    def normalverteilungSW(x,y):
        shapiroTest = [shapiro(x), shapiro(y)]
        resultNV.append(shapiroTest)
        return resultNV
    def normalverteilungKS(x,y):
        ksTest = [kstest(x, 'norm'), kstest(y, 'norm')]
        resultNV.append(ksTest)
        return resultNV
    if sampleSize < 20:
        resultNV.append(normalverteilungSW(G1, G2))
    if sampleSize > 20:
        resultNV.append(normalverteilungKS(G1, G2))
if number_Groups > 2:
    def normalverteilungSW(x, y, z):
        shapiroTest = [shapiro(x), shapiro(y), shapiro(z)]
        resultNV.append(shapiroTest)
        return resultNV
    def normalverteilungKS(x, y, z):
        ksTest = [kstest(x, 'norm'), kstest(y, 'norm'), kstest(z, 'norm')]
        resultNV.append(ksTest)
        return resultNV
    if sampleSize < 20:
        resultNV.append(normalverteilungSW(G1, G2, G3))
    if sampleSize > 20:
        resultNV.append(normalverteilungKS(G1, G2, G3))

# Unterschiedsprüfung für verbundene/abhängigen Stichproben
if independence == 1 and number_Groups == 2:
    if (resultNV[0][0][1] > 0.5) and (resultNV[1][0][1][1] > 0.5):
        # Normalverteilung geg.: Durchführung t-Test
        from scipy.stats import ttest_rel
        t_Test_rel_result = []
        def tTestRel(x, y):
            stat, p = ttest_rel(x, y)
            t_Test_rel_result.append(stat)
            t_Test_rel_result.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result tTestRel: Same distribution (accept H0)')
            else:
                print('Result tTestRel: Different distribution (reject H0)')
        tTestRel(G1, G2)

    if (resultNV[0][0][1] < 0.5) or (resultNV[1][0][1][1] < 0.5):
        # Normalverteilung nicht geg.: Durchführung Wilcoxon-Signed-Test
        from scipy.stats import wilcoxon
        wilcoxon_Test_result = []
        def wilcoxonSRang(x, y):
            stat, p = wilcoxon(x, y)
            wilcoxon_Test_result.append(stat)
            wilcoxon_Test_result.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result: Wilcoxon Signed Rang: Same distribution (accept H0)')
            else:
                print('Result: Wilcoxon Signed Rang: Different distribution (reject H0)')
        wilcoxonSRang(G1,G2)

# Unterschiedsprüfung für unverbundene/unabhängigen Stichproben
if (independence == 2) and (number_Groups == 2):
    if (resultNV[0][0][1] > 0.5) and (resultNV[1][0][1][1] > 0.5):
        # Normalverteilung geg.: Durchführung t-Test
        from scipy.stats import ttest_ind
        t_Test_ind_result = []
        def tTestInd(x, y):
            stat, p = ttest_ind(x, y)
            t_Test_ind_result.append(stat)
            t_Test_ind_result.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result tTest_ind: Same distribution (accept H0)')
            else:
                print('Result tTestRel_ind: Different distribution (reject H0)')
        tTestInd(G1, G2)

    if (resultNV[0][0][1] < 0.5) or (resultNV[1][0][1][1] < 0.5):
        # Normalverteilung nicht geg.: Durchführung Wilcoxon-Signed-Test
        from scipy.stats import mannwhitneyu
        mannWhitneyU_result = []
        def mannWhitneyU(x, y):
            stat, p = mannwhitneyu(x, y)
            mannWhitneyU_result.append(stat)
            mannWhitneyU_result.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result MannWhitneyU Test: Same distribution (accept H0)')
            else:
                print('Result MannWhitneyU Test: Different distribution (reject H0)')
        mannWhitneyU(G1,G2)

# Unterschiedsprüfung für mehr als 2 Gruppen (verbundene/abhängige Stichproben)
if (independence == 1) and (number_Groups >= 3):
    if (resultNV[0][0][1] > 0.5) and (resultNV[1][0][1][1] > 0.5) and (resultNV[1][0][2][1] > 0.5):
        # Normalverteilung geg.: Durchführung ANOVA mit Messwiederholung
        pass
    if (resultNV[0][0][1] < 0.5) or (resultNV[1][0][1][1] < 0.5) or (resultNV[1][0][2][1] < 0.5):
        # Normalverteilung nicht geg.: Friedman-Test
        from scipy.stats import friedmanchisquare
        friedman_Test_result = []
        def friedmanTest(x, y, z):
            stat, p = friedmanchisquare(x, y, z)
            friedman_Test_result.append(stat); friedman_Test_result.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat, p))
            if p > alpha:
                print('Result: Friedman Test: Same distributions (accept H0)')
            else:
                print('Result: Friedman Test: Different distributions (reject H0)') 

# Unterschiedsprüfung für mehr als 2 Gruppen (unverbundene/unabhängige Stichproben)
if (independence == 2) and (number_Groups >= 3):
    if (resultNV[0][0][1] > 0.5) and (resultNV[1][0][1][1] > 0.5) and (resultNV[1][0][2][1] > 0.5):
        # Normalverteilung geg.: Durchführung ANOVA für unabhängige Stichproben
        from scipy.stats import f_oneway
        oneFacANOVA_ind = []
        def fANOVAoneFac(x, y, z):
            stat, p = f_oneway(x, y, z)
            oneFacANOVA_ind.append(stat)
            oneFacANOVA_ind.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result: Einfaktorielle ANOVA: Same distribution (accept H0)')
            else:
                print('Result: Einfaktorielle ANOVA: Different distribution (reject H0)')
        fANOVAoneFac(G1,G2,G3)        
        
    if (resultNV[0][0][1] < 0.5) or (resultNV[1][0][1][1] < 0.5) or (resultNV[1][0][2][1] < 0.5):
        # Normalverteilung nicht geg.: Kruskal-Wallis Test
        from scipy.stats import kruskal
        kruskalWallis_results = []
        def kruskalWallis(x, y, z):
            stat, p = kruskal(x, y, z)
            kruskalWallis_results.append(stat)
            kruskalWallis_results.append(p)
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            if p > alpha:
                print('Result: Kruskal Wallis: Same distributions (accept H0)')
            else:
                print('Result: Kruskal Wallis: Different distributions (reject H0)') 
        kruskalWallis(G1, G2, G3)

endTime = process_time()
calcTime = endTime-startTime
print("Time of Calculation: {:.3f}".format(calcTime))
# %%
