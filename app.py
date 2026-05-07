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
    mycursor.execute("select sum(amount) from expenses where month(date1)=month(now()) and year(date1)=year(now())")
    total1=mycursor.fetchone()[0] # fetchone returns tuple like (6700,) we need only 6700. hence the '0'
    # for the chart
    mycursor.execute('Select category, sum(amount) from expenses group by category')
    graph_results= mycursor.fetchall()
    return render_template ('view.html',expenses=expenses, total1=total1, graph_results=graph_results)


@app.route('/deleteexpense', methods=['POST'])
def deleteexpense():
    mycursor=con.cursor() # no need to write if req method=post cuz alwas post hi hoga kya get?
    id=request.form['id']
    mycursor.execute('Delete from expenses where id=%s',(id,))
    con.commit()
    return redirect(url_for('viewexpense'))
    

@app.route('/editexpense',  methods=['POST'])
def editexpense():
    mycursor=con.cursor()
    id=request.form['id']
    mycursor.execute('Select * from expenses where id=%s',(id,))
    expense=mycursor.fetchone()
    return render_template ('edit.html', expense=expense)


@app.route('/updateexpense', methods=['POST'])
def updateexpense():
    mycursor=con.cursor()
    id=request.form['id']
    name=request.form["expense_name"]
    amount=request.form["expense_amount"]
    date=request.form["expense_date"]
    category=request.form["expense_category"]
    notes=request.form["expense_notes"]

    mycursor.execute('Update expenses set name=%s , amount=%s, date1=%s, category=%s, notes=%s where id=%s',(name, amount, date, category,notes,id))

    con.commit()
    return redirect(url_for('viewexpense'))

@app.route('/searchexpense')
def searchexpense():
    mycursor=con.cursor()
    searchword='%' + request.args.get('category') + '%'
    mycursor.execute('select * from expenses where name like %s or date1 like %s or category like %s or notes like %s', (searchword, searchword, searchword, searchword))
    expenses=mycursor.fetchall()
    return render_template ('view.html', expenses=expenses)



        

if __name__ == "__main__":
    app.run(debug=True)


