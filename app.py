from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("students.csv")

# Total marks
df["Total"] = df["Math"] + df["Physics"] + df["Chemistry"]

# Statistics
avg_math = round(df["Math"].mean(), 2)
avg_physics = round(df["Physics"].mean(), 2)
avg_chemistry = round(df["Chemistry"].mean(), 2)

# Topper & weak student
topper = df.loc[df["Total"].idxmax(), "Name"]
weak_student = df.loc[df["Total"].idxmin(), "Name"]

# Convert to frontend format
students = df.to_dict(orient="records")

@app.route("/")
def home():
    return render_template(
        "index.html",
        students=students,
        avg_math=avg_math,
        avg_physics=avg_physics,
        avg_chemistry=avg_chemistry,
        topper=topper,
        weak_student=weak_student
    )

if __name__ == "__main__":
    app.run(debug=True)
