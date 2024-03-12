from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_panel():
    return render_template('admin_panel.html')
