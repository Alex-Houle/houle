from flask import Flask, render_template, json, current_app
from flask_login import LoginManager, current_user, login_required
from accounts.routes import accounts
from accounts.data import user_manager, user_api
from accounts.data.user_models import UserLogin
from werkzeug.local import LocalProxy

# Create Flask app
app = Flask(__name__)
# Set a secret key for sessions and security
app.config['SECRET_KEY'] = 'rnaomdkeynononeisevreguessing' # You should change this to a unique, random string

# Load config and initialize user manager and API
with open('config.json') as f:
    config = json.load(f)

db_url = config.get('DATABASE_URL')
db_db = config.get('DATABASE_DB')
db_col = config.get('DATABASE_COL')

umngr = user_manager.UserManager(db_url, db_db, db_col)
app.um = user_api.UserAPI(umngr)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# This function is automatically called by Flask-Login on every request
@login_manager.user_loader
def load_user(user_id):
    # Use current_app.um to access the user API
    user_data = current_app.um.read_by_id(user_id)
    if user_data:
        return UserLogin(user_data['id'], user_data['username'], user_data.get('admin', False))
    return None

# Register the accounts blueprint
app.register_blueprint(accounts)

@app.route('/')
def hello():
    ''' serve index.html '''
    return render_template('index.html')

if __name__ == "__main__":
    # This code is for development use only
    # The app will not run from here in a production environment
    app.run(debug=True)