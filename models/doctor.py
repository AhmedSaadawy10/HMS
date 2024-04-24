from odoo import models, fields


class Doctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "f_name"

    f_name = fields.Char(string="First Name")
    l_name = fields.Char(string="Last Name")
    image = fields.Binary(string="Image")

