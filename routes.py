import os
from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
)
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
from models import User, StudentProfile, Application, Document
from forms import RegistrationForm, LoginForm, ApplicationForm
from utils import (
    save_documents,
    generate_admission_letter,
    handle_errors,
    VALID_NATIONALITIES,
)


# COMMON ROUTES
## Index Route
@app.route("/")
@handle_errors
def index():
    return render_template("index.html")


## Registration Route
@app.route("/register", methods=["GET", "POST"])
@handle_errors
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role="student")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
    return render_template("register.html", form=form)


## Login Route
@app.route("/login", methods=["GET", "POST"])
@handle_errors
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Invalid email or password.", "error")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
    return render_template("login.html", form=form)


## Logout Route
@app.route("/logout")
@handle_errors
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


@app.route("/valid-nationalities")
@handle_errors
def valid_nationalities():
    return render_template(
        "valid_nationalities.html", nationalities=VALID_NATIONALITIES
    )


@app.route("/download_admission_file/<int:application_id>/<string:file_name>")
@handle_errors
@login_required
def download_admission_file(application_id, file_name):
    application = Application.query.get_or_404(application_id)
    if (
        current_user.role == "student"
        and application.profile.user_id != current_user.id
    ):
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    if not os.path.exists(pdf_path):
        flash("Admission file not available.", "error")
        return redirect(url_for("application_detail", application_id=application_id))
    return send_from_directory(app.config["UPLOAD_FOLDER"], file_name)


# ADMIN
## Admin Dashboard
@app.route("/admin/dashboard")
@handle_errors
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))

    # Filter applications by status
    submitted_applications = Application.query.filter_by(status="Submitted").all()
    approved_applications = Application.query.filter_by(status="Approved").all()
    rejected_applications = Application.query.filter_by(status="Rejected").all()

    return render_template(
        "admin_dashboard.html",
        submitted_applications=submitted_applications,
        approved_applications=approved_applications,
        rejected_applications=rejected_applications,
    )


## Application Detail (Admin)
@app.route("/admin/application/<int:application_id>", methods=["GET", "POST"])
@handle_errors
@login_required
def application_detail_admin(application_id):
    application = Application.query.get_or_404(application_id)
    # Ensure students cannot access admin routes
    if (
        current_user.role == "student"
        and application.profile.user_id != current_user.id
    ):
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))
    print("ok-------------------------------------------")
    if request.method == "POST":
        action = request.form.get("action")
        print(request.form)  # Debugging
        if action == "approve":
            application.status = "Approved"
            application.decision_date = datetime.now()
            if generate_admission_letter(application):
                print("ok2-------------------------------------------")
                db.session.commit()
                flash("Application approved.", "success")
            else:
                flash("failed to generate pdf", "error")
        elif action == "reject":
            application.status = "Rejected"
            application.decision_date = datetime.now()
            db.session.commit()
            flash("Application rejected.", "success")
        return redirect(url_for("admin_dashboard"))
    documents = application.documents
    return render_template(
        "application_detail_admin.html",
        application=application,
        documents=documents,
    )


@app.route("/admin/application/<int:application_id>/pdf-content", methods=["GET"])
@handle_errors
@login_required
def application_detail_pdf_content(application_id):
    application = Application.query.get_or_404(application_id)
    return render_template("admission_letter.html", profile=application.profile)


# STUDENTS
## Application Form
@app.route("/apply", methods=["GET", "POST"])
@handle_errors
@login_required
def apply():
    if current_user.role != "student":
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))

    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if profile:
        existing_application = Application.query.filter_by(
            profile_id=profile.id
        ).first()
        if existing_application:
            flash("You have already submitted an application.", "info")
            return redirect(url_for("application_status"))

    form = ApplicationForm()
    if form.validate_on_submit():
        profile = StudentProfile(
            full_name=form.full_name.data,
            date_of_birth=form.date_of_birth.data,
            contact_number=form.contact_number.data,
            address=form.address.data,
            nationality=form.nationality.data,
            academic_background=form.academic_background.data,
            gpa=form.gpa.data,
            user_id=current_user.id,
        )
        db.session.add(profile)
        db.session.commit()

        application = Application(profile_id=profile.id)
        db.session.add(application)
        db.session.commit()

        # Save Documents
        files = form.documents.data
        file_names = save_documents(files, application.id)
        for filename in file_names:
            document = Document(
                document_type="Uploaded Document",
                file_name=filename,
                application_id=application.id,
            )
            db.session.add(document)
        db.session.commit()

        flash("Application submitted successfully.", "success")
        return redirect(url_for("application_status"))
    else:
        # Loop over each field's errors and flash them.
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")

    return render_template(
        "application_form.html", form=form, valid_nationalities=VALID_NATIONALITIES
    )


# Application Status
@app.route("/application_status")
@handle_errors
@login_required
def application_status():
    if current_user.role != "student":
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    application = (
        Application.query.filter_by(profile_id=profile.id).first() if profile else None
    )
    return render_template("application_status.html", application=application)


## Application Detail (Student)
@app.route("/application/<int:application_id>", methods=["GET"])
@handle_errors
@login_required
def application_detail_student(application_id):
    application = Application.query.get_or_404(application_id)
    if (
        current_user.role == "student"
        and application.profile.user_id != current_user.id
    ):
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))
    documents = application.documents
    return render_template(
        "application_detail_student.html",
        application=application,
        documents=documents,
    )


# Download Admission Letter
@app.route("/download_admission_letter/<int:application_id>")
@handle_errors
@login_required
def download_admission_letter(application_id):
    application = Application.query.get_or_404(application_id)
    if current_user.role != "student" or application.profile.user_id != current_user.id:
        flash("Unauthorized access.", "error")
        return redirect(url_for("index"))
    pdf_file = f"admission_letter_{application_id}.pdf"
    pdf_path = os.path.join(app.config["ADMISSION_LETTER_FOLDER"], pdf_file)
    if not os.path.exists(pdf_path):
        flash("Admission letter not available.", "error")
        return redirect(url_for("application_status"))
    return send_from_directory(app.config["ADMISSION_LETTER_FOLDER"], pdf_file)
