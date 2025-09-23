from flask import Blueprint, redirect, render_template, request, url_for, render_template_string, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .data.user_models import UserAuth, UserLogin
from .data.user_api import UserAPI

accounts = Blueprint("accounts", __name__, template_folder="templates")

# Login route
@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # Process POST request for login
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Authenticate with the user API
    user_data = current_app.um.authenticate({'username': username, 'password': password})

    if user_data:
        # If user is found, create a UserLogin object and log them in
        user = UserLogin(user_data['id'], user_data['username'], user_data.get('admin', False))
        login_user(user)
        flash('Logged in successfully!')
        return redirect(url_for('hello'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('accounts.login'))

# Logout route
@accounts.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('hello'))

# Create user route
@accounts.route('/users/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        u = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'admin': request.form.get('admin') == 'on'
        }
        try:
            # Use current_app.um for API calls
            uid = current_app.um.create(u)
            if not uid:
                return render_template_string("""
                    {% include 'header.html' %}
                    <h1>Error: Username already taken</h1>
                """), 400
        except Exception as e:
            return render_template_string("""
                {% include 'header.html' %}
                <h1>Error: {{ message }}</h1>
            """, message=str(e)), 400

        # After creating the user, log them in
        user_data = current_app.um.read_by_id(uid)
        if user_data:
            user = UserLogin(user_data['id'], user_data['username'], user_data.get('admin', False))
            login_user(user)

        flash("User created successfully!")
        return redirect(url_for('accounts.view', username=u['username']))

    return render_template("create.html")


# List all users
@accounts.get("/users/")
@login_required
def users():
    if not current_user.admin:
        flash("You do not have permission to access this page.")
        return redirect(url_for('hello'))

    # Use current_app.um for API calls
    users_dict = current_app.um.read_all()  # returns list or dict
    if isinstance(users_dict, dict):
        users_list = users_dict.get('users', [])
    else:
        users_list = users_dict or []
    msg = request.args.get("msg")
    return render_template("users.html", users=users_list, msg=msg)


# View / update a single user
@accounts.route("/users/<username>", methods=["POST", "GET"])
@login_required
def view(username):
    # Restrict access based on current user's role or username
    if not (current_user.admin or current_user.username == username):
        flash("You do not have permission to access this user's profile.")
        return redirect(url_for('hello'))

    # Use current_app.um for API calls
    users_dict = current_app.um.read({"username": username})
    users_list = users_dict.get('users', []) if users_dict else []

    if not users_list:
        return redirect(url_for("accounts.users", msg=f"User '{username}' not found"))

    user = users_list[0]

    if request.method == "GET":
        msg = request.args.get("msg")
        return render_template("view.html", user=user, msg=msg)

    elif request.method == "POST":
        updated_data = {
            "password": request.form.get("password"),
            "admin": request.form.get("admin") == "on"
        }
        
        # Only allow admins to change the admin status
        if not current_user.admin and user.get('admin', False) != updated_data.get('admin', False):
            flash("You do not have permission to change admin status.")
            return redirect(url_for("accounts.view", username=username))

        user_id = user.get('id') or user.get('_id')
        result = current_app.um.update(user_id, updated_data)

        if result:
            return redirect(url_for("accounts.view", username=username, msg="User updated successfully"))
        else:
            return render_template_string("""
                {% include 'header.html' %}
                <h1>Error updating user</h1>
            """), 400


# Delete a single user
@accounts.post("/users/delete/<username>")
@login_required
def delete(username):
    if not current_user.admin:
        flash("You do not have permission to delete this user.")
        return redirect(url_for('accounts.users'))

    # Use current_app.um for API calls
    users_dict = current_app.um.read({"username": username})
    users_list = users_dict.get('users', []) if users_dict else []

    if not users_list:
        return redirect(url_for("accounts.users", msg=f"User '{username}' not found"))

    user_id = users_list[0].get('id') or users_list[0].get('_id')
    deleted_count = current_app.um.delete_by_id(user_id)

    if deleted_count == 0:
        return render_template_string("""
            {% include 'header.html' %}
            <h1>Error: Could not delete user</h1>
        """), 400

    return redirect(url_for("accounts.users", msg=f"User '{username}' deleted!"))


@accounts.route('/users/delete/all', methods=['POST'])
@login_required
def delete_all():
    if not current_user.admin:
        flash("You do not have permission to delete all users.")
        return redirect(url_for('accounts.users'))

    n = current_app.um.delete_all()
    return f"deleted {n} users"