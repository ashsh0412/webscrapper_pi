from flask import Flask, render_template,request,redirect,send_file
from scrapper import get_jobs
from exporter import save_to_file
app = Flask("Tony")
Db = {}
@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report")
def report(): 
  word = request.args.get('word')
  if word:
   word = word.lower()
   exist = Db.get(word)
   if exist:
     jobs = exist
   else:
      jobs = get_jobs(word)
      Db[word] = jobs

  else:
    return redirect("/")

  return render_template("report.html", SearchingBy=word, resultsNumber = len(jobs),jobs=jobs)
@app.route("/export")
def export():
  try:
   word = request.args.get('word')
   if not word:
     raise Exception()
   word = word.lower()
   jobs = Db.get(word)
   if not jobs:
     raise Exception()
   save_to_file(jobs)
   return send_file("jobs.csv")
  except:
    return redirect("/")
  

app.run(host ="0.0.0.0")