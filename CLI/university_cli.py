import pymongo
from pymongo import MongoClient
from bson import ObjectId
from faker import Faker
import random

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['university']

# Collections
faculties_collection = db['faculties']
departments_collection = db['departments']
students_collection = db['students']
teachers_collection = db['teachers']
courses_collection = db['courses']
admin_staff_collection = db['admin_staff']

fake = Faker()

def generate_data():
    faculty_ids = []
    for _ in range(5):
        faculty_data = {
            "name": fake.company(),
            "dean": fake.name(),
            "address": fake.address()
        }
        faculty_ids.append(faculties_collection.insert_one(faculty_data).inserted_id)
    
    department_ids = []
    for _ in range(15):
        department_data = {
            "name": fake.bs(),
            "faculty_id": random.choice(faculty_ids)
        }
        department_ids.append(departments_collection.insert_one(department_data).inserted_id)
    
    for _ in range(2000):
        student_data = {
            "name": fake.name(),
            "age": random.randint(18, 25),
            "gender": random.choice(["Male", "Female"]),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "department_id": random.choice(department_ids)
        }
        students_collection.insert_one(student_data)
    
    for _ in range(20):
        teacher_data = {
            "name": fake.name(),
            "age": random.randint(28, 55),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "department_id": random.choice(department_ids),
            "subject": fake.job()
        }
        teachers_collection.insert_one(teacher_data)
    
    for _ in range(150):
        course_data = {
            "name": fake.catch_phrase(),
            "faculty_id": random.choice(faculty_ids),
            "teacher_id": random.choice(list(teachers_collection.find()))["_id"],
            "semester": random.randint(1, 2),
            "year": random.randint(2010, 2022)
        }
        courses_collection.insert_one(course_data)
    
    for _ in range(10):
        admin_staff_data = {
            "name": fake.name(),
            "role": fake.job(),
            "department": fake.word()
        }
        admin_staff_collection.insert_one(admin_staff_data)
    
    print("Données générées avec succès!")

def add_student():
    nom = input("Nom de l'étudiant: ")
    age = int(input("Âge de l'étudiant: "))
    gender = input("Genre de l'étudiant: ")
    email = input("Email de l'étudiant: ")
    phone = input("Téléphone de l'étudiant: ")
    address = input("Adresse de l'étudiant: ")
    department_id = input("ID du département de l'étudiant: ")

    student = {
        "name": nom,
        "age": age,
        "gender": gender,
        "email": email,
        "phone": phone,
        "address": address,
        "department_id": ObjectId(department_id)
    }

    students_collection.insert_one(student)
    print(f"Étudiant {nom} ajouté avec succès!")

def remove_student():
    student_id = input("ID de l'étudiant à supprimer: ")
    students_collection.delete_one({"_id": ObjectId(student_id)})
    print(f"Étudiant avec l'ID {student_id} supprimé!")

def update_student():
    student_id = input("ID de l'étudiant à modifier: ")
    student = students_collection.find_one({"_id": ObjectId(student_id)})

    if student:
        nom = input(f"Nom actuel: {student['name']}. Nouveau nom ? (Appuyez sur Entrée pour conserver): ") or student['name']
        age = input(f"Âge actuel: {student['age']}. Nouveau âge ? (Appuyez sur Entrée pour conserver): ") or student['age']
        gender = input(f"Genre actuel: {student['gender']}. Nouveau genre ? (Appuyez sur Entrée pour conserver): ") or student['gender']
        email = input(f"Email actuel: {student['email']}. Nouveau email ? (Appuyez sur Entrée pour conserver): ") or student['email']
        phone = input(f"Téléphone actuel: {student['phone']}. Nouveau téléphone ? (Appuyez sur Entrée pour conserver): ") or student['phone']
        address = input(f"Adresse actuelle: {student['address']}. Nouvelle adresse ? (Appuyez sur Entrée pour conserver): ") or student['address']
        department_id = input(f"ID du département actuel: {student['department_id']}. Nouveau ID de département ? (Appuyez sur Entrée pour conserver): ") or student['department_id']

        student_modifie = {
            "name": nom,
            "age": age,
            "gender": gender,
            "email": email,
            "phone": phone,
            "address": address,
            "department_id": ObjectId(department_id)
        }
        students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_modifie})
        print(f"Étudiant avec l'ID {student_id} modifié avec succès!")
    else:
        print(f"Étudiant avec l'ID {student_id} introuvable!")

def list_students():
    for student in students_collection.find():
        print(f"ID: {student['_id']}")
        print(f"Nom: {student['name']}")
        print(f"Âge: {student['age']}")
        print(f"Genre: {student['gender']}")
        print(f"Email: {student['email']}")
        print(f"Téléphone: {student['phone']}")
        print(f"Adresse: {student['address']}")
        print(f"Département ID: {student['department_id']}")
        print("----")

