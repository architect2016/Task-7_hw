from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    SELECT s.group_id,
       round(AVG(gr.grade), 2) AS average_grade
    FROM grades gr
    JOIN students s ON gr.student_id = s.id
    JOIN subjects sub ON gr.subject_id = sub.id
    WHERE sub.id = 4 -- Замініть 'назва_предмета' на фактичну назву предмета
    GROUP BY s.group_id;
    """
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Subject, Subject.id == Grade.subjects_id) \
        .filter(Subject.id == 4) \
        .group_by(Student.group_id).all()
    return result


def select_04():
    """
    SELECT round(AVG(grade), 2) AS average_grade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).scalar()
    return result


def select_05():
    """
    SELECT t.fullname AS teacher_name, sub.name AS course_name
    FROM subjects sub
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE t.id = 2; -- Замініть id викладача на інше, для якого ви хочете знайти курси
    """
    result = session.query(Teacher.fullname, Subject.name.label('course_name')) \
        .join(Subject, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.id == 2).all()
    return result


def select_06():
    """
    SELECT s.fullname AS student_name, g.name AS group_name
    FROM students s
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1; -- Замініть id групи на іншу групу, для якої ви хочете знайти студентів
    """
    result = session.query(Student.fullname.label('student_name'), Group.name.label('group_name')) \
        .join(Group, Group.id == Student.group_id) \
        .filter(Group.id == 1).all()
    return result


def select_07():
    """
    SELECT g.grade, s.fullname AS student_name, sub.name as subject_name, gr.name as group_name
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN subjects sub ON g.subject_id = sub.id
    JOIN groups gr ON s.group_id = gr.id
    WHERE gr.id = 1 -- Замініть id групи на іншу групи
    AND sub.id = 5; -- Замініть id предмета на інше предмета
    """
    result = session.query(Grade.grade, Student.fullname.label('student_name'),
                           Subject.name.label('subject_name'), Group.name.label('group_name')) \
        .join(Student, Student.id == Grade.student_id) \
        .join(Subject, Subject.id == Grade.subjects_id) \
        .join(Group, Group.id == Student.group_id) \
        .filter(and_(Group.id == 1, Subject.id == 5)).all()
    return result


def select_08():
    """
    SELECT round(AVG(g.grade), 2) as average_grade, t.fullname as teacher_name, sub.name as subject_name
    FROM grades g
    JOIN subjects sub ON g.subject_id = sub.id
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE t.id = 3
    GROUP BY t.fullname, sub.name;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade'),
                           Teacher.fullname.label('teacher_name'),
                           Subject.name.label('subject_name')) \
        .join(Subject, Subject.id == Grade.subjects_id) \
        .join(Teacher, Teacher.id == Subject.teacher_id) \
        .filter(Teacher.id == 3) \
        .group_by(Teacher.fullname, Subject.name).all()
    return result


def select_09():
    """
    SELECT DISTINCT sub.name AS course_name, s.fullname as student_name
    FROM students s
    JOIN groups g ON s.group_id = g.id
    JOIN grades gr ON s.id = gr.student_id
    JOIN subjects sub ON gr.subject_id = sub.id
    WHERE s.id = 5; -- Замініть id студента на інше студента
    """
    result = session.query(Subject.name.label('course_name'), Student.fullname.label('student_name')) \
        .join(Grade, Grade.subjects_id == Subject.id) \
        .join(Student, Student.id == Grade.student_id) \
        .filter(Student.id == 5).distinct().all()
    return result


def select_10():
    """
    SELECT DISTINCT sub.name AS course_name, s.fullname as student_name, t.fullname as teacher_name
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sub ON g.subject_id = sub.id
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE s.id = 2 AND t.id = 2;

    """
    result = session.query(Subject.name.label('course_name'), Student.fullname.label('student_name'),
                           Teacher.fullname.label('teacher_name')) \
        .join(Grade, Grade.subjects_id == Subject.id) \
        .join(Student, Student.id == Grade.student_id) \
        .join(Teacher, Teacher.id == Subject.teacher_id) \
        .filter(Student.id == 2, Teacher.id == 2).distinct().all()
    return result


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_12())