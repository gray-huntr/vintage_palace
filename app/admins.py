from app import app
from flask import render_template, request, flash, redirect,session,url_for
import pymysql
from werkzeug.utils import secure_filename
import os
app.secret_key = app.config['SECRET_KEY']

def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])

@app.route("/shoe_upload", methods=['POST', 'GET'])
def shoe_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', "warning")
            return redirect("/shoe_upload")
        file = request.files['file']
        art_number = request.form['art_number']
        price = request.form['price']
        shoe_type = request.form['shoe_type']
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
                sql = ("insert into shoes(art_number,shoe_type,price,picture) "
                       "values(%s,%s,%s,%s)")
                # send to database
                cursor.execute(sql, (art_number, shoe_type, price,filename))
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