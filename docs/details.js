from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for demonstration
data = {
    'student': {
        'John Doe': {
            'name': 'John Doe',
            'roomNumber': '101',
            'hostelName': 'Alpha Hostel',
            'userType': 'student',
            'course': 'Computer Science'
        }
    },
    'faculty': {
        'Dr. Smith': {
            'name': 'Dr. Smith',
            'roomNumber': '301',
            'hostelName': 'Beta Hostel',
            'userType': 'faculty',
            'department': 'Computer Science'
        }
    }
}

@app.route('/getDetails')
def get_details():
    user_name = request.args.get('userName')
    user_type = request.args.get('userType')

    if user_type in data and user_name in data[user_type]:
        return jsonify({'success': True, 'details': data[user_type][user_name]})
    
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
