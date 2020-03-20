from AlzheimerMain import app,db,bcrypt
from AlzheimerMain.models import User
from flask_login import login_user,current_user,logout_user,login_required
from flask import redirect, request, render_template,send_from_directory,flash
from fastai.vision import *
from fastai.metrics import accuracy
from werkzeug.utils import secure_filename
from AlzheimerMain import login_manager
@app.route('/')
def entry_page():
    print("Routing entry page")
    return render_template('index.html')

@app.route('/signup_form')
def signup_form():
    return render_template('signup.html')

@app.route('/login_form')
def login_form():
    return render_template('login.html')
    

@app.route('/prediction_page')
@login_required
def prediction_page():
    return render_template('prediction.html')

@login_manager.unauthorized_handler 
def unauthorized_callback():     
    return render_template("login.html")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if current_user.is_authenticated:
        return render_template("prediction.html")
    if request.method == "POST":    
        name = request.form["nm"]  
        email = request.form["email"] 
        password = request.form["password"] 
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username = name , email = email, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    return render_template("register.html")
       

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return render_template("prediction.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return render_template("prediction.html")
        else:
            error = 'Invalid username or password. Please try again!'
            return render_template('login.html', error = error)
        
    return redirect(request.url)

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/predict_class/', methods=['GET', 'POST'])
def render_message():
    if request.method=='POST':
        if request.files:
            image = request.files["image"]
            if image.filename=="":
                print("Invalid Image")
                return redirect(request.url)
            else:
                model = load_learner('./AlzheimerMain/model','alzheimer.pkl')
                print("Model loaded successfully")
    
            try:
                img1 =open_image(image)
                prediction_result = model.predict(img1)
                print("After prediction")
                message = "Model prediction: {}".format(prediction_result[0])
                print('Python module executed successfully')
               # full_file = send_from_directory(app.config["IMAGE_UPLOADS"], filename )
                return render_template("result.html" , message=message)
                
                #return render_template('result.html',
                 #           message=message,
                  #          )
        
            except Exception as e:
                message = "Error encountered. Try another image. ErrorClass: {}, Argument: {} and Traceback details are: {}".format(e.__class__,e.args,e.__doc__)
        #final = pd.DataFrame({'A': ['Error'], 'B': [0]})
                return render_template('result.html',
                            message=message,
                            )
@app.route('/logout')
def logout():
    logout_user()  
    return render_template("index.html")

            