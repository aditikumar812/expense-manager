import mysql.connector as my
from flask import Flask , render_template, request, redirect, url_for
app=Flask(__name__)

#--database--
con=my.connect(host='localhost', user='root', password='Aditi@Mona123', database='expense_manager')
#dont add cursor here. each function gets its own

@app.route("/")#your comment
def home():
    return 'Hello World'

@app.route('/addexpense', methods=['GET', 'POST'])
def addexpense():
    if request.method=="POST":
        name=request.form["expense_name"]
        amount=request.form["expense_amount"]
        date=request.form["expense_date"]
        category=request.form["expense_category"]
        notes=request.form["expense_notes"]
        
    
        #mysql 
        mycursor=con.cursor()
        mycursor.execute("Insert into expenses (name, amount, date1, category, notes) values (%s, %s, %s, %s, %s)",(name, amount, date, category, notes))
        con.commit()


        return redirect(url_for('home'))
    else:
        return render_template('add.html')
    

@app.route('/viewexpense')# why didnt we write methods? cuz we need only 'get' to view and 'get' is by default
def viewexpense():
    mycursor=con.cursor()
    mycursor.execute('Select * from expenses;')
    expenses=mycursor.fetchall()
    return render_template ('view.html',expenses=expenses)


@app.route('/deleteexpense', methods=['GET', 'POST'])
def deleteexpense():
    mycursor=con.cursor() # no need to write if req method=post cuz alwas post hi hoga kya get?
    id=request.form['id']
    mycursor.execute('Delete from expenses where id=%s',(id,))
    con.commit()
    return redirect(url_for('viewexpense'))
    


        
        

if __name__ == "__main__":
    app.run(debug=True)


