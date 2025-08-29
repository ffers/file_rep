from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import requests
from infrastructure.models import Users

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import identity_changed, AnonymousIdentity, Identity
from server_flask.permission_registred import update_roles

from dependency_injector.wiring import Provide, inject
from infrastructure.container import Container, ProjectCntrl, UserCntrl

from dataclasses import dataclass

from infrastructure.context import current_user_id


from utils import OC_logger
logger = OC_logger.oc_log("flask_login")


bp = Blueprint("auth", __name__, template_folder='templates')

def login_fail(ip, user):
    logger.warning(f"LOGIN FAILED from {ip} for user '{user}'")

@dataclass
class User:
    id: int
    name: str
    email: str
    project_id: int



# cntrl: BalanceCntrl = Provide[Container.balance_cntr]

@bp.route("/login", methods=['GET', 'POST'])
@inject
def login(
    project_cntrl: ProjectCntrl = Provide[Container.project_cntrl], 
    user_cntrl: UserCntrl = Provide[Container.user_cntrl], 
          ):
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = user_cntrl.get_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                print("login check", user.id)
                login_user(user, remember=True)     
                print("AUTHIFICATED")
                flash("Logged in!", category='success')
                # identity = Identity(user.id)
                # identity_changed.send(bp, identity=identity)
                update_roles()
                # project_id = project_cntrl.get_by_user_id(user.id)

                '''
                сначала ауз в ауз получаем дание в сешн потом before_request
                '''
                session["user_id"] = user.id
                current_user_id.set(user.id)
                print(f"check_password_hash {session.get('user_id')}")
                
                project = project_cntrl.get_by_user_id()
                if project is None:
                    return redirect(url_for("project.edit", item_id=1))
                session['active_pid'] = project.id

                return redirect(url_for('balance.index'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            login_fail(ip, email)
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



@bp.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user_response = request.form.get('g-recaptcha-response')
        recaptcha_secret_key = '6LfN0-8oAAAAAFk21kj7lvsXwz6IFK3ij3fDAe1K'
        data = {
            'secret': recaptcha_secret_key,
            'response': user_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        email_exists = Users.query.filter_by(email=email).first()
        username_exists = Users.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        elif result['success'] != True:
            flash(" Failed reCaptcha.", category='error')
        else:
            new_user = Users(email=email, username=username,
                             password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('index'))
    return render_template("signup.html", user=current_user)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(bp, identity=AnonymousIdentity())
    return redirect(url_for("index"))
