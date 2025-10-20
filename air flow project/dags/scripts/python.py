import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix , accuracy_score
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import pickle

DB_USER = "postgres" 
DB_PASS = "123456"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres_db"
SCHEMA = "public"
TABLE = "int_churn_features_encoded"

db_connection_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_connection_str)

table_name = f"{SCHEMA}.{TABLE}"

sql_query = f"SELECT * FROM {table_name};"

print("🚀 Loading data from data warehouse...")
try:
    df = pd.read_sql(sql_query, engine)
    print("✅ Data loaded successfully!")
    print("\nFirst 5 rows of the data:")
    print(df.head())
    print(f"\nDataFrame has {df.shape[0]} rows and {df.shape[1]} columns.")
    #print(df.isnull().sum())
    x = df.drop(columns=['churn_label'])
    y = df['churn_label']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    smote = SMOTE(random_state=42)
    x_train, y_train = smote.fit_resample(x_train, y_train)
    models = {
        "RandomForest": RandomForestClassifier(),
        "XGBoost": XGBClassifier(),
        "DecisionTree": DecisionTreeClassifier(),
        "LogisticRegression": LogisticRegression()
    }
    accuracy_dict = {}
    for model_name, model in models.items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        print(f"\nModel: {model_name}")
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        (print(f"Accuracy: {accuracy_score(y_test, y_pred)}"))
        accuracy_dict[model_name] = accuracy_score(y_test, y_pred)
    best_model = max(accuracy_dict, key=accuracy_dict.get)
    print(f"\n🏆 Best Model: {best_model} with Accuracy: {accuracy_dict[best_model]}")
    with open('best_model.pkl', 'wb') as f:
        pickle.dump(models[best_model], f)
    plt.bar(accuracy_dict.keys(), accuracy_dict.values())
    plt.xticks(rotation=45)
    plt.ylabel("Accuracy")
    plt.title("Model Comparison")
    plt.show()
except Exception as e:
    print(f"❌ Error loading data: {e}")


