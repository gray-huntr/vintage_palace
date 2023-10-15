from app import app
from flask import render_template, request, flash, redirect,session,url_for
import pymysql
from werkzeug.utils import secure_filename
import os
app.secret_key = app.config['SECRET_KEY']

def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])

@app.route("/admin_signup", methods=['POST', 'GET'])
def admin_signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        repeat_pass = request.form['repeat_pass']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from admins where email = %s ", email)
        if cursor.rowcount > 0:
            flash("Email already exists", "warning")
            return render_template('admins/admin_signup.html')
        else:
            # if there is no existing account, check whether the two passwords match
            if password == repeat_pass:
                #     insert the records to the users tables
                cursor.execute(
                    "insert into admins(name,email,number,password) values (%s,%s,%s,%s)",
                    (name, email, phone, password))
                # save records
                conn.commit()
                flash("Admin signed up successfully", "success")
                return render_template('admins/admin_signup.html', )
                # if passwords do not match display the following message
            elif password != repeat_pass:
                flash("Passwords do not match", "danger")
                return render_template('admins/admin_signup.html')
            else:
                flash("Error occurred please try again", "info")
                return render_template('admins/admin_signup.html')
    else:
        return render_template('admins/admin_signup.html')

@app.route("/admin_login", methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        # pick the record from the clients table
        cursor = conn.cursor()
        cursor.execute("select * from admins where email =%s and password=%s", (email, password))
        # if cursor.rowcount == 1:
        if cursor.rowcount == 1:
            session['admin'] = email
            return redirect('/shoe_upload')
        elif cursor.rowcount == 0:
            flash("User does not exist or incorrect password", "warning")
            return render_template('admins/admin_login.html')
    return render_template('admins/admin_login.html')
@app.route("/shoe_upload", methods=['POST', 'GET'])
def shoe_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', "warning")
            return redirect("/shoe_upload")
        file = request.files['file']
        name = request.form['name']
        price = request.form['price']
        shoe_type = request.form['shoe_type']
        stock = request.form['stock']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'warning')
            return redirect(url_for('.shoe_upload'))
        # If all checks are passed, the app proceeds to submit the file
        elif file and allowed_file(file.filename):
            try:
                #  connect to database
                conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                       password=app.config["DB_PASSWORD"],
                                       database=app.config["DB_NAME"])
                cursor = conn.cursor()

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                sql = ("insert into shoes(art_number,shoe_type,shoe_name,price,stock,picture)"
                       "values(%s,%s,%s,%s,%s,%s)")
                cursor.execute("select * from shoes order by product_number desc limit 1")
                rows = cursor.fetchall()
                art_number = 0
                for row in rows:
                    s_id = row[0]+1
                    art_number = "S"+str(s_id)

                # send to database
                cursor.execute(sql, (art_number, shoe_type,name, price,stock,filename))
                # Save to database
                conn.commit()
                flash("Uploaded Successfully", "success")
                return redirect('/shoe_upload')
                # if error occurs, display error message
            except Exception as e:
                flash("Upload Failed", "danger")
                print(f"An exception occurred: {str(e)}")
                return redirect('/shoe_upload')
        # If file is not on allowed list, display error message
        else:
            flash("Uploaded File Not Allowed", "warning")
            return redirect('/shoe_upload')
    else:
        return render_template('admins/shoe_upload.html')

@app.route("/attendants_signup", methods=['POST', 'GET'])
def attendants_signup():
    if request.method == 'POST':
        attendant_id = request.form['attendant_id']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from attendants where email = %s or attendant_id = %s ", (email, attendant_id))
        if cursor.rowcount > 0:
            flash("Email or employee id already exists, try another one", "warning")
            return render_template('admins/attendants_signup.html')
        elif cursor.rowcount == 0:
            # if there is no existing account, proceed
            #     insert the records to the attendants tables
            cursor.execute(
                "insert into attendants(attendant_id,name,phone,email) values (%s,%s,%s,%s)",
                (attendant_id, name, phone, email))
            # save records
            conn.commit()
            flash("attendant signed up successfully", "success")
            return render_template('admins/attendants_signup.html', )
        else:
            flash("Error occurred please try again", "info")
            return render_template('admins/attendants_signup.html')
    else:
        return render_template('admins/attendants_signup.html')

@app.route("/sales_search", methods=['POST','GET'])
def sales_search():
    if 'admin' in session:
        if request.method == 'POST':
            query = request.form['search']
            #  connect to database
            conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                   password=app.config["DB_PASSWORD"],
                                   database=app.config["DB_NAME"])
            cursor = conn.cursor()
            cursor.execute("select * from sales_records where sale_id = %s or name = %s or attendant_id = %s group by sale_id",
                           (query,query,query))
            if cursor.rowcount == 0:
                flash("The are no records for that id or name", "danger")
                return redirect("/sales")
            elif cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("sales.html", rows=rows)
            else:
                flash("Error occurred try again", "Warning")
                return redirect("/sales")

@app.route("/shoe_records", methods=['POST','GET'])
def shoe_records():
    if 'admin' in session:
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            art_number = request.form['art_number']
            s_type = request.form['s_type']
            s_name = request.form['s_name']
            price = request.form['price']
            stock = request.form['stock']
            status = request.form['status']

            cursor.execute("update shoes set shoe_type = %s, shoe_name = %s, price = %s, stock =%s, status = %s where art_number = %s",
                           (s_type,s_name,price,stock,status,art_number))
            conn.commit()
            flash("Record updated successfully", "success")
            return redirect("/shoe_records")
        else:
            cursor.execute("select * from shoes")
            if cursor.rowcount == 0:
                flash("There are no Records available", "Danger")
                return render_template("admins/shoe_records.html")
            else:
                rows = cursor.fetchall()
                return render_template("admins/shoe_records.html", rows=rows)

@app.route("/attendants_records", methods=['POST','GET'])
def attendants_records():
    if 'admin' in session:
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            attendant_id = request.form['attendant_id']
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            status = request.form['status']

            cursor.execute("update attendants set name = %s, phone = %s, email =%s, status = %s where attendant_id = %s",
                           (name,phone,email,status,attendant_id))
            conn.commit()
            flash("Record updated successfully", "success")
            return redirect("/attendants_records")
        else:
            cursor.execute("select * from attendants")
            if cursor.rowcount == 0:
                flash("There are no Records available", "Danger")
                return render_template("admins/attendants_records.html")
            else:
                rows = cursor.fetchall()
                return render_template("admins/attendants_records.html", rows=rows)
