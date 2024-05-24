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
    count = 0
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
        count += 1
        print(f"Total des étudiants: {count}")

def list_students_by_department():
    department_id = input("ID du département: ")
    for student in students_collection.find({"department_id": ObjectId(department_id)}):
        print(f"ID: {student['_id']}")
        print(f"Nom: {student['name']}")
        print(f"Âge: {student['age']}")
        print(f"Genre: {student['gender']}")
        print(f"Email: {student['email']}")
        print(f"Téléphone: {student['phone']}")
        print(f"Adresse: {student['address']}")
        print(f"Département ID: {student['department_id']}")
        print("----")
        count += 1
        print(f"Total des étudiants du departement: {count}")

def list_students_by_faculty():
    count = 0
    faculty_id = input("ID de la faculté: ")
    department_ids = [department['_id'] for department in departments_collection.find({"faculty_id": ObjectId(faculty_id)})]
    for student in students_collection.find({"department_id": {"$in": department_ids}}):
        print(f"ID: {student['_id']}")
        print(f"Nom: {student['name']}")
        print(f"Âge: {student['age']}")
        print(f"Genre: {student['gender']}")
        print(f"Email: {student['email']}")
        print(f"Téléphone: {student['phone']}")
        print(f"Adresse: {student['address']}")
        print(f"Département ID: {student['department_id']}")
        print("----")
        count += 1
        print(f"Total des étudiants de cette faculte: {count}")

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
    count = 0
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
        count += 1
        print(f"Total des enseignants: {count}")

def list_teachers_by_department():
    count = 0
    department_id = input("ID du département: ")
    for teacher in teachers_collection.find({"department_id": ObjectId(department_id)}):
        print(f"ID: {teacher['_id']}")
        print(f"Nom: {teacher['name']}")
        print(f"Âge: {teacher['age']}")
        print(f"Email: {teacher['email']}")
        print(f"Téléphone: {teacher['phone']}")
        print(f"Adresse: {teacher['address']}")
        print(f"Département ID: {teacher['department_id']}")
        print(f"Sujet: {teacher['subject']}")
        print("----")
        count += 1
        print(f"Total des enseignats du departement: {count}")

def list_teachers_by_faculty():
    count = 0
    faculty_id = input("ID de la faculté: ")
    department_ids = [department['_id'] for department in departments_collection.find({"faculty_id": ObjectId(faculty_id)})]
    for teacher in teachers_collection.find({"department_id": {"$in": department_ids}}):
        print(f"ID: {teacher['_id']}")
        print(f"Nom: {teacher['name']}")
        print(f"Âge: {teacher['age']}")
        print(f"Email: {teacher['email']}")
        print(f"Téléphone: {teacher['phone']}")
        print(f"Adresse: {teacher['address']}")
        print(f"Département ID: {teacher['department_id']}")
        print(f"Sujet: {teacher['subject']}")
        print("----")
        count += 1
        print(f"Total des enseignants de cette faculte: {count}")

def add_course():
    name = input("Nom de l'unité d'enseignement: ")
    faculty_id = input("ID de la faculté: ")
    teacher_id = input("ID de l'enseignant: ")
    semester = int(input("Semestre: "))
    year = int(input("Année: "))

    course = {
        "name": name,
        "faculty_id": ObjectId(faculty_id),
        "teacher_id": ObjectId(teacher_id),
        "semester": semester,
        "year": year
    }

    courses_collection.insert_one(course)
    print(f"Unité d'enseignement {name} ajoutée avec succès!")

def remove_course():
    course_id = input("ID de l'unité d'enseignement à supprimer: ")
    courses_collection.delete_one({"_id": ObjectId(course_id)})
    print(f"Unité d'enseignement avec l'ID {course_id} supprimée!")

def update_course():
    course_id = input("ID de l'unité d'enseignement à modifier: ")
    course = courses_collection.find_one({"_id": ObjectId(course_id)})

    if course:
        name = input(f"Nom actuel: {course['name']}. Nouveau nom ? (Appuyez sur Entrée pour conserver): ") or course['name']
        faculty_id = input(f"ID de la faculté actuelle: {course['faculty_id']}. Nouveau ID de la faculté ? (Appuyez sur Entrée pour conserver): ") or course['faculty_id']
        teacher_id = input(f"ID de l'enseignant actuel: {course['teacher_id']}. Nouveau ID de l'enseignant ? (Appuyez sur Entrée pour conserver): ") or course['teacher_id']
        semester = input(f"Semestre actuel: {course['semester']}. Nouveau semestre ? (Appuyez sur Entrée pour conserver): ") or course['semester']
        year = input(f"Année actuelle: {course['year']}. Nouvelle année ? (Appuyez sur Entrée pour conserver): ") or course['year']

        course_modifie = {
            "name": name,
            "faculty_id": ObjectId(faculty_id),
            "teacher_id": ObjectId(teacher_id),
            "semester": int(semester),
            "year": int(year)
        }
        courses_collection.update_one({"_id": ObjectId(course_id)}, {"$set": course_modifie})
        print(f"Unité d'enseignement avec l'ID {course_id} modifiée avec succès!")
    else:
        print(f"Unité d'enseignement avec l'ID {course_id} introuvable!")

