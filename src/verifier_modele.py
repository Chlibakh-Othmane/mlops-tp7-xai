from xai_commun import VERSION, m, Xte, yte, CAS
from mlflow import MlflowClient

# 1. Récupération du run associé pour afficher les infos
client = MlflowClient()
run = client.get_run(VERSION.run_id)

print(f"modèle     : fraude-tp2, version {VERSION.version} | run {VERSION.run_id[:8]}")

# 2. Affichage sécurisé des paramètres (évite le KeyError si les clés diffèrent)
try:
    params = {k: run.data.params[k] for k in ['n_estimators', 'max_depth'] if k in run.data.params}
    print("Paramètres principaux :", params)
except Exception:
    print("Paramètres complets :", run.data.params)

# 3. Test de prédiction sur le cas (ex: Mme Benali)
prediction = m.predict(CAS)
proba = m.predict_proba(CAS) if hasattr(m, "predict_proba") else None

print("\n--- Test sur le cas (Mme Benali) ---")
print("Prédiction (0 = Non fraude, 1 = Fraude) :", prediction[0])
if proba is not None:
    print("Probabilités :", proba[0])