from flask import Blueprint, render_template, request, redirect, url_for, session
from entity.user_account import db
from entity.fundraising_activity import FundRaisingActivity

fundraiser_bp = Blueprint("fundraiser", __name__)

@fundraiser_bp.route("/create-activity", methods=["GET", "POST"])
def create_activity():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "Fund Raiser":
        return render_template(
            "error.html",
            title = "Access denied",
            message = "Only Fund Raisers are able to create activites."
        )

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        target_amount = request.form["target_amount"]
        category = request.form["category"]
        deadline = request.form["deadline"]

        new_activity = FundRaisingActivity(
            title=title,
            description=description,
            target_amount=target_amount,
            category=category,
            deadline=deadline,
            status="Active",
            fundraiser_username=session["username"]
        )
        
        db.session.add(new_activity)
        db.session.commit()

        return f"""
        <h1>New Activity successfully created.</h1>

        <a href="{url_for('fundraiser.create_activity')}">
            <button>Create another activity</button>
        </a>

        <br><br>

        <a href="{url_for('auth.dashboard')}">
            <button>Back to dashboard</button>
        </a>

        """

    return render_template("create_activity.html")