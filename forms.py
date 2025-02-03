from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    DecimalField,
    DateField,
    TextAreaField,
    MultipleFileField,
    SubmitField,
)
from wtforms.validators import DataRequired, ValidationError, NumberRange, Regexp
from wtforms.validators import DataRequired, Email, Length

from utils import VALID_NATIONALITIES


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[DataRequired()])


class ApplicationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    date_of_birth = DateField("Date of Birth", validators=[DataRequired()])
    contact_number = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:\+91[6-9]\d{9}|[6-9]\d{9})$",
                message="Contact number must be in the format +919647846155 or 9647846155.",
            ),
        ],
    )
    address = TextAreaField("Address", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    academic_background = TextAreaField(
        "Academic Background", validators=[DataRequired()]
    )
    gpa = DecimalField(
        "GPA",
        validators=[
            DataRequired(),
            NumberRange(min=0.0, max=10.0, message="GPA must be between 0.0 and 10.0"),
        ],
    )
    documents = MultipleFileField("Documents", validators=[DataRequired()])
    submit = SubmitField("Submit Application")

    def validate_nationality(form, field):
        if field.data not in VALID_NATIONALITIES:
            raise ValidationError(
                f"Nationality must be valid. See this page /valid-nationalities for a list of valid nationalities."
            )
