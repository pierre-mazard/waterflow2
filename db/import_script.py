import psycopg2
import csv
import os
from datetime import datetime

# Chargement des variables d'environnement
DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/waterflow2")

CSV_PATH = "data/water_potability.csv"

def connect_db():
    try:
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        return conn
    except Exception as e:
        print("❌ Erreur de connexion à la base :", e)
        exit(1)

def create_test_client(conn):
    """
    Crée un client de test si aucun n'existe.
    """
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM clients;")
    count = cur.fetchone()[0]

    if count == 0:
        print("➡ Aucun client trouvé : création d'un client de test...")
        cur.execute("""
            INSERT INTO clients (code_client, nom_structure, adresse_postale, api_key)
            VALUES ('CLIENT-TEST', 'Structure Test', 'Adresse Test', 'TEST-API-KEY');
        """)
        print("✔ Client de test créé.")
    else:
        print("✔ Client déjà présent, OK.")

def import_measurements(conn):
    """
    Importe les mesures depuis le CSV dans la table measurements.
    """
    cur = conn.cursor()

    print(f"➡ Import du fichier CSV : {CSV_PATH}")

    try:
        with open(CSV_PATH, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                cur.execute("""
                    INSERT INTO measurements (
                        id_client,
                        date_prelevement,
                        lieu_prelevement,
                        ph,
                        hardness,
                        solids,
                        chloramines,
                        sulfate,
                        conductivity,
                        organic_carbon,
                        trihalomethanes,
                        turbidity,
                        provenance,
                        prediction,
                        prediction_model_version
                    )
                    VALUES (
                        1,
                        %s,
                        %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        'Saisie',
                        NULL,
                        NULL
                    );
                """, (
                    datetime.now(),
                    "Import CSV",
                    row["ph"],
                    row["Hardness"],
                    row["Solids"],
                    row["Chloramines"],
                    row["Sulfate"],
                    row["Conductivity"],
                    row["Organic_carbon"],
                    row["Trihalomethanes"],
                    row["Turbidity"]
                ))

        print("✔ Import terminé avec succès.")

    except Exception as e:
        print("❌ Erreur lors de l'import :", e)

def main():
    print("🚀 Script d'import Waterflow 2")
    conn = connect_db()
    create_test_client(conn)
    import_measurements(conn)
    conn.close()
    print("🎉 Import terminé.")

if __name__ == "__main__":
    main()
