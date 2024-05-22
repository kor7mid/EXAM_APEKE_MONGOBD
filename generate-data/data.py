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

fake = Faker()

# Fonction pour générer des données pour une faculté
def generate_faculty():
    return {
        'name': fake.company(),
        'dean': fake.name(),
        'address': fake.address()
    }

# Fonction pour générer des données pour un étudiant
def generate_student():
    return {
        'name': fake.name(),
        'age': random.randint(18, 25),
        'faculty': random.choice(['Engineering', 'Medicine', 'Arts', 'Science', 'Business']),
        'year': random.randint(1, 5)
    }

# Fonction pour générer des données pour un enseignant
def generate_teacher():
    return {
        'name': fake.name(),
        'faculty': random.choice(['Engineering', 'Medicine', 'Arts', 'Science', 'Business']),
        'subject': fake.job()
    }

# Fonction pour générer des données pour une unité d'enseignement
def generate_ue():
    return {
        'name': fake.catch_phrase(),
        'faculty': random.choice(['Engineering', 'Medicine', 'Arts', 'Science', 'Business']),
        'teacher': fake.name(),
        'semester': random.randint(1, 2),
        'year': random.randint(2010, 2022)
    }

# Générer et insérer des données dans la base de données
def generate_data():
    # Générer des données pour les facultés
    for _ in range(5):
        faculty_data = generate_faculty()
        faculties_collection.insert_one(faculty_data)

    # Générer des données pour les étudiants
    for _ in range(100000):
        student_data = generate_student()
        students_collection.insert_one(student_data)

    # Générer des données pour les enseignants
    for _ in range(200):
        teacher_data = generate_teacher()
        teachers_collection.insert_one(teacher_data)

    # Générer des données pour les unités d'enseignement
    for _ in range(500):
        ue_data = generate_ue()
        ues_collection.insert_one(ue_data)

# Appeler la fonction pour générer les données
generate_data()
