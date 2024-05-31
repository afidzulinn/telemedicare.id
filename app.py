from flask import Flask, session
from views import views
from controllers import auth_controller, dokter_controller, histori_controller, chat_controller

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your-secret-key'

app.register_blueprint(views.views_blueprint)
app.register_blueprint(auth_controller.auth_blueprint)
app.register_blueprint(dokter_controller.dokter_blueprint)
app.register_blueprint(histori_controller.histori_blueprint)
app.register_blueprint(chat_controller.chat_blueprint)

if __name__ == '__main__':
    app.run(debug=True)