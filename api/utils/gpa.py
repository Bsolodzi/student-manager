# conversion of score to a grade
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score < 90 and score >= 80:
        return 'B'
    elif score < 80 and score >= 70:
        return 'C'
    elif score < 70 and score >= 60:
        return 'D'
    elif score < 60 and score >= 50:
        return 'E'
    else:
        return 'F'
    

# gettting gpa based on scores
def get_gpa(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.5
    elif grade == 'C':
        return 3.0
    elif grade == 'D':
        return 2.5
    elif grade == 'E':
        return 2.0
    elif grade == 'F':
        return 1.5
    else:
        return 0