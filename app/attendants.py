from app import app

from flask import request, session, redirect, flash,render_template
import pymysql

@app.route("/")
def signin():
    if request.method == 'POST':
        attendant_id = request.form['attendant_id']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("Select * from attendants where attendant_id = %s ", attendant_id)
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                session['attendant'] = row[1]
                return redirect("/attendant_dashboard")
        else:
            flash("The code is invalid", "warning")
            return redirect("/")
    else:
        return render_template("attendants/index.html")



