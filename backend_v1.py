from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import base64
app = Flask(__name__)
CORS(app)

# Database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '200515',
    'database': 'hostel'
}

# List of required tables
required_tables = [
    'attendance',
    'credentials',
    'faculty',
    'floor',
    'hostel',
    'hostel_fee',
    'hostel_manager',
    'roles',
    'room',
    'room_allotment',
    'student',
    'warden'
]

ROLE_MAPPING = {
    "student": 1,
    "warden": 2,
    "manager": 3,
    "faculty": 4
}

def check_tables_exist():
    print("Checking if all required tables exist...")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    missing_tables = []
    
    for table in required_tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}';")
        result = cursor.fetchone()
        if not result:
            missing_tables.append(table)
            print(f"Table missing: {table}")
    
    cursor.close()
    connection.close()
    return missing_tables

@app.route('/check_tables', methods=['GET'])
def check_tables():
    print("Endpoint /check_tables called")
    missing_tables = check_tables_exist()
    if missing_tables:
        print("Missing tables:", missing_tables)
        return jsonify({
            'status': 'fail',
            'message': 'Missing tables: ' + ', '.join(missing_tables)
        }), 500
    else:
        print("All required tables are present.")
        return jsonify({
            'status': 'success',
            'message': 'All required tables are present.'
        }), 200

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        print("OPTIONS request received for /login")
        response = jsonify({'status': 'preflight check successful'})
        response.headers.add("Access-Control-Allow-Origin", "https://muhammedanees-loony.github.io")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    data = request.get_json()
    print("Login request data received:", data)

    login_id = data.get('loginId')
    password = data.get('password')
    user_type = data.get('userType')
    role_id = ROLE_MAPPING.get(user_type.lower())
    
    if role_id is None:
        print("Invalid user type:", user_type)
        return jsonify({'status': 'fail', 'message': 'Invalid user type'}), 400

    missing_tables = check_tables_exist()
    if missing_tables:
        print("Missing tables detected in /login:", missing_tables)
        return jsonify({'status': 'fail', 'message': 'Missing tables: ' + ', '.join(missing_tables)}), 500

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT User_ID, Password, Role_ID
    FROM credentials
    WHERE User_Name = %s AND Password = %s AND Role_ID = %s AND Status = 'active';
    """
    cursor.execute(query, (login_id, password, role_id))
    credentials_result = cursor.fetchone()
    cursor.nextset()

    if credentials_result:
        print("Credentials validated for user:", login_id)
        user_id = credentials_result['User_ID']
        user_data = None
        if user_type == "student":
            user_query = "SELECT * FROM student WHERE Student_ID = %s"
        elif user_type == "faculty":
            user_query = "SELECT * FROM faculty WHERE faculty_id = %s"
        elif user_type == "manager":
            user_query = "SELECT * FROM hostel_manager WHERE Manager_ID = %s"
        elif user_type== "warden":
            user_query= "SELECT * FROM warden WHERE Warden_ID = %s"

        cursor.execute(user_query, (user_id,))
        user_data = cursor.fetchone()

        if user_type == "student" and user_data:
            # Retrieve Room_ID from room_allotment table
            room_allotment_query = "SELECT Room_ID FROM room_allotment WHERE Student_ID = %s AND Is_Active = 1"
            cursor.execute(room_allotment_query, (user_id,))
            room_allotment_data = cursor.fetchone()

            if room_allotment_data:
                room_id = room_allotment_data['Room_ID']
                
                # Retrieve room details from room table
                room_query = "SELECT Room_Number, Hostel_ID FROM room WHERE Room_ID = %s"
                cursor.execute(room_query, (room_id,))
                room_data = cursor.fetchone()

                if room_data:
                    room_number = room_data['Room_Number']
                    hostel_id = room_data['Hostel_ID']
                    
                    # Retrieve hostel name from hostel table
                    hostel_query = "SELECT Name FROM hostel WHERE Hostel_ID = %s"
                    cursor.execute(hostel_query, (hostel_id,))
                    hostel_data = cursor.fetchone()

                    if hostel_data:
                        hostel_name = hostel_data['Name']
                        user_data['room_number'] = room_number
                        user_data['hostel_name'] = hostel_name
                        user_data['user_id']=user_id
                        print(f"Room number and hostel name found: {room_number}, {hostel_name}")
        
        # warden
        if user_type=="warden":
            room_allotment_query = "SELECT Room_ID FROM room_allotment WHERE Student_ID = %s AND Is_Active = 1"
            cursor.execute(room_allotment_query, (user_id,))
            room_allotment_data = cursor.fetchone()

            if room_allotment_data:
                room_id = room_allotment_data['Room_ID']
                
                # Retrieve room details from room table
                room_query = "SELECT Room_Number, Hostel_ID FROM room WHERE Room_ID = %s"
                cursor.execute(room_query, (room_id,))
                room_data = cursor.fetchone()

                if room_data:
                    room_number = room_data['Room_Number']
                    hostel_id = room_data['Hostel_ID']
                    
                    # Retrieve hostel name from hostel table
                    hostel_query = "SELECT Name FROM hostel WHERE Hostel_ID = %s"
                    cursor.execute(hostel_query, (hostel_id,))
                    hostel_data = cursor.fetchone()

                    if hostel_data:
                        hostel_name = hostel_data['Name']
                        user_data['room_number'] = room_number
                        user_data['user_id']=user_id
                        user_data['hostel_name'] = hostel_name
                        print(f"Room number and hostel name found: {room_number}, {hostel_name},{user_id}")

        cursor.close()
        connection.close()

        if user_data:
            print(f"User data found for {user_type}:", user_data)
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'username': login_id,
                    'role_id': credentials_result['Role_ID'],
                    'user_details': user_data
                    
                }
            }), 200
        else:
            print(f"No user data found in specific table for {user_type}.")
            return jsonify({'status': 'fail', 'message': 'User details not found in specific table'}), 404
    else:
        cursor.close()
        connection.close()
        print("Invalid credentials provided.")
        return jsonify({'status': 'fail', 'message': 'Invalid login ID, password, or user type'}), 401
    

@app.route('/api/getStudents', methods=['POST'])
def get_students_by_room():
    data = request.json
    room_number = data.get('roomNumber')
    print(f"Received room number: {room_number}")

    if not room_number:
        print("Error: Room number is required")
        return jsonify({"error": "Room number is required"}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch Room_ID based on Room_Number from the room table
        cursor.execute("SELECT Room_ID FROM room WHERE Room_Number = %s", (room_number,))
        room = cursor.fetchone()
        print(f"Room query result: {room}")

        if not room:
            print("Error: Room not found")
            return jsonify({"error": "Room not found"}), 404

        room_id = room["Room_ID"]
        print(f"Found Room_ID: {room_id}")

        # Fetch Student_IDs from room_allotment where Room_ID matches and Is_Active = 1
        cursor.execute("SELECT Student_ID FROM room_allotment WHERE Room_ID = %s AND Is_Active = 1", (room_id,))
        student_ids = cursor.fetchall()
        print(f"Student IDs fetched: {student_ids}")

        if not student_ids:
            print("No active students found in this room")
            return jsonify({"students": []})

        # Convert list of dictionaries to a flat list of student IDs
        student_ids = [sid["Student_ID"] for sid in student_ids]
        print(f"Extracted Student_IDs: {student_ids}")

        # Adjust the query to work with single or multiple IDs
        format_strings = ','.join(['%s'] * len(student_ids))
        query = f"SELECT Student_ID, Name FROM student WHERE Student_ID IN ({format_strings})"
        cursor.execute(query, tuple(student_ids))
        students = cursor.fetchall()
        print(f"Fetched students: {students}")

        # Format the data as a list of dictionaries with student ID and name
        student_list = [{"id": student["Student_ID"], "name": student["Name"]} for student in students]
        print(f"Formatted student list: {student_list}")

        return jsonify({"students": student_list})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()



@app.route('/attendance', methods=['POST', 'OPTIONS'])
def get_attendance():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'preflight check successful'})
        response.headers.add("Access-Control-Allow-Origin", "https://muhammedanees-loony.github.io")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    data = request.get_json()
    student_id = data.get('student_id')
    date_str = data.get('date')
    print(student_id,date_str)
    
    # Convert date to a datetime object to handle date comparisons
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'status': 'fail', 'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    if not student_id:
        return jsonify({'status': 'fail', 'message': 'Student ID is required'}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT Date, Status
    FROM attendance
    WHERE Student_ID = %s AND Date <= %s
    ORDER BY Date ASC;
    """
    cursor.execute(query, (student_id, date))
    attendance_records = cursor.fetchall()
    print(attendance_records)
    cursor.close()
    connection.close()

    if attendance_records:
        return jsonify({
            'status': 'success',
            'message': 'Attendance records retrieved successfully',
            'data': attendance_records
        }), 200
    else:
        return jsonify({
            'status': 'fail',
            'message': 'No attendance records found for the given student and date'
        }), 404
    
