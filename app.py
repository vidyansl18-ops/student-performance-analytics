from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("students.csv")

# ---------------------------
# CALCULATIONS
# ---------------------------
df["Total"] = df["Math"] + df["Physics"] + df["Chemistry"]

avg_math = round(df["Math"].mean(), 2)
avg_physics = round(df["Physics"].mean(), 2)
avg_chemistry = round(df["Chemistry"].mean(), 2)

topper = df.loc[df["Total"].idxmax(), "Name"]
weak_student = df.loc[df["Total"].idxmin(), "Name"]

# Convert to list of dictionaries for Flask templates
students = df.to_dict(orient="records")

# Simple analytics lists (for UI section)
top_students = df.sort_values("Total", ascending=False).head(3)["Name"].tolist()
weak_students = df.sort_values("Total", ascending=True).head(3)["Name"].tolist()

# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        students=students,
        avg_math=avg_math,
        avg_physics=avg_physics,
        avg_chemistry=avg_chemistry,
        topper=topper,
        weak_student=weak_student,
        top_students=top_students,
        weak_students=weak_students
    )

@app.route("/student/<name>")
def student(name):
    student_data = df[df["Name"] == name].to_dict(orient="records")
    return render_template("student.html", name=name, data=student_data[0])

@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        avg_math=avg_math,
        avg_physics=avg_physics,
        avg_chemistry=avg_chemistry,
        top_students=top_students,
        weak_students=weak_students
    )

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
