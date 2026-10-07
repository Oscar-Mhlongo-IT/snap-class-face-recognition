import sqlite3

# Connect to (or create) local database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create Students table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT,
    starting_year INTEGER,
    total_attendance INTEGER,
    year INTEGER,
    last_attendance_time TEXT
)
""")

# Student data
data = {
    "223379840": {
        "Name": "Clement Letshwene",
        "Course": "Information Technology",
        "Starting_Year": 2023,
        "Total_Attendance": 7,
        "Year": 3,
        "Last_attendance_time": "2025-09-13 09:54:14"
    },
    "218431600": {
        "Name": "Kagiso Aphane",
        "Course": "Information Technology",
        "Starting_Year": 2023,
        "Total_Attendance": 12,
        "Year": 3,
        "Last_attendance_time": "2025-09-11 15:00:25"
    },
    "2236781251": {
        "Name": "Naledi Maseko",
        "Course": "Information Technology",
        "Starting_Year": 2022,
        "Total_Attendance": 17,
        "Year": 4,
        "Last_attendance_time": "2025-10-03 14:54:34"
    }
}

# Insert or update each student
for student_id, value in data.items():
    cursor.execute("""
    INSERT OR REPLACE INTO Students (id, name, course, starting_year, total_attendance, year, last_attendance_time)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        value["Name"],
        value["Course"],
        value["Starting_Year"],
        value["Total_Attendance"],
        value["Year"],
        value["Last_attendance_time"]
    ))

# Save and close connection
conn.commit()
conn.close()

print("✅ Data successfully saved to SQLite database (database.db)")
