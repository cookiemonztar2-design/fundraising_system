from flask import Blueprint, render_template, request, redirect, url_for, session
from entity.user_account import db
from entity.fundraising_activity import FundRaisingActivity

fundraiser_bp = Blueprint("fundraiser", __name__)

@fundraiser_bp.route("/create-activity", methods=["GET", "POST"])
def create_activity():
    if "username" not in session:
        return redirect(url_for("auth.login"))