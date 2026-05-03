from flask import Blueprint, render_template, request, redirect, url_for, session
from entity.user_account import db, UserAccount

user_admin_bp = Blueprint("user_admin", __name__)

@user_admin_bp.route("/create-user", methods=["GET", "POST"])
def create_user():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    if session["role"] != "User Admin":
        return render_template(
            "error.html",
            title = "Access Denied",
            message = "Only User Admins can create new users."
        )
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = UserAccount.query.filter_by(username=username).first()

        if existing_user:
            return f"""
            <h1>Username already exists.</h1>
            
            <a href="{url_for('user_admin.create_user')}">
                <button>Create another user</button>
            </a>

            <br><br>

            <a href="{url_for('auth.dashboard')}">
                <button>Return to Dashboard</button>
            </a>
            """

        new_user = UserAccount(
            username=username,
            password=password,
            role=role,
            status="Active"
        )

        db.session.add(new_user)
        db.session.commit()

        return f"""
        <h1>User {username} created successfully.</h1>

        <a href="{url_for('user_admin.create_user')}">
            <button>Create another user</button>
        </a>

        <br><br>

        <a href="{url_for('auth.dashboard')}">
            <button>Return to Dashboard</button>
        </a>
        """
    
    return render_template("create_user.html")

@user_admin_bp.route("/view-users")
def view_users():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if session["role"] != "User Admin":
        return render_template(
            "error.html",
            title = "Access Denied",
            message = "Only User Admins can view users."
        )
    
    users = UserAccount.query.all()

    return render_template("view_users.html", users=users)

@user_admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "username" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "User Admin":
        return render_template(
            "error.html",
            title = "Access Denied",
            message = "Only User Admins can edit users."
        )

    user = UserAccount.query.get_or_404(user_id)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = UserAccount.query.filter_by(username=username).first()

        if existing_user and existing_user.id != user.id:
            return render_template(
                "error.html",
                title = "Username already exists.",
                message = "Please choose a different username."
            )

        user.username = username
        user.role = role

        if password:
            user.password = password
        
        db.session.commit()

        return f"""
        <h1>User updated successfully.</h1>

        <a href="{ url_for('user_admin.view_users') }">
            <button>Back to View Users</button>
        </a>

        <br><br>

        <a href="{ url_for('auth.dashboard') }">
            <button>Back to Dashboard</button>
        </a>
        """
    
    return render_template("edit_user.html", user=user)

@user_admin_bp.route("/suspend-user/<int:user_id>")
def suspend_user(user_id):
    if "username" not in session:
        return redirect(url_for("auth.login"))
    if session["role"] != "User Admin":
        return render_template(
            "error.html",
            title = "Access Denied",
            message = "Only User Admins can suspend users."
        )
    
    user = UserAccount.query.get_or_404(user_id)

    if user.status == "Suspended":
        return "User is already suspended."

    user.status = "Suspended"
    db.session.commit()

    return redirect(url_for("user_admin.view_users"))

@user_admin_bp.route("/unsuspend-user/<int:user_id>")
def unsuspend_user(user_id):
    if "username" not in session:
        return redirect(url_for("auth.login"))
    if session["role"] != "User Admin":
        return render_template(
            "error.html",
            title = "Access Denied",
            message = "Only User Admins can unsuspend users."
        )
    user = UserAccount.query.get_or_404(user_id)

    user.status = "Active"
    db.session.commit()

    return redirect(url_for("user_admin.view_users"))