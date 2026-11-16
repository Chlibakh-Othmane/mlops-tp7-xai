# Model Card - fraude (version servie par l'alias production)

## Modèle
Nom et version dans le registre MLflow : `fraude-tp2`, version 1, alias `production`.
Famille et réglages : forêt aléatoire (`RandomForestClassifier`), 500 arbres, profondeur maximale 16, `random_state=42`.
Run d'origine (MLflow) : `8bf57bb0` (run qui a produit la version 1 du modèle, TP2).

## Objectif et usage prévu
Détecter les transactions bancaires potentiellement frauduleuses (classe 1 = fraude) à partir de quatre variables connues au moment du paiement : `montant` (MAD), `anciennete` (mois), `freq_24h` (transactions sur 24 h), `nuit` (paiement entre 0 h et 5 h).
Le modèle sert d'aide à la décision : il déclenche une alerte ou un blocage préventif, qu'un conseiller peut lever après vérification auprès du client.

## Usages exclus
Ne pas bloquer définitivement un compte ni rejeter un paiement sans revue humaine : sur le test, 15 clients honnêtes sont bloqués à tort et 20 fraudes sur 134 passent (matrice [[1101, 15], [20, 114]]).
Ne pas utiliser le modèle sur des données réelles sans nouvelle évaluation, ni pour d'autres populations, d'autres monnaies ou d'autres canaux de paiement que ceux des données d'entraînement.

## Données
Fichier `data/transactions.csv`, 5 000 lignes, 568 fraudes (11,4 %), empreinte md5 (tag `donnees_md5` du run d'explications) : `[À COMPLÉTER : copier la valeur du tag dans MLflow]`.
Origine : données **synthétiques**, générées par une formule à graine fixe (annexe A du TP) ; aucune transaction réelle.

## Performances (jeu de test, 1 250 transactions)
F1 : 0,8669    précision : 0,8837    rappel : 0,8507    AUC : 0,9872
(valeurs de référence de l'énoncé ; à vérifier sur votre sortie de `verifier_modele.py`).
Matrice de confusion : 1101 vrais négatifs, 15 fausses alertes, 20 fraudes manquées, 114 fraudes détectées (114 / 134).

## Méthodes d'explicabilité
Globale : importance par permutation (perte de F1, 10 répétitions) comparée à la MDI de la forêt ; SHAP global (`TreeExplainer`, 400 transactions de test, moyenne des valeurs absolues).
Locale : SHAP (waterfall) pour cette cliente et pour la transaction de test 668 ; LIME (2 000 voisins, graine 0) comparé sur 5 graines. Pour Mme Benali (1 800 MAD, de nuit, P(fraude) = 0,924) : `nuit` +0,370, `montant` +0,367, `anciennete` +0,090, `freq_24h` −0,018 ; base + somme = prédiction.
Variables les plus influentes : `montant` en tête (permutation ≈ 0,59 ; SHAP ≈ 0,116), suivi de `anciennete`, `nuit` et `freq_24h`, dont l'ordre varie selon la méthode (importances SHAP presque égales, 0,056 à 0,058). Effet du montant positif à partir d'environ 1 000 MAD ; une longue ancienneté réduit le risque.

## Comparaison avec un modèle interprétable
La régression logistique avec log10(montant) obtient F1 = 0,8593 (113 / 134 fraudes) contre 0,8669 (114 / 134) pour la forêt : écart d'une seule fraude, dans le bruit du jeu de test. Avec le montant brut, F1 = 0,7407. Un arbre de profondeur 3 (8 feuilles, entièrement lisible) n'atteint que F1 = 0,5737 (72 / 134) ; l'arbre sans limite (206 feuilles) 0,7556.

## Limites et risques connus
Données synthétiques construites à partir d'un score presque linéaire en log10(montant) : les performances et les explications ne prouvent rien sur des fraudes réelles ; cas rares non couverts.
LIME est instable pour les variables à effet faible (`anciennete`, `freq_24h` changent de signe selon la graine) ; SHAP décrit comment le modèle utilise une variable, pas la cause réelle de la fraude. Les effets de `montant` et de `nuit` sont à surveiller dans le temps.

## Recommandations d'utilisation et de surveillance
Maintenir une revue humaine avant tout blocage durable ; suivre le taux de fausses alertes et le rappel après chaque réentraînement.
Relancer les explications (SHAP, vérification de stabilité) et mettre à jour cette carte à chaque réentraînement ou changement d'alias `production`. La logistique avec log10(montant) est une alternative lisible à envisager (écart de performance non significatif).
Limite d'audit : le TP n'enregistre pas le journal de chaque décision (entrées, date, version servie, seuil).

## Traçabilité
Run des explications (expérience `tp7-explicabilite`) : `xai-fraude-v1`, run `6ca645d3`, relié à la version 1 du modèle par le tag `explications_run`.
Auteurs : Othmane Chlibakh, Sara Nabil    Date : 16 novembre 2026    Prochaine revue : à chaque réentraînement ou changement d'alias, et au plus tard dans 6 mois (proposition).
Dépôts GitHub : https://github.com/Chlibakh-Othmane/mlops-tp7-xai, https://github.com/Sara200409/mlops-tp7-xai
