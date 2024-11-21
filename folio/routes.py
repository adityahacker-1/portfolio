from folio import app
from flask import redirect,render_template,Flask,request,flash,session,url_for
from folio.database import Database

databaseObj = Database()

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html', email=session['email'])
    else:
        return redirect('/login')

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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        confirm_password = request.form.get('confirm_password')

        # Check if the email is already registered
        databaseObj.cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
        existing_email = databaseObj.cursor.fetchone()

        if existing_email:
            flash('Email is already registered', 'danger')
            return redirect('/register')

        # Check if the username is already taken
        databaseObj.cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        existing_username = databaseObj.cursor.fetchone()

        if existing_username:
            flash('Username is already taken', 'danger')
            return redirect('/register')

        # Check if passwords match
        if password == confirm_password:
            try:
                # Register the user
                databaseObj.register(email, password, username, firstname, lastname)
                flash("User has been successfully registered", 'success')
                return redirect('/login')
            except Exception as e:
                # Log error and flash a message
                print(f"Error during registration: {e}")
                flash('An error occurred during registration. Please try again.', 'danger')
                return redirect('/register')
        else:
            flash('Passwords did not match', 'danger')
            return redirect('/register')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    
    return redirect('/login')