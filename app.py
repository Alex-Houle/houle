from flask import Flask, render_template, json, current_app
from flask_login import LoginManager, current_user, login_required
from accounts.routes import accounts
from accounts.data import user_manager, user_api
from accounts.data.user_models import UserLogin
from werkzeug.local import LocalProxy
import certifi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rnaomdkeynononeisevreguessing' 

with open('config.json') as f:
    config = json.load(f)

db_url = config.get('DATABASE_URL')
db_db = config.get('DATABASE_DB')
db_col = config.get('DATABASE_COL')

uri = db_url + "&tlsCAFile=" + certifi.where()
umngr = user_manager.UserManager(uri, db_db, db_col)
app.um = user_api.UserAPI(umngr)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = current_app.um.read_by_id(user_id)
    if user_data:
        return UserLogin(user_data['id'], user_data['username'], user_data.get('admin', False))
    return None

app.register_blueprint(accounts)

@app.route('/')
def hello():
    ''' serve index.html '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)