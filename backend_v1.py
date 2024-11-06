from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

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
            user_query = "SELECT * FROM faculty WHERE User_ID = %s"
        elif user_type == "manager":
            user_query = "SELECT * FROM hostel_manager WHERE User_ID = %s"

        cursor.execute(user_query, (user_id,))
        user_data = cursor.fetchone()

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
