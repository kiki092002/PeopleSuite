
from flask import Flask, jsonify, request
import mysql.connector
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/PeopleSuiteDB'  # Updated database name
db = SQLAlchemy(app)
@app.route('/')
def hello_world():
    return 'Hello, PeopleSuite!'

class Employee(db.Model):
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    EmailAddress = db.Column(db.String(100), nullable=False, unique=True)
    Country = db.Column(db.String(2), nullable=False)

@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'GET':
        employees_list = Employee.query.all()
        employees = [{"EmployeeID": emp.EmployeeID, "FirstName": emp.FirstName, "LastName": emp.LastName,
                      "EmailAddress": emp.EmailAddress, "Country": emp.Country} for emp in employees_list]
        return jsonify(employees)
    elif request.method == 'POST':
        new_employee_data = request.get_json()
        new_employee = Employee(**new_employee_data)
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"EmployeeID": new_employee.EmployeeID,
                        "FirstName": new_employee.FirstName,
                        "LastName": new_employee.LastName,
                        "EmailAddress": new_employee.EmailAddress,
                        "Country": new_employee.Country})

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        return jsonify({"EmployeeID": employee.EmployeeID,
                        "FirstName": employee.FirstName,
                        "LastName": employee.LastName,
                        "EmailAddress": employee.EmailAddress,
                        "Country": employee.Country})
    else:
        return jsonify({"error": "Employee not found"}), 404



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')