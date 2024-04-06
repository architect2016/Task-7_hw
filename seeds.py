import random
from faker import Faker
from conf.db import session
from conf.models import Student, Group, Subject, Teacher, Grade

fake = Faker()


# Функція генерування випадкових оцінок для студента з предмету
def generate_grades(student_id, subject_id):
    num_grades = random.randint(10, 20)
    grades = []
    for _ in range(num_grades):
        grade = random.uniform(2, 5) 
        grade_obj = Grade(student_id=student_id, subjects_id=subject_id, grade=grade)
        grades.append(grade_obj)
    return grades


# Учні
students = []
for _ in range(30):
    student = Student(fullname=fake.name())
    students.append(student)

# Групи
groups = [Group(name=f'Group {i}') for i in range(1, 4)]

# Предмети
subjects = [Subject(name=fake.word()) for _ in range(5, 9)]

# Вчителя
teachers = [Teacher(fullname=fake.name()) for _ in range(3, 6)]

# Додати об’єкти до сеансу
session.add_all(students)
session.add_all(groups)
session.add_all(subjects)
session.add_all(teachers)
session.commit()

# Заповнити оцінки
for student in students:
    for subject in subjects:
        grades = generate_grades(student.id, subject.id)
        session.add_all(grades)
        session.commit()

print("Database seeded successfully.")
