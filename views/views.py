from flask import Blueprint, render_template, redirect, url_for, request, session

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def home():
    uname_user = session.get('uname_user')
    return render_template("index.html", uname_user=uname_user)

@views_blueprint.route('/rekomendasi')
def rekomendasi():
    if 'uname_user' in session:
        return render_template("rekomendasi.html")
    else:
        return redirect(url_for('auth.login'))