from app import app

from flask import request, session, redirect, flash,render_template,make_response
import pymysql
from fpdf import FPDF, XPos, YPos


@app.route("/", methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        attendant_id = request.form['attendant_id']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("Select * from attendants where attendant_id = %s and status = %s ", (attendant_id, "Active"))
        if cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                session['attendant'] = row[1]
                return redirect("/attendant_dashboard")
        else:
            flash("The code is invalid or your account is blocked", "warning")
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
    cursor.execute("select attendant_id from attendants where name = %s ", session['attendant'])
    a_id = cursor.fetchone()
    if request.method == 'POST':
        if action == 'add':
            art_number = request.form['art_number']
            shoe_name = request.form['name']
            price = int(request.form['price'])
            quantity = int(request.form['quantity'])
            total = price * quantity

            cursor.execute("insert into cart(art_number, shoe_name, price,quantity,total, sold_by, attendant_id) "
                           "values (%s,%s,%s,%s,%s,%s,%s)", (art_number,shoe_name,price,quantity,total,session['attendant'],a_id))
            conn.commit()
            flash("Product added to cart successfully", "success")
            return redirect("/attendant_dashboard")
        elif action == 'remove':
            cart_id = request.form['cart_id']

            cursor.execute("delete from cart where cart_id = %s and sold_by = %s", (cart_id,session['attendant']))
            conn.commit()
            flash("Item removed successfully", "success")
            return redirect("/attendant_dashboard")
    else:
        flash("Error occurred try again", "warning")
        return redirect("/attendant_dashboard")


@app.route("/checkout")
def checkout():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from cart where sold_by = %s ", session['attendant'])
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        for row in rows:
            art_number = row[1]
            name = row[2]
            price = row[3]
            quantity = row[4]
            total = row[5]
            a_id = row[7]

            # Read the sales id file
            with open("app/sale_id.txt", "r") as file:
                sale_id = int(file.read())
            cursor.execute("insert into sales_records( sale_id, art_number, name, price, quantity, total, sold_by,attendant_id) "
                           "values(%s,%s,%s,%s,%s,%s,%s,%s)",
                           (sale_id, art_number,name,price,quantity,total,session['attendant'],a_id))
            conn.commit()
            cursor.execute("select * from shoes where art_number = %s" , art_number)
            shoe = cursor.fetchall()
            for rows in shoe:
                amount_sold = rows[5] + quantity
                stock = rows[6] - quantity
                cursor.execute("update shoes set amount_sold = %s, stock = %s where art_number = %s", (amount_sold,stock,art_number))
                conn.commit()
        cursor.execute("delete from cart where sold_by = %s ", session['attendant'])
        conn.commit()
        # Increase sale id
        sale_id += 1
        # save it to file
        with open("app/sale_id.txt", "w") as file:
            file.write(str(sale_id))
        flash("Order completed successfully", "success")
        return redirect("/attendant_dashboard")

@app.route("/sales")
def sales():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if 'attendant' in session:
        cursor.execute("select * from sales_records where sold_by = %s group by  sale_id order by sale_id desc",
                       session['attendant'])
        if cursor.rowcount == 0:
            flash("You don't have any complete sales", "info")
            return render_template("attendants/sales.html")
        else:
            rows=cursor.fetchall()
            return render_template("attendants/sales.html", rows=rows)
    else:
        flash("Please log in first", "warning")
        return redirect("/")

@app.route("/view/<sale_id>")
def view(sale_id):
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from sales_records where sale_id = %s", sale_id)
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        total = 0
        for row in rows:
            total = row[6] + total
        return render_template("attendants/sale_view.html", rows=rows, total=total)
    elif cursor.rowcount == 0:
        flash("There is no sale order with the given ID")
        return redirect("/sales")
    else:
        flash("Error occurred try again", "warning")
        return redirect("/sales")

@app.route("/receipt/<sale_id>")
def receipt(sale_id):
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from sales_records where sale_id = %s ", sale_id)
    rows = cursor.fetchall()

    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 20)
            # title
            self.cell(0, 10, "VINTAGE PALACE", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.cell(0, 0, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = PDF('P', 'mm', (145,200))

    # Add a page
    pdf.add_page()

    # specify font
    # fonts ('times', 'courier', 'helvetica', 'symbol', 'zpfdingbats')
    # 'B' (bold), 'U' (underline), 'I' (italics), '' (regular), combination (i.e., ('BU'))
    pdf.set_font('times', '', 16)
    # pdf.set_text_color(220,50,50)
    # Add text
    # w = width
    # h = height
    # txt = your text
    # border (0 False; 1 True - add border around cell)
    pdf.cell(120, 10, f'Order number: {sale_id}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(55, 10, 'Product Name')
    pdf.cell(20, 10, 'Cost')
    pdf.cell(25, 10, 'Qtty')
    pdf.cell(35, 10, 'Total', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    total_sum = 0
    for row in rows:
        pdf.cell(55, 10, f'{row[3]}')
        pdf.cell(25, 10, f'{row[4]}')
        pdf.cell(20, 10, f'{row[5]}')
        pdf.cell(35, 10, f'{row[6]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(110, 0, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        total_sum = total_sum + row[6]

    pdf.cell(10, 15, f'Total: {total_sum}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # pdf.output(f"{sale_id}.pdf")
    output = bytes(pdf.output(dest='S'))
# enabling output to be downloadable
    response = make_response(output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={sale_id}.pdf'
    return response

@app.route("/logout_attendants")
def logout_attendants():
    session.pop('attendant', None)
    return redirect("/")