def list_courses():
    count = 0
    for course in courses_collection.find():
        print(f"ID: {course['_id']}")
        print(f"Nom: {course['name']}")
        print(f"ID de la faculté: {course['faculty_id']}")
        print(f"ID de l'enseignant: {course['teacher_id']}")
        print(f"Semestre: {course['semester']}")
        print(f"Année: {course['year']}")
        print("----")
        count += 1
        print(f"Total des cours: {count}")

def list_courses_by_department():
    count = 0
    department_id = input("ID du département: ")
    teacher_ids = [teacher['_id'] for teacher in teachers_collection.find({"department_id": ObjectId(department_id)})]
    for course in courses_collection.find({"teacher_id": {"$in": teacher_ids}}):
        print(f"ID: {course['_id']}")
        print(f"Nom: {course['name']}")
        print(f"ID de la faculté: {course['faculty_id']}")
        print(f"ID de l'enseignant: {course['teacher_id']}")
        print(f"Semestre: {course['semester']}")
        print(f"Année: {course['year']}")
        print("----")
        count += 1
        print(f"Total des cours de ce departement: {count}")

def list_courses_by_faculty():
    count = 0
    faculty_id = input("ID de la faculté: ")
    for course in courses_collection.find({"faculty_id": ObjectId(faculty_id)}):
        print(f"ID: {course['_id']}")
        print(f"Nom: {course['name']}")
        print(f"ID de la faculté: {course['faculty_id']}")
        print(f"ID de l'enseignant: {course['teacher_id']}")
        print(f"Semestre: {course['semester']}")
        print(f"Année: {course['year']}")
        print("----")
        count += 1
        print(f"Total des cours de cette faculte: {count}")

def add_admin_staff():
    name = input("Nom du membre du personnel administratif: ")
    role = input("Rôle du membre du personnel administratif: ")
    department = input("Département du membre du personnel administratif: ")

    admin_staff = {
        "name": name,
        "role": role,
        "department": department
    }

    admin_staff_collection.insert_one(admin_staff)
    print(f"Membre du personnel administratif {name} ajouté avec succès!")

def remove_admin_staff():
    admin_staff_id = input("ID du membre du personnel administratif à supprimer: ")
    admin_staff_collection.delete_one({"_id": ObjectId(admin_staff_id)})
    print(f"Membre du personnel administratif avec l'ID {admin_staff_id} supprimé!")

def update_admin_staff():
    admin_staff_id = input("ID du membre du personnel administratif à modifier: ")
    admin_staff = admin_staff_collection.find_one({"_id": ObjectId(admin_staff_id)})

    if admin_staff:
        name = input(f"Nom actuel: {admin_staff['name']}. Nouveau nom ? (Appuyez sur Entrée pour conserver): ") or admin_staff['name']
        role = input(f"Rôle actuel: {admin_staff['role']}. Nouveau rôle ? (Appuyez sur Entrée pour conserver): ") or admin_staff['role']
        department = input(f"Département actuel: {admin_staff['department']}. Nouveau département ? (Appuyez sur Entrée pour conserver): ") or admin_staff['department']

        admin_staff_modifie = {
            "name": name,
            "role": role,
            "department": department
        }
        admin_staff_collection.update_one({"_id": ObjectId(admin_staff_id)}, {"$set": admin_staff_modifie})
        print(f"Membre du personnel administratif avec l'ID {admin_staff_id} modifié avec succès!")
    else:
        print(f"Membre du personnel administratif avec l'ID {admin_staff_id} introuvable!")

def list_admin_staff():
    count = 0
    for admin_staff in admin_staff_collection.find():
        print(f"ID: {admin_staff['_id']}")
        print(f"Nom: {admin_staff['name']}")
        print(f"Rôle: {admin_staff['role']}")
        print(f"Département: {admin_staff['department']}")
        print("----")
        count += 1
        print(f"Total des administrateurs: {count}")

# Fonction pour quitter le programme
def quitter():
    print("Au revoir!")
    exit()

