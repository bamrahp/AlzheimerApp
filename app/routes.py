from AlzheimerMain import app
from app.models import User
from flask import redirect, request, render_template,send_from_directory,flash
from fastai.vision import *
from fastai.metrics import accuracy
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
def prediction_page():
    return render_template('prediction.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == "POST":  
        try:  
            name = request.form["nm"]  
            email = request.form["email"] 
            password = request.form["password"] 
            with sqlite3.connect("arp.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into PROJECT (NAME,EMAIL,PASSWORD) values (?,?,?)",(name,email,password))  
                con.commit()  
                flash('Account Created Successfully!')
                return redirect(url_for('home'))
        except:  
            con.rollback()  
            msg = "We can not add the record to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            with sqlite3.connect("arp.db") as con:
                print("Connected Successfully")
                cur = con.cursor()
                cur.execute("Select * From PROJECT where NAME = ? and PASSWORD =?",(username,password))
                record = cur.fetchone()
                if record:
                    return render_template("prediction.html")
                else:
                    error = 'Invalid username or password. Please try again!'
                    return render_template('login.html', error = error)
        except:
            con.rollback()
            print("Error")
            return redirect(request.url,error=error)

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
                filename = secure_filename(image.filename) #Gives sanitized filename for image
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image Saved Successfully!")
                model = load_learner('./model','alzheimer.pkl')
                print("Model loaded successfully")
    
            try:
                img1 =open_image(image)
                prediction_result = model.predict(img1)
                print("After prediction")
                message = "Model prediction: {}".format(prediction_result[0])
                print('Python module executed successfully')
               # full_file = send_from_directory(app.config["IMAGE_UPLOADS"], filename )
                return render_template("result.html", user_image = filename , message=message)
                
                #return render_template('result.html',
                 #           message=message,
                  #          )
        
            except Exception as e:
                message = "Error encountered. Try another image. ErrorClass: {}, Argument: {} and Traceback details are: {}".format(e.__class__,e.args,e.__doc__)
        #final = pd.DataFrame({'A': ['Error'], 'B': [0]})
                return render_template('result.html',
                            user_image = filename,
                            message=message,
                            )
        

            