from pymongo import MongoClient
from faker import Faker
import random

# Se connecter à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['university']  # Nom de la base de données
faculties_collection = db['faculties']  
students_collection = db['students']    
teachers_collection = db['teachers']   
ues_collection = db['ues']             
admin_staff_collection = db['admin_staff'] 
sports_collection = db['sports'] 

# Liste de noms de facultés réels
faculty_names = [
    "Faculté des sciences",
    "Faculté de médecine",
    "Faculté des arts",
    "Faculté de droit",
    "Faculté de génie",
]

fake = Faker()

#  générer des données pour une faculté
def generate_faculty():
    return {
        'name': random.choice(faculty_names),
        'dean': fake.name(),
        'address': fake.address()
    }

#  générer des données pour un étudiant
def generate_student(faculty_id):
    return {
        'name': fake.name(),
        'age': random.randint(18, 25),
        'gender': random.choice(['Male', 'Female']),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'faculty_id': faculty_id,
        'sport': random.choice(['Football', 'Basketball', 'Volleyball', 'Swimming'])
    }

# générer des données pour un enseignant
def generate_teacher():
    return {
        'name': fake.name(),
        'age': random.randint(28, 55),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'faculty': random.choice(faculty_names),
        'subject': fake.job()
    }

# générer des données pour une unité d'enseignement
def generate_ue():
    return {
        'name': fake.catch_phrase(),
        'faculty': random.choice(faculty_names),
        'teacher': fake.name(),
        'semester': random.randint(1, 2),
        'year': random.randint(2010, 2022)
    }

# générer des données pour le personnel administratif
def generate_admin_staff():
    return {
        'name': fake.name(),
        'role': fake.job(),
        'department': random.choice(['HR', 'Finance', 'IT', 'Administration'])
    }

# générer des données pour les sports
def generate_sport():
    return {
        'name': random.choice(['Football', 'Basketball', 'Volleyball', 'Swimming']),
        'coach': fake.name(),
        'location': fake.address()
    }

# Générer et insérer des données dans la base de données
def generate_data():
    # Générer des données pour les facultés
    faculty_ids = []
    for _ in range(5):
        faculty_data = generate_faculty()
        faculty_ids.append(faculties_collection.insert_one(faculty_data).inserted_id)

    # Générer des données pour les étudiants
    for _ in range(2000):
        student_data = generate_student(random.choice(faculty_ids))
        students_collection.insert_one(student_data)

    # Générer des données pour les enseignants
    for _ in range(20):
        teacher_data = generate_teacher()
        teachers_collection.insert_one(teacher_data)

    # Générer des données pour les unités d'enseignement
    for _ in range(150):
        ue_data = generate_ue()
        ues_collection.insert_one(ue_data)

    # Générer des données pour le personnel administratif
    for _ in range(10):
        admin_staff_data = generate_admin_staff()
        admin_staff_collection.insert_one(admin_staff_data)

    # Générer des données pour les sports
    for _ in range(4):
        sport_data = generate_sport()
        sports_collection.insert_one(sport_data)

# Appeler la fonction pour générer les données
generate_data()