@app.route('/api/getFeeDetails', methods=['POST'])
def get_fee_details():
    data = request.json
    date = data.get('date')
    
    # Print the received date from frontend
    print(f"Received date: {date}")
    
    if not date:
        print("Error: Date is required.")
        return jsonify({"error": "Date is required"}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Fetch fee details for the given date along with the user name
        query = """
        SELECT fp.user_id, fp.fee_category, fp.image, fp.payment_date, s.Name as student_name
        FROM fee_payment fp
        JOIN student s ON fp.user_id = s.Student_ID
        WHERE DATE(fp.payment_date) = %s
        """
        print(f"Executing query with date: {date}")
        cursor.execute(query, (date,))
        fee_details = cursor.fetchall()

        if not fee_details:
            print(f"No fee records found for the date: {date}")
            return jsonify({"success": False, "message": "No fee records found for this date"}), 404

        users = []
       # print(f"Fetched fee details: {fee_detail.user_id}")

        for detail in fee_details:
            print(f"User ID: {detail['user_id']}")
            user = {
                'id': detail['user_id'],
                'name': detail['student_name'],
                'fee_category': detail['fee_category'],
                'receipt': convert_image_to_base64(detail['image']) if detail['image'] else None
            }
            users.append(user)

        print(f"Returning fee details for {len(users)} users.")
        return jsonify({"success": True, "users": users})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

def convert_image_to_base64(image_data):
    if image_data:
        print(f"Converting image to base64...")
        return base64.b64encode(image_data).decode('utf-8')
    return None

@app.route('/api/markAttendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    date = data.get('date')
    status = data.get('status')
    print(f"Received attendance data - Student ID: {student_id}, Date: {date}, Status: {status}")

    if not student_id or not date or status not in ['Present', 'Absent']:
        print("Error: Missing or invalid data")
        return jsonify({"error": "Student ID, date, and valid status (Present/Absent) are required"}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Check if attendance for this student and date already exists
        cursor.execute("SELECT * FROM attendance WHERE Student_ID = %s AND Date = %s", (student_id, date))
        existing_record = cursor.fetchone()
        print(f"Existing record check: {existing_record}")

        if existing_record:
            # Update existing attendance record
            cursor.execute("UPDATE attendance SET Status = %s WHERE Student_ID = %s AND Date = %s", 
                           (status, student_id, date))
            print(f"Updated attendance for Student ID {student_id} on {date} to {status}")
        else:
            # Insert new attendance record
            cursor.execute("INSERT INTO attendance (Student_ID, Date, Status) VALUES (%s, %s, %s)", 
                           (student_id, date, status))
            print(f"Inserted attendance for Student ID {student_id} on {date} with status {status}")

        connection.commit()
        return jsonify({"success": True, "message": f"Attendance marked as {status} for Student ID {student_id} on {date}"}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/upload_fee_payment', methods=['POST'])
def upload_fee_payment():
    # Get form data
    user_id = request.form.get('user_id')
    fee_category = request.form.get('fee_category')

    # Get the uploaded image file
    image = request.files.get('image')
    
    if not user_id or not fee_category or not image:
        return jsonify({'status': 'fail', 'message': 'Missing data'}), 400

    # Read the image as binary
    image_binary = image.read()

    # Get current timestamp
    timestamp = datetime.now()

    # Create a connection to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    # Insert into the fee_payment table
    query = """
    INSERT INTO fee_payment (user_id, fee_category, image, payment_date)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, fee_category, image_binary, timestamp))
    
    # Commit the transaction
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    return jsonify({'status': 'success', 'message': 'Payment receipt uploaded successfully'}), 200

@app.route('/get_fee_status', methods=['POST'])
def get_fee_status():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract user_id from the request data
        user_id = data.get('user_id')

        # Check if user_id is provided
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Invalid parameters'}), 400
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        # Query to fetch the fee status and pending amount for the user
        query = """
            SELECT Amount AS pending_amount, Payment_Status
            FROM hostel_fee
            WHERE Student_ID = %s AND Payment_Status = 'Unpaid'
        """

        # Execute the query
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  # Get the first result

        # Check if the fee status was retrieved
        if result:
            if result['Payment_Status'] == 'Unpaid':
                pending_amount = result['pending_amount']
                return jsonify({'status': 'success', 'pending_amount': pending_amount}), 200
            else:
                return jsonify({'status': 'success', 'pending_amount': 0}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No record found for this user'}), 404

    except Exception as err:
        return jsonify({'status': 'error', 'message': 'Error processing request'}), 500

    finally:
        # Ensure the cursor is closed after use
        cursor.close()

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    print("Registration request data received:", data)

    user_type = data.get('user_type')
    name = data.get('name')
    contact = data.get('contact')
    email = data.get('email')
    assigned_floor = data.get('assigned_floor')

    missing_tables = check_tables_exist()
    if missing_tables:
        print("Missing tables detected in /register_user:", missing_tables)
        return jsonify({'status': 'fail', 'message': 'Missing tables: ' + ', '.join(missing_tables)}), 500

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        if user_type == 'student':
            dob = data.get('dob')
            gender = data.get('gender')
            address = data.get('address')
            year_of_study = data.get('year_of_study')
            query = """
            INSERT INTO student (Name, DOB, Gender, Contact, Email, Address, Year_of_Study)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (name, dob, gender, contact, email, address, year_of_study))
            connection.commit()
            student_id = cursor.lastrowid
            print("Student registered with ID:", student_id)
            return jsonify({'status': 'success', 'message': 'Student registered successfully', 'student_id': student_id}), 201
        elif user_type == 'faculty':
            department = data.get('department')
            query = """
            INSERT INTO faculty (Name, Department, Contact, Email, Assigned_Floor)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (name, department, contact, email, assigned_floor))
            connection.commit()
            faculty_id = cursor.lastrowid
            print("Faculty registered with ID:", faculty_id)
            return jsonify({'status': 'success', 'message': 'Faculty registered successfully', 'faculty_id': faculty_id}), 201
        elif user_type == 'warden':
            address = data.get('address')
            hostel_id = data.get('hostel_id')
            query = """
            INSERT INTO warden (Name, Contact, Address, Email, Manager_ID, Hostel_ID, Assigned_Floor)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (name, contact, address, email, None, hostel_id, assigned_floor))
            connection.commit()
            warden_id = cursor.lastrowid
            print("Warden registered with ID:", warden_id)
            return jsonify({'status': 'success', 'message': 'Warden registered successfully', 'warden_id': warden_id}), 201
        elif user_type == 'hostel_manager':
            query = """
            INSERT INTO hostel_manager (Name, Contact, Email)
            VALUES (%s, %s, %s);
            """
            cursor.execute(query, (name, contact, email))
            connection.commit()
            manager_id = cursor.lastrowid
            print("Hostel Manager registered with ID:", manager_id)
            return jsonify({'status': 'success', 'message': 'Hostel Manager registered successfully', 'manager_id': manager_id}), 201
        else:
            print("Invalid user type provided during registration:", user_type)
            return jsonify({'status': 'fail', 'message': 'Invalid user type'}), 400
    except mysql.connector.Error as err:
        print("Database error during registration:", err)
        connection.rollback()
        return jsonify({'status': 'fail', 'message': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
