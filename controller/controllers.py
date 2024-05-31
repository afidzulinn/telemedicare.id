from flask import Blueprint, request, redirect, url_for, session, render_template
import mysql.connector
from models import Dokter, model

# Authentication controller
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nama_user = test_input(request.form['nama_user'])
        uname_user = test_input(request.form['uname_user'])
        email = test_input(request.form['email'])
        password_user = test_input(request.form['password_user'])


        cursor = conn.cursor()

        query = "INSERT INTO users (nama_user, uname_user, email, password_user) VALUES (%s, %s, %s, %s)"
        values = (nama_user, uname_user, email, password_user)
        cursor.execute(query, values)

        conn.commit()

        cursor.close()


        return redirect('/login')  # Ganti '/login' dengan halaman tujuan setelah registrasi


    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname_user = request.form['uname_user']
        password_user = request.form['password_user']

        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM users WHERE uname_user=%s AND password_user=%s"
        cursor.execute(query, (uname_user, password_user))
        result = cursor.fetchone()

        cursor.close()


        if result[0] > 0:
            session['uname_user'] = uname_user  # Menyimpan sesi login
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'


    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('uname_user', None) 
    return redirect(url_for('home'))

# Dokter controller
dokter_blueprint = Blueprint('dokter', __name__)

@app.route('/rekomendasi')
def rekomendasi():
    if 'uname_user' in session:
        return render_template("rekomendasi.html")
    else:
        return redirect(url_for('login'))

@dokter_blueprint.route('/rekomendasi', methods=['POST'])
def hasil():
    if 'uname_user' not in session:
        return redirect(url_for('login'))

    gejala1 = request.form['gejala1']
    gejala2 = request.form['gejala2']
    gejala3 = request.form['gejala3']


    features = [[gejala1, gejala2, gejala3]]


    prediction = model.predict(features)


    if prediction == "urologi":
        spesialis = "Urologi"
    elif prediction == "kulit dan kelamin":
        spesialis = "Kulit dan kelamin"
    elif prediction == "jantung dan pembuluh darah":
        spesialis = "Jantung dan pembuluh darah"
    elif prediction == "saraf dan neurolog":
        spesialis = "Saraf dan neurolog"
    elif prediction == "penyakit dalam":
        spesialis = "Penyakit dalam"
    elif prediction == "gastroenterologi":
        spesialis = "Gastroenterologi"
    elif prediction == "paru":
        spesialis = "Paru"
    elif prediction == "endokrinologi":
        spesialis = "Endokrinologi"
    else:
        spesialis = ""


    cursor = conn.cursor()


    query = "SELECT nama_dokter, gender_dokter FROM dokter WHERE spesialis=%s"
    cursor.execute(query, (spesialis,))
    result = cursor.fetchall()


    rekomendasi_dokter = []
    for row in result:
        nama_dokter = row[0]
        gender_dokter = row[1]
        dokter = Dokter(nama_dokter, gender_dokter, spesialis)
        rekomendasi_dokter.append(dokter)


    query_user = "SELECT id_user FROM users WHERE uname_user = %s"
    cursor.execute(query_user, (session['uname_user'],))
    user_result = cursor.fetchone()
    id_user = user_result[0]


    query_histori = "INSERT INTO rekam_histori (id_user, uname_user, gejala1, gejala2, gejala3, spesialis, waktu) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
    values_histori = (id_user, session['uname_user'], gejala1, gejala2, gejala3, spesialis)
    cursor.execute(query_histori, values_histori)

    conn.commit()

    cursor.close()

    return render_template('rekomendasi.html', prediction=prediction, spesialis=spesialis, rekomendasi_dokter=rekomendasi_dokter)


def test_input(data):
    data = data.strip()
    data = data.replace('\\', '\\\\')
    data = data.replace('"', '\\"')
    data = data.replace("'", "\\'")
    data = data.replace('<', '&lt;')
    data = data.replace('>', '&gt;')
    return data

# Histori controller
histori_blueprint = Blueprint('histori', __name__)

@histori_blueprint.route('/rekam_histori')
def rekam_histori():
    if 'uname_user' in session:
        cursor = conn.cursor()


        query = "SELECT waktu, gejala1, gejala2, gejala3, spesialis FROM rekam_histori WHERE uname_user = %s"
        cursor.execute(query, (session['uname_user'],))
        result = cursor.fetchall()

        cursor.close()


        return render_template("rekam_histori.html", rekam_histori=result)
    else:
        return redirect(url_for('login'))

# Chat controller
chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/chat/<dokter_id>', methods=['GET'])
def chat(dokter_id):
    if 'uname_user' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()


    query_user = "SELECT id_user FROM users WHERE uname_user = %s"
    cursor.execute(query_user, (session['uname_user'],))
    user_result = cursor.fetchone()
    id_user = user_result[0]


    query_chat = "INSERT INTO messages (id_user, id_dokter, message, waktu) VALUES (%s, %s, %s, NOW())"
    values_chat = (id_user, dokter_id, messages)
    cursor.execute(query_chat, values_chat)

    conn.commit()

    cursor.close()


    return redirect(url_for('chat', dokter_id=dokter_id))