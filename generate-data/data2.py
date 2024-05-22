from pymongo import MongoClient
from faker import Faker
import random

# Se connecter à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['university']  # Nom de la base de données
faculties_collection = db['faculties']  # Collection pour les facultés
students_collection = db['students']    # Collection pour les étudiants
teachers_collection = db['teachers']    # Collection pour les enseignants
ues_collection = db['ues']              # Collection pour les unités d'enseignement


# Liste de noms de facultés réels
faculty_names = [
    "Faculté des sciences",
    "Faculté de médecine",
    "Faculté des arts",
    "Faculté de droit",
    "Faculté de génie",
    # Ajoutez d'autres noms de facultés au besoin
]

fake = Faker()

# Fonction pour générer des données pour une faculté
def generate_faculty():
    return {
        'name': random.choice(faculty_names),
        'dean': fake.name(),
        'address': fake.address()
    }

# Fonction pour générer des données pour un étudiant
def generate_student(faculty_id):
    return {
        'name': fake.name(),
        'age': random.randint(18, 25),
        'gender': random.choice(['Male', 'Female']),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'faculty_id': faculty_id
    }

# Fonction pour générer des données pour un enseignant
def generate_teacher(faculty_id):
    return {
        'name': fake.name(),
        'age': random.randint(28, 55),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'faculty_id': faculty_id,
        'subject': fake.job()
    }

# Fonction pour générer des données pour une unité d'enseignement
def generate_ue(faculty_id):
    return {
        'name': fake.catch_phrase(),
        'faculty_id': faculty_id,
        'teacher': fake.name(),
        'semester': random.randint(1, 2),
        'year': random.randint(2010, 2022)
    }

# Générer et insérer des données dans la base de données
def generate_data():
    # Générer des données pour les facultés
    for _ in range(5):
        faculty_data = generate_faculty()
        faculty_id = faculties_collection.insert_one(faculty_data).inserted_id

        # Générer des données pour les étudiants de cette faculté
        for _ in range(1000):
            student_data = generate_student(faculty_id)
            students_collection.insert_one(student_data)

        # Générer des données pour les enseignants de cette faculté
        for _ in range(20):
            teacher_data = generate_teacher(faculty_id)
            teachers_collection.insert_one(teacher_data)

        # Générer des données pour les unités d'enseignement de cette faculté
        for _ in range(50):
            ue_data = generate_ue(faculty_id)
            ues_collection.insert_one(ue_data)

# Appeler la fonction pour générer les données
generate_data()
