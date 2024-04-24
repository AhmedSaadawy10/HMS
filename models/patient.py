from odoo import models, fields, api


class Patient(models.Model):
    _name = "hms.patient"
    _rec_name = "f_name"

    f_name = fields.Char(string="First Name", required=True)
    l_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date")
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
    age = fields.Integer(string="Age")
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctors_ids = fields.Many2many("hms.doctor")
    log_history_ids = fields.One2many("patient.log.history", "patient_id")
    state = fields.Selection([
        ('undetermined', "Undetermined"),
        ('good', "Good"),
        ('fair', "Fair"),
        ('serious', "Serious")
    ], default='good')


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
    current_date = fields.Datetime(related="patient_id.create_date")
    description = fields.Text()
