from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

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

def check_tables_exist():
    # Establish a connection to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    missing_tables = []
    
    for table in required_tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}';")
        result = cursor.fetchone()
        if not result:
            missing_tables.append(table)

    cursor.close()
    connection.close()

    return missing_tables

@app.route('/check_tables', methods=['GET'])
def check_tables():
    missing_tables = check_tables_exist()

    if missing_tables:
        return jsonify({
            'status': 'fail',
            'message': 'Missing tables: ' + ', '.join(missing_tables)
        }), 500
    else:
        return jsonify({
            'status': 'success',
            'message': 'All required tables are present.'
        }), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Login Request Data:", data)  # Print received login data
    username = data.get('username')
    password = data.get('password')

    # Check if tables exist
    missing_tables = check_tables_exist()
    if missing_tables:
        return jsonify({
            'status': 'fail',
            'message': 'Missing tables: ' + ', '.join(missing_tables)
        }), 500

    # Establish a connection to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to check if the username and password match
    query = """
    SELECT User_Name, Password, Role_ID
    FROM credentials
    WHERE User_Name = %s AND Password = %s AND Status = 'active';
    """
    
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'username': result['User_Name'],
                'role_id': result['Role_ID']
            }
        }), 200
    else:
        return jsonify({
            'status': 'fail',
            'message': 'Invalid username or password'
        }), 401

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    print("Registration Request Data:", data)  # Print received registration data
    user_type = data.get('user_type')

    # Common fields for all user types
    name = data.get('name')
    contact = data.get('contact')
    email = data.get('email')
    assigned_floor = data.get('assigned_floor')

    # Check if tables exist
    missing_tables = check_tables_exist()
    if missing_tables:
        return jsonify({
            'status': 'fail',
            'message': 'Missing tables: ' + ', '.join(missing_tables)
        }), 500

    # Establish a connection to the database
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
            return jsonify({
                'status': 'success',
                'message': 'Student registered successfully',
                'student_id': student_id
            }), 201

        elif user_type == 'faculty':
            department = data.get('department')

            query = """
            INSERT INTO faculty (Name, Department, Contact, Email, Assigned_Floor)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (name, department, contact, email, assigned_floor))
            connection.commit()
            faculty_id = cursor.lastrowid
            return jsonify({
                'status': 'success',
                'message': 'Faculty registered successfully',
                'faculty_id': faculty_id
            }), 201

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
            return jsonify({
                'status': 'success',
                'message': 'Warden registered successfully',
                'warden_id': warden_id
            }), 201

        elif user_type == 'hostel_manager':
            query = """
            INSERT INTO hostel_manager (Name, Contact, Email)
            VALUES (%s, %s, %s);
            """
            cursor.execute(query, (name, contact, email))
            connection.commit()
            manager_id = cursor.lastrowid
            return jsonify({
                'status': 'success',
                'message': 'Hostel Manager registered successfully',
                'manager_id': manager_id
            }), 201

        else:
            return jsonify({
                'status': 'fail',
                'message': 'Invalid user type'
            }), 400

    except mysql.connector.Error as err:
        connection.rollback()  # Rollback if there is an error
        return jsonify({
            'status': 'fail',
            'message': str(err)
        }), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
