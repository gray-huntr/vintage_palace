from app import app

from flask import request, session, redirect, flash,render_template
import pymysql

@app.route("/", methods=['POST','GET'])
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

@app.route("/attendant_dashboard", methods=['POST','GET'])
def attendant_dashboard():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        art_number = request.form['art_number']

        cursor.execute("select * from shoes where art_number = %s ", art_number)
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            return render_template("attendants/attendant_dashboard.html", rows=rows)
        else:
            flash("The art number does not exist try again", "info")
            return redirect("/attendant_dashboard")
    else:
        cursor.execute("select * from cart where sold_by = %s", session['attendant'])
        if cursor.rowcount == 0:
            return render_template("attendants/attendant_dashboard.html", msg="Your cart is empty")
        else:
            rows = cursor.fetchall()
            return render_template("attendants/attendant_dashboard.html", rows=rows)
