from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  # Changed from pyodbc
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# def get_db_connection():
#     """Create and return a MySQL database connection"""
#     try:
#         conn = mysql.connector.connect(
#             host=os.getenv('DB_HOST'),
#             port=os.getenv('DB_PORT'),
#             user=os.getenv('DB_USER'),
#             password=os.getenv('DB_PASSWORD'),
#             database=os.getenv('DB_DATABASE')
#         )
#         return conn
#     except mysql.connector.Error as e:
#         print(f"Database connection failed: {e}")
#         raise

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            ssl_ca=os.getenv('SSL_CA'),
            ssl_disabled=False
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        raise



# def get_db_connection():
#     return mysql.connector.connect(
#         host=os.getenv('DB_HOST'),
#         port=os.getenv('DB_PORT'),
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASSWORD'),
#         database=os.getenv('DB_DATABASE'),
#         ssl_ca=os.getenv('SSL_CA'),
#         ssl_disabled=False  # Enable SSL
#     )

@app.route('/')
def index():
    """Display all tasks"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM tasks ORDER BY due_date")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        return f"Error loading tasks: {str(e)}", 500

@app.route('/add', methods=['POST'])
def add_task():
    """Add new task to database"""
    try:
        task_name = request.form['task_name']
        description = request.form['description']
        status = request.form['status']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Changed from ? to %s
        cursor.execute(
            "INSERT INTO tasks (task_name, description, status, due_date) VALUES (%s, %s, %s, %s)",
            (task_name, description, status, due_date)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error adding task: {str(e)}", 500

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    """Update task status"""
    try:
        new_status = request.form['status']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Changed from ? to %s
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            (new_status, id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error updating task: {str(e)}", 500

@app.route('/delete/<int:id>')
def delete_task(id):
    """Delete task from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Changed from ? to %s
        cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting task: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)