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
        session.pop("cart", None)
        art_number = request.form['art_number']

        cursor.execute("select * from shoes where art_number = %s ", art_number)
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            return render_template("attendants/attendant_dashboard.html", rows=rows)
        else:
            flash("The art number does not exist try again", "info")
            return redirect("/attendant_dashboard")
    else:
        session['cart'] = True
        cursor.execute("select * from cart where sold_by = %s", session['attendant'])
        if cursor.rowcount == 0:
            return render_template("attendants/attendant_dashboard.html", msg="Your cart is empty")
        else:
            rows = cursor.fetchall()
            total = 0
            for row in rows:
                total = row[5] + total
            return render_template("attendants/attendant_dashboard.html", rows=rows, total=total)

@app.route("/cart/<action>", methods=['POST','GET'])
def cart(action):
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        if action == 'add':
            art_number = request.form['art_number']
            shoe_name = request.form['name']
            price = int(request.form['price'])
            quantity = int(request.form['quantity'])
            total = price * quantity

            cursor.execute("insert into cart(art_number, shoe_name, price,quantity,total, sold_by) "
                           "values (%s,%s,%s,%s,%s,%s)", (art_number,shoe_name,price,quantity,total,session['attendant']))
            conn.commit()
            flash("Product added to cart successfully", "success")
            return redirect("/attendant_dashboard")

    else:
        flash("Error occurred try again", "warning")
        return redirect("/attendant_dashboard")



