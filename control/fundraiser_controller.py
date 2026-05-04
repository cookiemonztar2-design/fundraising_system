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
            message = "Only Fund Raisers are able to create activities."
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

@fundraiser_bp.route("/view-activities")
def view_activities():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if session["role"] != "Fund Raiser":
        return render_template(
            "error.html",
            title = "Access denied",
            message = "Only Fund Raisers are allowed to view the activites."
        )
    
    search = request.args.get("search")

    query = FundRaisingActivity.query.filter_by(
        fundraiser_username=session["username"]
    )

    if search:
        query = query.filter(
            (FundRaisingActivity.title.contains(search)) |
            (FundRaisingActivity.category.contains(search))
        )

    activities = query.all()

    return render_template("view_activities.html", activities=activities)

@fundraiser_bp.route("/edit-activity/<int:activity_id>", methods=["GET", "POST"])
def edit_activity(activity_id):
    if "username" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "Fund Raiser":
        return render_template(
            "error.html",
            title = "Access denied",
            message = "Only Fund Raisers are able to edit activities."
        )

    activity = FundRaisingActivity.query.get_or_404(activity_id)

    if activity.fundraiser_username != session["username"]:
        return render_template(
            "error.html",
            title = "Access denied",
            message = "You can only edit your own activities."
        )

    if request.method == "POST":
        activity.title = request.form["title"]
        activity.description = request.form["description"]
        activity.target_amount = request.form["target_amount"]
        activity.categroy = request.form["category"]
        activity.deadline = request.form["deadline"]

        db.session.commit()

        return f"""
        <h1>Activity updated successfully.</h1>

        <a href="{url_for('fundraiser.view_activities')}">
            <button>Back to Activities</button>
        </a>

        <br><br>

        <a href="{url_for('auth.dashboard')}">
            <button>Back to Dashboard</button>
        </a>
        """

    return render_template("edit_activity.html", activity=activity)

@fundraiser_bp.route("/delete-activity/<int:activity_id>")
def delete_activity(activity_id):
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if session["role"] != "Fund Raiser":
        return render_template(
            "error.html",
            title = "Access denied",
            message = "Only Fund Raisers can delete activities"
        )

    activity = FundRaisingActivity.query.get_or_404(activity_id)

    if activity.fundraiser_username != session["username"]:
        return render_template(
            "error.html",
            title = "Access denied",
            message = "You can only delete your own activities."
        )

    db.session.delete(activity)
    db.session.commit()

    return redirect(url_for("fundraiser.view_activities"))
