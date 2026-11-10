import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from sklearn.model_selection import train_test_split

# 1. Connexion au serveur MLflow actif
mlflow.set_tracking_uri("http://127.0.0.1:5001")

# 2. Définition des constantes (avec le nom exact "fraude-tp2")
NOM, ALIAS = "fraude-tp2", "production"

# 3. Récupération de la version et du modèle enregistré
VERSION = MlflowClient().get_model_version_by_alias(NOM, ALIAS)
m = mlflow.sklearn.load_model(f"models:/{NOM}@{ALIAS}")

# 4. Chargement des données et découpage (identique au TP2)
df = pd.read_csv("data/transactions.csv")
X, y = df.drop(columns="fraude"), df["fraude"]
Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 5. Cas test spécifique (ex: Mme Benali)
CAS = pd.DataFrame([{
    "montant": 1800.0,
    "anciennete": 30,
    "freq_24h": 4,
    "nuit": 1,
}])