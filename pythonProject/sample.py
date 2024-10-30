import sqlalchemy as db

# Create engine and connect to the SQLite database
engine = db.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = db.MetaData()

# Define the Studentt table
Studentt = db.Table('Studentt', metadata,
                    db.Column('Id', db.Integer(), primary_key=True),
                    db.Column('Name', db.String(255), nullable=False),
                    db.Column('Major', db.String(255), default="Math"),
                    db.Column('marks', db.Integer(), default=35)
                    )

# Create the table in the database
metadata.create_all(engine)

# Insert data into the Studentt table
query = db.insert(Studentt)
values_list = [
    {'Id': 2, 'Name': 'Nisha', 'Major': "Science", 'marks': 50},
    {'Id': 3, 'Name': 'Natasha', 'Major': "Math", 'marks': 60},
    {'Id': 4, 'Name': 'Ben', 'Major': "English", 'marks': 70}
]
conn.execute(query, values_list)


# Function to update a student's marks by Id
def update_student_marks(student_id, new_marks):
    update_query = db.update(Studentt).where(Studentt.c.Id == student_id).values(marks=new_marks)
    conn.execute(update_query)
    print(f"Updated marks for student with Id {student_id} to {new_marks}.")


# Update marks for a specific student
update_student_marks(2, 90)  # Update Nisha's marks to 90
update_student_marks(3, 75)  # Update Natasha's marks to 75


# Function to sum up all marks
# Function to calculate total and average marks
def calculate_marks():
    # Query for total marks
    total_query = db.select(db.func.sum(Studentt.c.marks).label('total_marks'))
    total_result = conn.execute(total_query).scalar()  # Get the total marks

    # Query for average marks
    average_query = db.select(db.func.avg(Studentt.c.marks).label('average_marks'))
    average_result = conn.execute(average_query).scalar()  # Get the average marks

    return total_result if total_result is not None else 0, average_result if average_result is not None else 0


# Retrieve and print all data from the Studentt table
output = conn.execute(Studentt.select()).fetchall()
print(output)

total_marks, average_marks = calculate_marks()

# Print the results
print(f"Total marks in the Studentt table: {total_marks}")
print(f"Average marks in the Studentt table: {average_marks:.2f}")


def get_students_ordered_by_marks():
    # Query to select all students ordered by marks in ascending order
    order_query = db.select(Studentt).order_by(Studentt.c.marks.asc())
    return conn.execute(order_query).fetchall()


# Retrieve and print all students ordered by marks
ordered_students = get_students_ordered_by_marks()

# Print the results
print("Students ordered by Marks (Ascending):")
for record in ordered_students:
    print(f"Name: {record.Name}, Marks: {record.marks}")


def get_max_min_students():
    try:
        # Retrieve all student records
        all_students = conn.execute(db.select(Studentt)).fetchall()

        if not all_students:
            print("No student records found.")
            return [], []

        # Initialize variables for max and min
        max_marks = all_students[0].marks
        min_marks = all_students[0].marks

        # Find max and min marks
        for student in all_students:
            if student.marks > max_marks:
                max_marks = student.marks
            if student.marks < min_marks:
                min_marks = student.marks

        # Collect students with max and min marks
        max_students = [student for student in all_students if student.marks == max_marks]
        min_students = [student for student in all_students if student.marks == min_marks]

        return max_students, min_students

    except Exception as e:
        print(f"Error retrieving max/min students: {e}")
        return [], []


# Retrieve and print max and min marks with student names
max_records, min_records = get_max_min_students()

print("Students with Maximum Marks:")
for record in max_records:
    print(f"Name: {record.Name}, Marks: {record.marks}")

print("Students with Minimum Marks:")
for record in min_records:
    print(f"Name: {record.Name}, Marks: {record.marks}")
conn.close()