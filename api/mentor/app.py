from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import faiss
import numpy as np
import logging
from sentence_transformers import SentenceTransformer

# Configure Flask App
app = Flask(__name__)
# Allow CORS only for the frontend origin
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "PlsWork@1234",
    "database": "mentors_testing"
}

# Load Sentence Transformer Model
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# FAISS Index Setup
D = 384  # Dimension of embeddings
faiss_index = faiss.IndexFlatL2(D)
mentor_data = []  # Store mentor details for ID mapping

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to generate embeddings
def get_embedding(text):
    return np.expand_dims(embedding_model.encode(text).astype(np.float32), axis=0)

# API to Register Mentor
@app.route("/register_mentor", methods=["POST"])
def register_mentor():
    data = request.json
    required_fields = ["name", "email", "phone", "calendly", "expertise", "experience", "age", "bio"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Insert mentor details into database
        with get_db_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO mentors (name, email, phone, calendly, expertise, experience, age, bio)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (data["name"], data["email"], data["phone"], data["calendly"],
                     data["expertise"], data["experience"], data["age"], data["bio"])
                )
                db.commit()

        # Generate embedding and store it in FAISS
        text = f"{data['expertise']} {data['experience']} years experience {data['age']} {data['bio']}"
        embedding = get_embedding(text)
        faiss_index.add(embedding)

        # Store metadata for mentor retrieval
        mentor_data.append((data["name"], data["expertise"], data["bio"], data["email"], data["phone"], data["calendly"]))

        logging.info(f"Mentor {data['name']} registered successfully.")
        return jsonify({"message": "Mentor registered successfully!"}), 201

    except mysql.connector.Error as err:
        logging.error(f"Database Error: {err}")
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# API to Search Mentors
@app.route("/search_mentor", methods=["POST"])
def search_mentor():
    query = request.json.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    if len(mentor_data) == 0:
        return jsonify({"error": "No mentors available"}), 404

    try:
        query_embedding = get_embedding(query)
        _, indices = faiss_index.search(query_embedding, min(3, len(mentor_data)))

        results = [
            {
                "name": mentor_data[idx][0],
                "expertise": mentor_data[idx][1],
                "bio": mentor_data[idx][2],
                "email": mentor_data[idx][3],
                "phone": mentor_data[idx][4],
                "calendly": mentor_data[idx][5]
            }
            for idx in indices[0] if idx < len(mentor_data)
        ]

        return jsonify({"mentors": results})

    except Exception as e:
        logging.error(f"Error in mentor search: {e}")
        return jsonify({"error": "An error occurred while searching"}), 500

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)