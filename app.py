from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#MYSQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#HOME PAGE LOADING
@app.route('/')
def home():
    con=mysql.connection.cursor()
    qry="SELECT * FROM fruits"
    con.execute(qry)
    res=con.fetchall()
    return render_template('index.html',datas=res)

#NEW FRUIT ADDING
@app.route('/add_fruit',methods=['GET','POST'])
def addFruit():
    if request.method=='POST':
        name=request.form['name']
        color=request.form['color']
        is_sweet=request.form['is_sweet']
        quantity=request.form['quantity']
        con=mysql.connection.cursor()
        qry="INSERT INTO fruits (NAME,COLOR,IS_SWEET,QUANTITY) VALUES (%s,%s,%s,%s)"
        con.execute(qry,[name,color,is_sweet,quantity])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template('addfruit.html')

#EDIT EXISTING DETAILS
@app.route('/edit_fruit/<string:id>',methods=['GET','POST'])
def editFruit(id):   
    if request.method=='POST':
        name=request.form['name']
        color=request.form['color']
        is_sweet=request.form['is_sweet']
        quantity=request.form['quantity']
        con=mysql.connection.cursor()
        qry="UPDATE fruits SET NAME=%s,COLOR=%s,IS_SWEET=%s,QUANTITY=%s WHERE ID=%s"
        con.execute(qry,[name,color,is_sweet,quantity,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
    qry="SELECT * FROM fruits WHERE ID=%s"
    con.execute(qry,[id])
    res=con.fetchone()
    return render_template('editfruit.html',data=res)

#DELETE FRUIT
@app.route('/delete_fruit/<string:id>',methods=['GET','POST'])
def deleteFruit(id):
    con=mysql.connection.cursor()
    qry="DELETE FROM fruits WHERE ID=%s"
    con.execute(qry,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))
if __name__ == '__main__':
    app.run(debug=True)