def get_students_per_course():
    pipeline = [
        {"$group": {"_id": "$course_id", "student_count": {"$sum": 1}}}
    ]
    result = students_collection.aggregate(pipeline)
    for entry in result:
        ue = courses_collection.find_one({"_id": entry["_id"]})
        if ue:
            print(f"UE: {ue['name']}, Nombre d'étudiants: {entry['student_count']}")

def add_teacher():
    nom = input("Nom de l'enseignant: ")
    age = int(input("Âge de l'enseignant: "))
    email = input("Email de l'enseignant: ")
    phone = input("Téléphone de l'enseignant: ")
    address = input("Adresse de l'enseignant: ")
    department_id = input("ID du département de l'enseignant: ")
    subject = input("Sujet de l'enseignant: ")

    teacher = {
        "name": nom,
        "age": age,
        "email": email,
        "phone": phone,
        "address": address,
        "department_id": ObjectId(department_id),
        "subject": subject
    }

    teachers_collection.insert_one(teacher)
    print(f"Enseignant {nom} ajouté avec succès!")

def remove_teacher():
    teacher_id = input("ID de l'enseignant à supprimer: ")
    teachers_collection.delete_one({"_id": ObjectId(teacher_id)})
    print(f"Enseignant avec l'ID {teacher_id} supprimé!")

def update_teacher():
    teacher_id = input("ID de l'enseignant à modifier: ")
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})

    if teacher:
        nom = input(f"Nom actuel: {teacher['name']}. Nouveau nom ? (Appuyez sur Entrée pour conserver): ") or teacher['name']
        age = input(f"Âge actuel: {teacher['age']}. Nouveau âge ? (Appuyez sur Entrée pour conserver): ") or teacher['age']
        email = input(f"Email actuel: {teacher['email']}. Nouveau email ? (Appuyez sur Entrée pour conserver): ") or teacher['email']
        phone = input(f"Téléphone actuel: {teacher['phone']}. Nouveau téléphone ? (Appuyez sur Entrée pour conserver): ") or teacher['phone']
        address = input(f"Adresse actuelle: {teacher['address']}. Nouvelle adresse ? (Appuyez sur Entrée pour conserver): ") or teacher['address']
        department_id = input(f"ID du département actuel: {teacher['department_id']}. Nouveau ID de département ? (Appuyez sur Entrée pour conserver): ") or teacher['department_id']
        subject = input(f"Sujet actuel: {teacher['subject']}. Nouveau sujet ? (Appuyez sur Entrée pour conserver): ") or teacher['subject']

        teacher_modifie = {
            "name": nom,
            "age": age,
            "email": email,
            "phone": phone,
            "address": address,
            "department_id": ObjectId(department_id),
            "subject": subject
        }
        teachers_collection.update_one({"_id": ObjectId(teacher_id)}, {"$set": teacher_modifie})
        print(f"Enseignant avec l'ID {teacher_id} modifié avec succès!")
    else:
        print(f"Enseignant avec l'ID {teacher_id} introuvable!")

def list_teachers():
    for teacher in teachers_collection.find():
        print(f"ID: {teacher['_id']}")
        print(f"Nom: {teacher['name']}")
        print(f"Âge: {teacher['age']}")
        print(f"Email: {teacher['email']}")
        print(f"Téléphone: {teacher['phone']}")
        print(f"Adresse: {teacher['address']}")
        print(f"Département ID: {teacher['department_id']}")
        print(f"Sujet: {teacher['subject']}")
        print("----")

def main_menu():
    print("\nGestion des données d'une université")
    print("1. Ajouter un étudiant")
    print("2. Supprimer un étudiant")
    print("3. Modifier un étudiant")
    print("4. Afficher tous les étudiants")
    print("5. Nombre d'étudiants par UE")
    print("6. Ajouter un enseignant")
    print("7. Supprimer un enseignant")
    print("8. Modifier un enseignant")
    print("10. Generer des donnees pour l'université")
    print("11. Quitter")

    choix = input("Entrez votre choix: ")

    if choix == '1':
        add_student()
    elif choix == '2':
        remove_student()
    elif choix == '3':
        update_student()
    elif choix == '4':
        list_students()
    elif choix == '5':
        get_students_per_course()
    elif choix == '6':
        add_teacher()
    elif choix == '7':
        remove_teacher()
    elif choix == '8':
        update_teacher()
    elif choix == '9':
        list_teachers()
    elif choix == '10':
        generate_data
    elif choix == '11':
        print("Au revoir!")
        return False
    else:
        print("Choix invalide. Veuillez réessayer.")
    
    return True

if __name__ == "__main__":
    generate_data()
    while True:
        if not main_menu():
            break
