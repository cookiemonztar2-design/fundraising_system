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

    role = session["role"]

    if role == "User Admin":
        return render_template("user_admin_dashboard.html")
    
    elif role == "Fund Raiser":
        return render_template("fundraiser_dashboard.html")

    else:
        return render_template(
            "error.html",
            title = "Invalid username, password or role",
            message = "Please ensure particulars entered are correct."
        )


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))