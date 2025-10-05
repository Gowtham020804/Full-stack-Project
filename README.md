# Student Feedback Portal

A simple web-based feedback management system built using **Flask**, **SQLite**, and **Bootstrap**.  
The portal allows students to submit feedback about teachers, while admins can view summarized insights through interactive charts.

---

## Project Aim
To develop an easy-to-use and efficient **Student Feedback Portal** that allows collecting, managing, and analyzing student feedback for teachers in a digital, organized, and secure way.

---

## Project Objectives

### Usability & Accessibility
- Create a simple and responsive interface for students and admins.  
- Ensure smooth navigation and accessibility on both desktop and mobile devices.  

###  Data Storage & Management
- Use a database (SQLite) to securely store all user and feedback data.  
- Implement separate access roles for **students** and **admins** to maintain data integrity.  

###  Visualization & Insights
- Generate clear and interactive charts for teacher feedback analysis.  
- Help admins make data-driven decisions based on collected feedback.  

---

##  Features

1. **Student Module**  
   - Register and login securely.  
   - Submit feedback for teachers easily.  

2. **Admin Module**  
   - Register and login as admin.  
   - Add and manage teacher details.  
   - View teacher-wise feedback as interactive pie charts.  

3. **Visualization**  
   - Displays feedback distribution using **Chart.js** for better insights.  

---

##  Technologies Used

| Component | Technology |
|------------|-------------|
| **Frontend** | HTML5, CSS3, Bootstrap |
| **Backend** | Python (Flask Framework) |
| **Database** | SQLite |
| **Charts** | Chart.js |

---

##  Installation & Setup

Follow these steps to run the project locally 👇

### Step 1: Clone the repository
```bash
git clone https://github.com/Gowtham020804/Full-stack-Project.git
cd Full-stack-Project
```

### Step 2: Create a virtual environment
```bash
python -m venv venv
```

### Step 3: Activate the virtual environment
**For Windows:**
```bash
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install dependencies
```bash
pip install flask werkzeug
```

### Step 5: Run the application
```bash
python app.py
```

### Step 6: Open in your browser
```
http://127.0.0.1:5000/
```

---

## Project Structure

```
student-feedback-portal/
│
├── app.py
├── feedback.db
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   ├── student_register.html
│   ├── student_login.html
│   ├── admin_register.html
│   ├── admin_login.html
│   ├── feedback_form.html
│   ├── teacher_chart.html
│   └── navbar.html
└── README.md
```

---

##  Future Enhancements

- Add **email notifications** for feedback submission.  
- Export feedback data to **Excel or PDF**.  
- Add **teacher login** for viewing their own feedback reports.  
- Integrate **AI-based sentiment analysis** for text feedback.  

---

##  Keywords

`Flask` · `Feedback System` · `Python` · `Chart.js` · `Bootstrap` · `SQLite` · `Web Development`
