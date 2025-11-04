from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

employees = [
    {"id": 1, "name": "Abdul", "role": "Manager"},
    {"id": 2, "name": "Sara", "role": "Developer"},
    {"id": 3, "name": "John", "role": "Designer"}
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    new_id = len(employees) + 1
    new_emp = {"id": new_id, "name": data["name"], "role": data["role"]}
    employees.append(new_emp)
    return jsonify(new_emp), 201

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    global employees
    employees = [e for e in employees if e["id"] != emp_id]
    return jsonify({"message": "Employee deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
