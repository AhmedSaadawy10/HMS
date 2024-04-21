from odoo import models, fields


class Patient(models.Model):
    _name = "hms.patient"
    _rec_name = "f_name"

    f_name = fields.Char(string="First Name")
    l_name = fields.Char(string="Last Name")
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




