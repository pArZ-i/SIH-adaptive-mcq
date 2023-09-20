from flask import Flask, render_template, request, redirect, url_for
import csv
import random

app = Flask(__name__)

questions = []
with open('engg_test_questions.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        questions.append(row)

score = 0  
question_num = 0

def calculate_ability(score):
  if score >= 4:
    return "High"
  elif score >= 3:   
    return "Medium"
  else:
    return "Low"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=['POST'])
def start():
    global score, question_num
    score = 0
    question_num = 0 
    return redirect(url_for('question'))

@app.route("/question")
def question():
    global question_num
    if question_num < 5:
        question_data = random.choice(questions)
        return render_template("question.html", q=question_data)
    else:
        return redirect(url_for('result'))

@app.route("/result")
def result():
    global score
    ability = calculate_ability(score)
    return render_template("result.html", score=score, ability=ability)

@app.route("/check", methods=["POST"])  
def check():
    global score, question_num 
    selected = request.form['answer']
    correct = questions[question_num]['answer'] 
    if selected == correct:
        score += 1
    question_num += 1
    return redirect(url_for('question'))

if __name__ == "__main__":
    app.run(debug=True)