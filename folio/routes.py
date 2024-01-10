from folio import app
from flask import redirect,render_template,Flask,request,flash,session,url_for
from folio.database import Database

databaseObj = Database()

@app.route('/home')
def home():
    return render_template('home.html',email=session['email'])

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password =request.form['password']
        
        databaseObj.cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s',(email,password))
        record = databaseObj.cursor.fetchone()
        if record:
            session['loggedin']=True
            session['email'] = record[2]
            flash('Logged in successfully','success')
            return redirect('/home')
        else:
            flash('Invalid credentials','danger')
            return redirect('/login')
        
        
    return render_template('login.html')


@app.route('/')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
        email=request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
            databaseObj.register(email,password,username,firstname,lastname)
            flash("User has been successfully registered",'success')
            return redirect('/login')
        
        else:
            flash('Password did not match','error')
            return redirect('/register')
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    
    return redirect('/login')