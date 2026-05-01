from flask import Flask, render_template, request, redirect, url_for, session
from entity.user_account import db, UserAccount

app = Flask(__name__, template_folder="boundary/templates")
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    if not UserAccount.query.filter_by(username="admin").first():
        user = UserAccount(username="admin", password="123", role="User Admin")
        db.session.add(user)
        db.session.commit()

@app.route('/')
def home():
    return "Flask is working!"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        user = UserAccount.query.filter_by(
            username=username,
            password=password,
            role=role
        ).first()

        if user:
            if user.status == "Suspended":
                return "Account suspended. Please contact admin."
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("dashboard"))

        else:
            return f"Invalid username, password or role"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"""
        <h1>Welcome {session["username"]} ({session["role"]})</h1>

        <a href="/create-user">
            <button>Create User</button>
        </a>

        <br><br>

        <a href="/view-users">
            <button>View Users</button>
        </a>

        <br><br>

        <a href="/logout">
            <button>Logout</button>
        </a>
        """
    else:
        return redirect(url_for("logiin"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    if "username" not in session:
        return redirect(url_for("login"))
    if session["role"] != "User Admin":
        return f"Access denied. Only User Admins can create users"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = UserAccount.query.filter_by(username=username).first()

        if existing_user:
            return f"""
            <h1>Username already exists.</h1>
            
            <a href="/create-user">
                <button>Create another user</button>
            </a>

            <br><br>

            <a href="/dashboard">
                <button>Return to Dashboard</button>
            </a>
            """

        new_user = UserAccount(
            username=username,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return f"""
        <h1>User {username} created successfully.</h1>

        <a href="/create-user">
            <button>Create another user</button>
        </a>

        <br><br>

        <a href="/dashboard">
            <button>Return to Dashboard</button>
        </a>

        
        """
    
    return render_template("create_user.html")

@app.route("/view-users")
def view_users():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if session["role"] != "User Admin":
        return "Access denied. Only User Admins can view users."
    
    users = UserAccount.query.all()

    return render_template("view_users.html", users=users)

@app.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "username" not in session:
        return redirect(url_for("login"))

    if session["role"] != "User Admin":
        return "Access denied. Only User Admin can edit users."

    user = UserAccount.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = UserAccount.query.filter_by(username=username).first()

        if existing_user and existing_user.id != user.id:
            return "Username already exists."

        user.username = username
        user.role = role

        if password:
            user.password = password
        
        db.session.commit()

        return f"""
        <h1>User updated successfully.</h1>

        <a href="/view-users">
            <button>Back to View Users</button>
        </a>

        <br><br>

        <a href="/dashboard">
            <button>Back to Dashboard</button>
        </a>
        """
    
    return render_template("edit_user.html", user=user)

@app.route("/suspend-user/<int:user_id>")
def suspend_user(user_id):
    if "username" not in session:
        return redirect(url_for("login"))
    if session["role"] != "User Admin":
        return "Access denied. Only User Admins can suspend users."
    
    user = UserAccount.query.get_or_404(user_id)

    if user.status == "Suspended":
        return "User is already suspended."
        db.session.commit()

    return redirect(url_for("view_users"))


if __name__=="__main__":
    app.run(debug=True)