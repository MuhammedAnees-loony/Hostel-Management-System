import logging
import mysql.connector
from mysql.connector import Error

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_contact(contact):
    if len(contact) > 15:
        raise ValueError("Contact number exceeds the maximum length of 15 characters.")

def create_connection():
    """Creates a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',    # Your host
            user='root',         # Your username
            password='200515',   # Your password
            database='hostel'    # Your database name
        )
        logging.info("Connection to MySQL DB successful")
    except Error as e:
        logging.error(f"The error '{e}' occurred")
    return connection

def truncate_tables(cursor):
    """Truncates all tables to start with a clean slate."""
    # Ensure 'roles' and 'user_roles' are included if necessary
    tables = [
        'user_roles', 'attendance', 'hostel_fee', 'room_allotment',
        'warden', 'student', 'room', 'faculty', 'hostel_manager',
        'hostel', 'floor', 'roles'
    ]
    try:
        # Disable foreign key checks once before truncating
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        logging.info("Foreign key checks disabled.")

        for table in tables:
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
            logging.info(f"Truncated table `{table}`.")
                
    except Error as e:
        logging.error(f"Error while truncating tables: {e}")
        raise
    finally:
        # Re-enable foreign key checks after truncating
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            logging.info("Re-enabled foreign key checks.")
        except Error as e:
            logging.error(f"Error while re-enabling foreign key checks: {e}")

def insert_roles(cursor):
    """Inserts predefined roles into the roles table."""
    roles = ['Student', 'Warden', 'Manager', 'Faculty']
    role_ids = {}
    for role in roles:
        cursor.execute(
            "INSERT INTO roles (Role_Name) VALUES (%s)",
            (role,)
        )
        role_ids[role] = cursor.lastrowid
        logging.info(f"Inserted role '{role}' with Role_ID {cursor.lastrowid}.")
    logging.info("Inserted all roles and collected Role IDs.")
    return role_ids

def insert_faculty(cursor):
    """Inserts faculty data into the faculty table."""
    faculty_data = [
        ("John Doe", "Mathematics", "1234567890", "john@example.com"),
        ("Jane Smith", "Physics", "0987654321", "jane@example.com"),
    ]
    faculty_ids = []
    for faculty in faculty_data:
        validate_contact(faculty[2])  # Validate contact number
        cursor.execute(
            "INSERT INTO faculty (Name, Department, Contact, Email) VALUES (%s, %s, %s, %s)",
            faculty
        )
        faculty_ids.append(cursor.lastrowid)  # Collect Faculty ID
        logging.info(f"Inserted faculty '{faculty[0]}' with Faculty_ID {cursor.lastrowid}.")
    logging.info("Inserted all faculty data and collected IDs.")
    return faculty_ids

def insert_hostel_manager(cursor):
    """Inserts hostel manager data into the hostel_manager table."""
    manager_data = [
        ("Alice Johnson", "9876543210", "alice@example.com"),
        ("Bob Brown", "1231231234", "bob@example.com"),
    ]
    manager_ids = []
    for manager in manager_data:
        validate_contact(manager[1])  # Validate contact number
        cursor.execute(
            "INSERT INTO hostel_manager (Name, Contact, Email) VALUES (%s, %s, %s)",
            manager
        )
        manager_ids.append(cursor.lastrowid)  # Collect Manager ID
        logging.info(f"Inserted hostel manager '{manager[0]}' with Manager_ID {cursor.lastrowid}.")
    logging.info("Inserted all hostel manager data and collected IDs.")
    return manager_ids

def insert_hostel(cursor, manager_ids):
    """Inserts hostel data into the hostel table."""
    hostel_data = [
        ('Hostel A', 'Location A', 5, 100, manager_ids[0]),
        ('Hostel B', 'Location B', 3, 50, manager_ids[1])
    ]
    hostel_ids = []
    for hostel in hostel_data:
        cursor.execute(
            "INSERT INTO hostel (Name, Location, Total_Floors, Total_Rooms, Manager_ID) VALUES (%s, %s, %s, %s, %s)", 
            hostel
        )
        hostel_ids.append(cursor.lastrowid)
        logging.info(f"Inserted hostel '{hostel[0]}' with Hostel_ID {cursor.lastrowid}.")
    logging.info("Inserted all hostel data and collected IDs.")
    return hostel_ids

def insert_floor(cursor, hostel_ids, hostel_floors):
    """
    Inserts floor data into the floor table.
    
    :param hostel_floors: A list containing the number of floors for each hostel corresponding to hostel_ids.
    :return: A dictionary mapping (Hostel_ID, Floor_Number) to Floor_ID
    """
    floor_mapping = {}
    for hostel_id, total_floors in zip(hostel_ids, hostel_floors):
        for floor_number in range(1, total_floors + 1):
            description = f"Floor {floor_number} of Hostel ID {hostel_id}"
            cursor.execute(
                "INSERT INTO floor (Hostel_ID, Floor_Number, Description) VALUES (%s, %s, %s)",
                (hostel_id, floor_number, description)
            )
            floor_id = cursor.lastrowid
            floor_mapping[(hostel_id, floor_number)] = floor_id
            logging.info(f"Inserted Floor {floor_number} for Hostel ID {hostel_id} with Floor_ID {floor_id}.")
    logging.info("Inserted all floor data and created floor mapping.")
    return floor_mapping

def insert_warden(cursor, hostel_ids, manager_ids, floor_mapping):
    """Inserts warden data into the warden table."""
    # Example warden data
    warden_data = [
        ("Alice Smith", "1234567890", "123 Warden St", "alicewarden@example.com", manager_ids[0], hostel_ids[0], 2),
        ("Bob Johnson", "0987654321", "456 Warden Ave", "bobwarden@example.com", manager_ids[1], hostel_ids[1], 1)
        # Ensure to use existing hostel_ids and manager_ids as necessary
    ]
    warden_ids = []
    for warden in warden_data:
        # Assign Floor_ID based on Hostel_ID and Assigned Floor Number
        hostel_id = warden[5]
        assigned_floor_number = warden[6]
        floor_id = floor_mapping.get((hostel_id, assigned_floor_number))
        if not floor_id:
            logging.error(f"Floor {assigned_floor_number} for Hostel ID {hostel_id} does not exist.")
            raise ValueError(f"Floor {assigned_floor_number} for Hostel ID {hostel_id} does not exist.")
        
        cursor.execute(
            "INSERT INTO warden (Name, Contact, Address, Email, Manager_ID, Hostel_ID, Assigned_Floor) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (warden[0], warden[1], warden[2], warden[3], warden[4], hostel_id, floor_id)
        )
        warden_ids.append(cursor.lastrowid)  # Collect Warden ID
        logging.info(f"Inserted warden '{warden[0]}' with Warden_ID {cursor.lastrowid}.")
    logging.info("Inserted all warden data and collected IDs.")
    return warden_ids

def insert_room(cursor, hostel_ids, floor_mapping):
    """Inserts room data into the room table."""
    # Correct Parameter Order:
    # (Room_Number, Capacity, Floor_Number, Room_Type, Fee_Amount, Room_Status, Hostel_ID)
    room_data = [
        ('101', 1, 1, 'Single', 1000.00, 'Available', hostel_ids[0]),
        ('102', 2, 1, '2-Shared', 500.00, 'Available', hostel_ids[0]),
        ('201', 3, 2, '3-Shared', 300.00, 'Available', hostel_ids[1]),
        ('202', 1, 2, 'Single', 1000.00, 'Available', hostel_ids[1])
    ]
    for room in room_data:
        room_number, capacity, floor_number, room_type, fee_amount, room_status, hostel_id = room
        floor_id = floor_mapping.get((hostel_id, floor_number))
        if not floor_id:
            logging.error(f"Floor {floor_number} for Hostel ID {hostel_id} does not exist.")
            raise ValueError(f"Floor {floor_number} for Hostel ID {hostel_id} does not exist.")
        
        cursor.execute(
            "INSERT INTO room (Room_Number, Capacity, Floor_Number, Room_Type, Fee_Amount, Room_Status, Hostel_ID, Floor_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (room_number, capacity, floor_number, room_type, fee_amount, room_status, hostel_id, floor_id)
        )
        logging.info(f"Inserted Room '{room_number}' with Room_ID {cursor.lastrowid}.")
    logging.info("Inserted all room data.")

def insert_student(cursor):
    """Inserts student data into the student table."""
    # Example student data (ensure Address is provided)
    student_data = [
        ("Mike Adams", "2000-01-01", "M", "5678901234", "mike@example.com", "123 Main St", 2),
        ("Sara Connor", "2001-02-02", "F", "6789012345", "sara@example.com", "456 Park Ave", 1),
        ("John Doe", "2002-03-03", "M", "7890123456", "john@example.com", "789 Elm St", 1),
        ("Emily Davis", "2003-04-04", "F", "8901234567", "emily@example.com", "101 Maple St", 2)
    ]
    student_ids = []
    for student in student_data:
        validate_contact(student[3])  # Validate contact number
        cursor.execute(
            "INSERT INTO student (Name, DOB, Gender, Contact, Email, Address, Year_of_Study) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            student
        )
        student_ids.append(cursor.lastrowid)  # Collect Student ID
        logging.info(f"Inserted student '{student[0]}' with Student_ID {cursor.lastrowid}.")
    logging.info("Inserted all student data and collected IDs.")
    return student_ids

def insert_user_roles(cursor, student_ids, role_ids):
    """Assigns roles to students via the user_roles table."""
    # Assuming all students have the 'Student' role
    student_role_id = role_ids.get('Student')
    if not student_role_id:
        logging.error("Role 'Student' does not exist.")
        raise ValueError("Role 'Student' does not exist.")
    
    for student_id in student_ids:
        cursor.execute(
            "INSERT INTO user_roles (User_ID, Role_ID) VALUES (%s, %s)",
            (student_id, student_role_id)
        )
        logging.info(f"Assigned 'Student' role to Student_ID {student_id}.")
    logging.info("Assigned roles to all students.")

def insert_room_allotment(cursor, student_ids, room_ids):
    """Inserts room allotment data into the room_allotment table."""
    # Example allotment data
    allotments = [
        # (Student_ID, Room_ID, Date_of_Allotment, Is_Active)
        (student_ids[0], room_ids[0], '2024-10-01', 1),
        (student_ids[1], room_ids[1], '2024-10-02', 1),
        (student_ids[2], room_ids[2], '2024-10-03', 1),
        (student_ids[3], room_ids[3], '2024-10-04', 1)
    ]

    for allotment in allotments:
        student_id, room_id, date_of_allotment, is_active = allotment
        try:
            # Check for existing active room allotments
            cursor.execute(
                "SELECT COUNT(*) FROM room_allotment WHERE Student_ID = %s AND Is_Active = 1",
                (student_id,)
            )
            existing_count = cursor.fetchone()[0]
            if existing_count > 0:
                logging.warning(f"Student_ID {student_id} already has an active room allotment. Skipping insertion.")
                continue  # Skip this student if they already have an active allotment

            # Use date_of_allotment in the insert statement
            cursor.execute(
                "INSERT INTO room_allotment (Student_ID, Room_ID, Date_of_Allotment, Is_Active) VALUES (%s, %s, %s, %s)",
                (student_id, room_id, date_of_allotment, is_active)
            )
            logging.info(f"Inserted room allotment for Student_ID {student_id} to Room_ID {room_id}.")
        except Exception as e:
            logging.error(f"Error inserting room allotment for Student_ID {student_id}: {e}")

    logging.info("Inserted all room allotment data.")



def insert_attendance(cursor, student_ids):
    """Inserts attendance data into the attendance table."""
    """Assuming attendance records for a specific date"""
    attendance_data = [
        # (Student_ID, Date, Status)
        (student_ids[0], '2024-10-01', 'Present'),
        (student_ids[1], '2024-10-01', 'Absent'),
        (student_ids[2], '2024-10-01', 'Present'),
        (student_ids[3], '2024-10-01', 'Absent')
    ]
    for record in attendance_data:
        student_id, date, status = record
        cursor.execute(
            "INSERT INTO attendance (Student_ID, Date, Status) VALUES (%s, %s, %s)",
            record
        )
        logging.info(f"Inserted attendance for Student_ID {student_id} on {date} as {status}.")
    logging.info("Inserted all attendance data.")
def insert_hostel_fee(cursor, student_ids):
    """Inserts hostel fee data into the hostel_fee table with a temporary fee amount."""
    successful_inserts = 0  # Counter for successful inserts
    temporary_fee_amount = 500.00  # Set a temporary fee amount
    
    for student_id in student_ids:
        try:
            # Retrieve the active room allotment for the student
            cursor.execute("""
                SELECT ra.Room_ID
                FROM room_allotment ra
                WHERE ra.Student_ID = %s AND ra.Is_Active = 1
                ORDER BY ra.Date_of_Allotment DESC
                LIMIT 1
            """, (student_id,))
            result = cursor.fetchone()

            if result:
                room_id = result[0]  # Get the Room_ID (if needed)
                
                # Define Due_Date and Payment_Status as per business logic
                due_date = '2024-10-01'  # Example due date
                payment_status = 'Unpaid'  # Example status

                # Insert into hostel_fee with the temporary fee amount
                cursor.execute(
                    "INSERT INTO hostel_fee (Amount, Due_Date, Payment_Status, Student_ID) VALUES (%s, %s, %s, %s)",
                    (temporary_fee_amount, due_date, payment_status, student_id)
                )
                successful_inserts += 1  # Increment counter
                logging.info(f"Inserted hostel fee for Student_ID {student_id}: Amount={temporary_fee_amount}, Due_Date={due_date}, Status={payment_status}.")
            else:
                logging.error(f"No active room allotment found for Student_ID {student_id}. Cannot insert hostel_fee.")
                raise ValueError(f"No active room allotment found for Student_ID {student_id}.")
        except Exception as e:
            logging.error(f"Error processing Student_ID {student_id}: {e}")
            continue  # Skip to the next student

    logging.info(f"Inserted all hostel fee data. Total successful inserts: {successful_inserts}.")





def insert_room_ids(cursor):
    """Retrieves all Room_IDs after insertion for use in room_allotment."""
    cursor.execute("SELECT Room_ID FROM room ORDER BY Room_ID;")
    rooms = cursor.fetchall()
    room_ids = [room[0] for room in rooms]
    logging.info(f"Retrieved Room_IDs: {room_ids}")
    return room_ids

def main():
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            # Truncate all tables to start fresh
            truncate_tables(cursor)
            connection.commit()
            
            # Insert roles
            role_ids = insert_roles(cursor)
            connection.commit()
            
            # Insert data into faculty
            faculty_ids = insert_faculty(cursor)
            connection.commit()
            
            # Insert data into hostel_manager
            manager_ids = insert_hostel_manager(cursor)
            connection.commit()
            
            # Insert data into hostel
            hostel_ids = insert_hostel(cursor, manager_ids)
            connection.commit()
            
            # Insert floor data
            # Define number of floors per hostel (matching hostel_ids order)
            hostel_floors = [5, 3]  # Hostel A has 5 floors, Hostel B has 3 floors
            floor_mapping = insert_floor(cursor, hostel_ids, hostel_floors)
            connection.commit()
            
            # Insert warden data
            warden_ids = insert_warden(cursor, hostel_ids, manager_ids, floor_mapping)
            connection.commit()
            
            # Insert room data
            insert_room(cursor, hostel_ids, floor_mapping)
            connection.commit()
            
            # Insert student data
            student_ids = insert_student(cursor)
            connection.commit()
            
            # Assign roles to students
            insert_user_roles(cursor, student_ids, role_ids)
            connection.commit()
            
            # Insert room allotment data
            room_ids = insert_room_ids(cursor)
            insert_room_allotment(cursor, student_ids, room_ids)
            connection.commit()
            
            # Insert attendance data
            insert_attendance(cursor, student_ids)
            connection.commit()
            
            # Insert hostel fee data
            insert_hostel_fee(cursor, student_ids)
            connection.commit()
            
            logging.info("All data inserted successfully.")
            
        except Error as e:
            logging.error(f"Error: {e}")
            connection.rollback()  # Rollback in case of error
        finally:
            cursor.close()
            connection.close()
            logging.info("Connection to MySQL DB closed")

if __name__ == "__main__":
    main()
