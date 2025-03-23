from flask import Flask, request, jsonify
import mysql.connector
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PlsWork@1234",
    database="mentors_testing"
)
cursor = db.cursor()

# Load multilingual embedding model
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# FAISS Index Setup
D = 384  # Dimension of embedding model output
faiss_index = faiss.IndexFlatL2(D)
mentor_data = []  # Store mentor details for ID mapping

# Function to generate embeddings
def get_embedding(text):
    return np.array(embedding_model.encode(text), dtype=np.float32)

# API to register mentor
@app.route("/register_mentor", methods=["POST"])
def register_mentor():
    data = request.json
    name, email, phone, calendly, expertise, exp, age, bio = (
        data["name"], data["email"], data["phone"], data["calendly"],
        data["expertise"], data["experience"], data["age"], data["bio"]
    )

    # Insert into MySQL
    cursor.execute("""
        INSERT INTO mentors (name, email, phone, calendly, expertise, experience, age, bio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, email, phone, calendly, expertise, exp, age, bio))
    db.commit()

    # Generate embedding
    text = f"{expertise} {exp} years experience {age} {bio}"
    embedding = get_embedding(text)

    # Store in FAISS
    faiss_index.add(np.array([embedding]))
    mentor_data.append((name, expertise, bio, email, phone, calendly))

    return jsonify({"message": "Mentor registered successfully!"})

# API to search mentors
@app.route("/search_mentor", methods=["POST"])
def search_mentor():
    query = request.json["query"]
    query_embedding = get_embedding(query)

    # Perform similarity search
    _, indices = faiss_index.search(np.array([query_embedding]), 3)
    
    results = []
    for idx in indices[0]:
        if idx < len(mentor_data):
            results.append({
                "name": mentor_data[idx][0],
                "expertise": mentor_data[idx][1],
                "bio": mentor_data[idx][2],
                "email": mentor_data[idx][3],
                "phone": mentor_data[idx][4],
                "calendly": mentor_data[idx][5]
            })

    return jsonify({"mentors": results})

if __name__ == "__main__":
    app.run(debug=True)

