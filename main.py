class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self._finished_courses = []
        self.courses_in_progress = []
        self._grades = {}
    
    def __str__(self):
        # Hope the "length control" goes well
        avarage_grade = self.average_grade()
        info = (f'Имя: {self.name}\nФамилия: {self.surname}\n'
        f'Средняя оценка за домашние задания: {avarage_grade}\n'
        f'Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n'
        f'Завершенные курсы: {', '.join(self._finished_courses)}')
        return info

    def add_courses(self, course_name):
        self._finished_courses.append(course_name)
    
    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course
            in lecturer.courses_attached and course
            in self.courses_in_progress):
            if course in lecturer._rates:
                lecturer._rates[course] += [grade]
            else:
                lecturer._rates[course] = [grade]
        else:
            return 'InconsistError'
    
    def average_grade(self):
        avrg_every_course = [sum(x) / len(x) for x in self._grades.values()]
        avrg = sum(avrg_every_course) / len(avrg_every_course)
        return round(avrg, 1)
    
    # COMPARINGS
    def __eq__(self, student):
        return self.average_grade() == student.average_grade()
    
    def __gt__(self, student):
        return self.average_grade() > student.average_grade()
    
    def __lt__(self, student):
        return self.average_grade() < student.average_grade()

     
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self._rates = {}
    
    def __str__(self):
        info = (f'Имя: {self.name}\nФамилия: {self.surname}\n'
        f'Средняя оценка за лекции: {self.average_grade()}')
        return info
    
    def average_grade(self):
        avrg_every_course = [sum(x) / len(x) for x in self._rates.values()]
        avrg = sum(avrg_every_course) / len(avrg_every_course)
        return round(avrg, 1)
    
    def __eq__(self, lecturer):
        return self.average_grade() == lecturer.average_grade()
    
    def __gt__(self, lecturer):
        return self.average_grade() > lecturer.average_grade()
    
    def __lt__(self, lecturer):
        return self.average_grade() < lecturer.average_grade()
        

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        info = (f'Имя: {self.name}\nФамилия: {self.surname}')
        return info
        
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and course
            in student.courses_in_progress):
            if course in student._grades:
                student._grades[course] += [grade]
            else:
                student._grades[course] = [grade]
        else:
            return 'InconsistError'


def avrg_for_stud_per_course(students, course):
    grades_per_student = [student._grades[course] for student in students
                          if course in student._grades]
    avrg_every_student = [sum(x) / len(x) for x in grades_per_student]
    avrg = sum(avrg_every_student) / len(avrg_every_student)
    return round(avrg, 1)


def avrg_for_lect_per_course(lecturers, course):
    rates_per_lecturer = [lecturer._rates[course] for lecturer in lecturers
                          if course in lecturer._rates]
    avrg_every_lecturer = [sum(x) / len(x) for x in rates_per_lecturer]
    avrg = sum(avrg_every_lecturer) / len(avrg_every_lecturer)
    return round(avrg, 1)


# LECTURERS
lecturer_1 = Lecturer('Gin', 'Smith')
lecturer_1.courses_attached = ['Python']

lecturer_22 = Lecturer('Jane', 'Zvats')
lecturer_22.courses_attached = ['Java']

# STUDENTS
some_student_1 = Student('Ivan', 'Petrov', 'male')
some_student_1.courses_in_progress = ['Python', 'Java']
some_student_1.add_courses('English')
some_student_1.rate_lecturer(lecturer_1, 'Python', 10)
some_student_1.rate_lecturer(lecturer_22, 'Java', 9)

some_student_22 = Student('Petr', 'Ivanov', 'male')
some_student_22.courses_in_progress = ['Python', 'Java']
some_student_22.add_courses('English')
some_student_22.rate_lecturer(lecturer_1, 'Python', 7)
some_student_22.rate_lecturer(lecturer_22, 'Java', 10)

# REVIEWERS
some_reviewer_1 = Reviewer('Tom', 'Sees')
some_reviewer_1.rate_hw(some_student_1, 'Python', 10)
some_reviewer_1.rate_hw(some_student_1, 'Python', 8)
some_reviewer_1.rate_hw(some_student_22, 'Python', 8)
some_reviewer_1.rate_hw(some_student_22, 'Python', 8)

some_reviewer_22 = Reviewer('Kris', 'Ckekis')
some_reviewer_22.rate_hw(some_student_1, 'Java', 9.5)
some_reviewer_22.rate_hw(some_student_22, 'Java', 10)

# OUTPUT
print(lecturer_1, lecturer_22,
      some_student_1, some_student_22, 
      some_reviewer_1, sep='\n\n')

print('\n', some_student_1 == some_student_22)
print(some_student_1 > some_student_22)
print(some_student_1 < some_student_22)

print('\n', lecturer_1 == lecturer_22)
print(lecturer_1 > lecturer_22)
print(lecturer_1 < lecturer_22)

print('\nAvarage grades per course for students')
print(avrg_for_stud_per_course([some_student_1, some_student_22], 'Python'))
print(avrg_for_stud_per_course([some_student_1, some_student_22], 'Java'))

print('\nAvarage rates per course for lecturers')
print(avrg_for_lect_per_course([lecturer_1, lecturer_22], 'Python'))
print(avrg_for_lect_per_course([lecturer_1, lecturer_22], 'Java'))