if __name__ == "__main__":
    while True:
        print("\nMenu principal:")
        print("1. Gestion des étudiants")
        print("2. Gestion des enseignants")
        print("3. Gestion des unités d'enseignement (UE)")
        print("4. Gestion des cours")
        print("5. Gestion du personnel administratif")
        print("6. Generation des donnees tests")
        print("7. Quitter")

        choix = input("Veuillez saisir votre choix (1-6): ")

        if choix == "1":
            while True:
                print("\nGestion des étudiants:")
                print("1. Ajouter un étudiant")
                print("2. Supprimer un étudiant")
                print("3. Modifier un étudiant")
                print("4. Afficher la liste des étudiants")
                print("5. Afficher la liste des étudiants par département")
                print("6. Afficher la liste des étudiants par faculté")
                print("7. Nombre d'étudiants par UE")
                print("8. Revenir au menu principal")
                sous_choix = input("Veuillez saisir votre choix (1-8): ")
                if sous_choix == "1":
                    add_student()
                elif sous_choix == "2":
                    remove_student()
                elif sous_choix == "3":
                    update_student()
                elif sous_choix == "4":
                    list_students()
                elif sous_choix == "5":
                    list_students_by_department()
                elif sous_choix == "6":
                    list_students_by_faculty()
                elif sous_choix == "7":
                    get_students_per_course()
                elif sous_choix == "8":
                    break
                else:
                    print("Choix invalide!")
        elif choix == "2":
            while True:
                print("\nGestion des enseignants:")
                print("1. Ajouter un enseignant")
                print("2. Supprimer un enseignant")
                print("3. Modifier un enseignant")
                print("4. Afficher la liste des enseignants")
                print("5. Afficher la liste des enseignants par département")
                print("6. Afficher la liste des enseignants par faculté")
                print("7. Revenir au menu principal")
                sous_choix = input("Veuillez saisir votre choix (1-7): ")
                if sous_choix == "1":
                    add_teacher()
                elif sous_choix == "2":
                    remove_teacher()
                elif sous_choix == "3":
                    update_teacher()
                elif sous_choix == "4":
                    list_teachers()
                elif sous_choix == "5":
                    list_teachers_by_department()
                elif sous_choix == "6":
                    list_teachers_by_faculty()
                elif sous_choix == "7":
                    break
                else:
                    print("Choix invalide!")
        elif choix == "3":
            while True:
                print("\nGestion des unités d'enseignement (UE):")
                print("1. Ajouter une UE")
                print("2. Supprimer une UE")
                print("3. Modifier une UE")
                print("4. Afficher la liste des UE")
                print("5. Afficher la liste des UE par département")
                print("6. Afficher la liste des UE par faculté")
                print("7. Revenir au menu principal")
                sous_choix = input("Veuillez saisir votre choix (1-7): ")
                if sous_choix == "1":
                    add_course()
                elif sous_choix == "2":
                    remove_course()
                elif sous_choix == "3":
                    update_course()
                elif sous_choix == "4":
                    list_courses()
                elif sous_choix == "5":
                    list_courses_by_department()
                elif sous_choix == "6":
                    list_courses_by_faculty()
                elif sous_choix == "7":
                    break
                else:
                    print("Choix invalide!")
        elif choix == "4":
            while True:
                print("\nGestion des cours:")
                print("1. Afficher la liste des cours")
                print("2. Afficher la liste des cours par département")
                print("3. Afficher la liste des cours par faculté")
                print("4. Revenir au menu principal")
                sous_choix = input("Veuillez saisir votre choix (1-4): ")
                if sous_choix == "1":
                    list_courses()
                elif sous_choix == "2":
                    list_courses_by_department()
                elif sous_choix == "3":
                    list_courses_by_faculty()
                elif sous_choix == "4":
                    break
                else:
                    print("Choix invalide!")
        elif choix == "5":
            while True:
                print("\nGestion du personnel administratif:")
                print("1. Ajouter un membre du personnel administratif")
                print("2. Supprimer un membre du personnel administratif")
                print("3. Modifier un membre du personnel administratif")
                print("4. Afficher la liste des membres du personnel administratif")
                print("5. Revenir au menu principal")
                sous_choix = input("Veuillez saisir votre choix (1-5): ")
                if sous_choix == "1":
                    add_admin_staff()
                elif sous_choix == "2":
                    remove_admin_staff()
                elif sous_choix == "3":
                    update_admin_staff()
                elif sous_choix == "4":
                    list_admin_staff()
                elif sous_choix == "5":
                    break
                else:
                    print("Choix invalide!")
        elif choix == "6":
            generate_data()
        elif choix == "7":
            quitter()
        else:
            print("Choix invalide!")
            break
else:
     print("Choix invalide!")



