from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# ------------------ Database Configuration ------------------
db_config = {
    "host": "your-rds-endpoint.amazonaws.com",  # replace with your RDS endpoint
    "user": "admin",
    "password": "Cloud1234",
    "database": "employeedb"
}

def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# ------------------ Add Employee ------------------
@app.route("/api/employees", methods=["POST"])
def add_employee():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        department = data.get("department")
        role = data.get("role")

        if not name or not email or not department or not role:
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO employees (name, email, department, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, email, department, role))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Employee added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Get All Employees ------------------
@app.route("/api/employees", methods=["GET"])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, department, role, created_at FROM employees ORDER BY id DESC")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Delete Employee ------------------
@app.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
