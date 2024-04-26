from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
import re
from datetime import date


class Patient(models.Model):
    _name = "hms.patient"
    _rec_name = "f_name"

    f_name = fields.Char(string="First Name", required=True)
    l_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email")
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", compute="compute_age")
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection(
        [('a+', 'A+'),
         ('a-', 'A-'),
         ('b+', 'B+'),
         ('b-', 'B-'),
         ('ab+', 'AB+'),
         ('ab-', 'AB-'),
         ('O+', 'O+'),
         ('O-', 'O-')]
    )
    pcr = fields.Boolean(string="Pcr")
    image = fields.Binary(string="Image")
    address = fields.Text(string="Address")
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctors_ids = fields.Many2many("hms.doctor")
    log_history_ids = fields.One2many("patient.log.history", "patient_id")
    state = fields.Selection([
        ('undetermined', "Undetermined"),
        ('good', "Good"),
        ('fair', "Fair"),
        ('serious', "Serious")
    ], default='undetermined')

    _sql_constraints = [
        ("Duplicate_Email", "UNIQUE(email)", "Email Already Exists"),
    ]

    @api.depends("birth_date")
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = False

    @api.constrains("email")
    def check_email_valid(self):
        # check Email validation
        for rec in self:
            if rec.email:
                email_validation = re.match(r"^[A-z0-9]+@[A-z0-9]+\.(com|net|org|info|gov)$", rec.email)
                if not email_validation:
                    raise exceptions.ValidationError("Invalid email address")

    def undetermined(self):
        self.state = 'undetermined'
        self.env['patient.log.history'].create({
            'patient_id': self._uid,
            'current_date': date.today(),
            'description': f'state changed to {self.state}',
        })

    def good(self):
        self.state = 'good'
        self.env['patient.log.history'].create({
            'patient_id': self._uid,
            'current_date': date.today(),
            'description': f'state changed to {self.state}',
        })

    def fair(self):
        self.state = 'fair'
        self.env['patient.log.history'].create({
            'patient_id': self._uid,
            'current_date': date.today(),
            'description': f'state changed to {self.state}',
        })

    def serious(self):
        self.state = 'serious'
        self.env['patient.log.history'].create({
            'patient_id': self._uid,
            'current_date': date.today(),
            'description': f'state changed to {self.state}',
        })

    """
    This function is triggered when the 'age' field is changed. 
    It checks if the age is less than 30, sets 'pcr' to True, and returns a warning notification if the condition is met. 
    If age is 30 or greater, 'pcr' is set to False.
    """


@api.onchange("age")
def on_change_age(self):
    if self.age and self.age < 30:
        self.pcr = True
        return {
            "warning": {
                "title": "Note",
                "message": "The pcr is Checked because the age is less than 30",
                "type": "Notification"
            }
        }
    else:
        self.pcr = False


class PatientLogHistory(models.Model):
    _name = "patient.log.history"

    patient_id = fields.Many2one("hms.patient", readonly=True)
    current_date = fields.Datetime()
    description = fields.Text()
