from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change_this_to_a_secure_random_string"
DB_PATH = 'feedback.db'

# ---------- DB setup ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            instructor TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comments TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- routes ----------
@app.route('/')
def index():
    return render_template('index.html')

# Student register/login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        if not name or not email or not password:
            flash("All fields required.", "danger")
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO students (name,email,password) VALUES (?, ?, ?)", (name, email, hashed))
            conn.commit()
            conn.close()
            flash("Registration successful. Please sign in.", "success")
            return redirect(url_for('student_login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/student-login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','').strip()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['student_logged_in'] = True
            session['student_name'] = user['name']
            session['student_email'] = user['email']
            flash(f"Welcome {user['name']}!", "success")
            return redirect(url_for('feedback_form'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('student_login'))
    return render_template('student_login.html')

@app.route('/student-logout')
def student_logout():
    session.pop('student_logged_in', None)
    session.pop('student_name', None)
    session.pop('student_email', None)
    flash("Signed out.", "info")
    return redirect(url_for('index'))

# Feedback form (uses teachers list)
@app.route('/feedback', methods=['GET','POST'])
def feedback_form():
    if not session.get('student_logged_in'):
        flash("Please sign in to give feedback.", "warning")
        return redirect(url_for('student_login'))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM teachers ORDER BY name")
    teachers = cur.fetchall()  # list of (id,name)
    conn.close()

    if request.method == 'POST':
        name = session.get('student_name')
        email = session.get('student_email')
        course = request.form['course'].strip()
        # instructor might be a teacher id (select) or 'other' text
        instructor_choice = request.form.get('instructor_select')
        instructor_text = request.form.get('instructor_text','').strip()
        if instructor_choice == 'other':
            instructor = instructor_text or "Unknown"
        else:
            # instructor_choice holds teacher id as string
            try:
                tid = int(instructor_choice)
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT name FROM teachers WHERE id = ?", (tid,))
                row = cur.fetchone()
                conn.close()
                instructor = row[0] if row else instructor_text or "Unknown"
            except:
                instructor = instructor_text or "Unknown"

        rating = int(request.form['rating'])
        comments = request.form['comments'].strip()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO feedback (name,email,course,instructor,rating,comments)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, course, instructor, rating, comments))
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))

    return render_template('feedback.html', teachers=teachers)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Admin registration & login
@app.route('/admin-register', methods=['GET','POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash("Enter username & password.", "danger")
            return redirect(url_for('admin_register'))
        hashed = generate_password_hash(password)
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO admins (username,password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            conn.close()
            flash("Admin registered. Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
            return redirect(url_for('admin_register'))
    return render_template('admin_register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins WHERE username = ?", (username,))
        admin = cur.fetchone()
        conn.close()
        if admin and check_password_hash(admin['password'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin['username']
            flash("Admin signed in.", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Signed out.", "info")
    return redirect(url_for('index'))

# Admin dashboard - list teachers (admin-only)
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Admin access only.", "warning")
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, department FROM teachers ORDER BY name")
    teachers = cur.fetchall()
    conn.close()
    return render_template('admin.html', teachers=teachers)

# Add teacher (admin-only)
@app.route('/add-teacher', methods=['GET','POST'])
def add_teacher():
    if not session.get('admin_logged_in'):
        flash("Admin access only.", "warning")
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        department = request.form['department'].strip()
        if not name or not department:
            flash("All fields required.", "danger")
            return redirect(url_for('add_teacher'))
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO teachers (name, department) VALUES (?, ?)", (name, department))
        conn.commit()
        conn.close()
        flash("Teacher added.", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('add_teacher.html')

# Teacher chart (admin-only) by teacher id to avoid url-encoding/space bugs
@app.route('/teacher/<int:teacher_id>')
def teacher_feedback(teacher_id):
    if not session.get('admin_logged_in'):
        flash("Admin access only.", "warning")
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM teachers WHERE id = ?", (teacher_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        flash("Teacher not found.", "danger")
        return redirect(url_for('admin_dashboard'))
    teacher_name = row[0]
    cur.execute("SELECT rating, COUNT(*) FROM feedback WHERE instructor = ? GROUP BY rating", (teacher_name,))
    data = cur.fetchall()  # list of (rating,count)
    conn.close()

    labels = [str(r[0]) for r in data]
    values = [r[1] for r in data]

    return render_template('teacher_chart.html', teacher_name=teacher_name, labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)
