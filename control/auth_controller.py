from flask import Blueprint, render_template, request, redirect, url_for, session
from entity.user_account import UserAccount

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        user = UserAccount.query.filter_by(
            username = username,
            password = password,
            role = role
        ).first()

        if user:
            if user.status == "Suspended":
                return "Account suspended"

            session["username"] = user.username
            session["role"] = user.role
            
            return redirect(url_for("auth.dashboard"))
        else:
            return "Invalid login"

    return render_template("login.html")

@auth_bp.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    return f"""
    <h1>Welcome {session['username']} ({session['role']})</h1>

    <a href="{url_for("user_admin.create_user")}"><button>Create User</button></a>
    <a href="{url_for("user_admin.view_users")}"><button>View Users</button></a>
    <a href="{url_for("fundraiser.create_activity")}")><button>Create Activity</button></a>
    <a href="{url_for("auth.logout")}"><button>Logout</button></a>
    """

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))