
from faceapp.doorlock import open_door
from flask import Flask, render_template, request, redirect, url_for
import flask
from webapp.gen_frames import gen_registration_frames, gen_detection_frames, train
from webapp.memberslist import get_members
from faceapp.datagathering import register
from faceapp.sms import send_sms
from fsdb.fsdb import delete_data, get_by_id
from settings import BASE_DIR
from settings import settings
from settings import Settings
import cv2
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


class AdminUser(UserMixin):
    id = 1
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return AdminUser()


# login form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    

@app.route('/')
@login_required
def index():
    
    context = {
        "members" : get_members(),
        "settings": settings,
        "messages": [{
            "level":"info",
            "message": "Face Detection Program"
        }]
    }
    
    return render_template('index.html', **context)

@app.route('/clear_data')
@login_required
def clear_data():
    import os, shutil
    try:
        shutil.rmtree('data/')
    except:
        pass
    
    try:
        os.mkdir("data")
    except:
        pass
    
    with open('data/data.md', 'w+') as f:
        f.write("# All data stays here")
        
    # remove database
    with open('db.json', 'w+') as d:
        d.write("[]")
        
    # delete modal
    if os.path.isfile(BASE_DIR / "recognizer.yml"):
        os.remove(BASE_DIR / "recognizer.yml")
    
    return redirect(url_for('index'))


@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    import os
    # print(id)
    # delete from db
    delete_data(id)
    
    # try:
    # delete all images from data folder
    # print(os.listdir(path= BASE_DIR / 'data')[0].split(".")[0])
    for img in [ i for i in os.listdir(path= BASE_DIR / 'data') if i.split(".")[0] == str(id)]:
        os.remove(os.path.join(BASE_DIR / 'data', img))
    # except:
    #     pass
    
    if len(os.listdir(path= BASE_DIR / 'data')) > 2:
        train()
    else:
        if os.path.isfile(BASE_DIR / "recognizer.yml"):
            os.remove(BASE_DIR / "recognizer.yml")
    
    return redirect(url_for('index'))


@app.route('/settings', methods=["POST"])
@login_required
def set_settings():
    _settings = Settings(**request.form)
    _settings.save()
    members = get_members()
    return render_template('index.html', members = members, settings = settings)



@app.route('/reg_video_feed', methods=["POST"])
@login_required
def reg_video_feed():
    
    context = {
            "members" : get_members(),
            "settings": settings,
            "messages": [{
                "level":"info",
                "message": "Face Detection Program"
            }]
        }
    
    try:
        name = f"{request.form['first_name']} {request.form['last_name']}"
        print(name)
        gen_registration_frames(name)
        cv2.destroyAllWindows()
        # time.sleep(2)
        context["members"] = get_members()
        context["messages"] = [{
            "level":"info",
            "message":f"User {name} registered successfully"
        }]
        
        return render_template('index.html', **context)
    except:
        cv2.destroyAllWindows()
    
        context["messages"] = [{
            "level":"error",
            "message":f"User {name} registration failed"
        }]
        
        return render_template('index.html', **context)



@app.route('/det_video_feed')
@login_required
def det_video_feed():
    
    from settings import settings
    
    context = {
            "members" : get_members(),
            "settings": settings,
            "messages": [{
                "level":"info",
                "message": "Face Detection Program"
            }]
        }
    
    # try:
    if True:
        face = gen_detection_frames()
        
        if face is None:
            # msg = "Intruder at the door."
            # num = settings.PHONE_NUMBERS
            # send_sms(num, msg)
            # return {"message":"no face detected"}
                
            msg = "Intruder at the door."
            num = settings.PHONE_NUMBERS
        
            send_sms(num, msg)
            context["messages"] = [{
                "level":"error",
                "message":f"Intruder Detected !!!"
            }]
            
            return render_template('index.html', **context)
        
        print(face)
        cv2.destroyAllWindows()
        open_door('1')
        context["messages"] = [{
            "level":"info",
            "message":f"welcome in {face}"
        }]
        
        return render_template('index.html', **context)
    
    # except:
    else:
        
        cv2.destroyAllWindows()
    
        context["messages"] = [{
            "level":"error",
            "message":"Some error occured. Detection failed!!!"
        }]
        
        return render_template('index.html', **context)
        



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    messages = [{
                "level":"error",
                "message": "Please login"
            }]
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = AdminUser()
        
        if form.data.get('username') == user.username and form.data.get('password') == user.password:
            # user should be an instance of your `User` class
            login_user(user)

            next = flask.request.args.get('next')
            from flask import Response
            return flask.redirect(next or flask.url_for('index'))
        else:
            messages = [{
                    "level":"error",
                    "message": "Login failed"
                }]
    
    return flask.render_template('login.html', form=form, messages=messages)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')



