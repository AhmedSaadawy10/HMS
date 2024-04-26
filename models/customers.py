from odoo import models, fields, api, exceptions


class CustomersInherit(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"

    related_patient_id = fields.Many2one("hms.patient")
    vat = fields.Char(required=True)

    """
    Checks for duplicate emails in the current model.

    This function is a constrain that is triggered whenever the 'email' field is modified.
    It checks if the email entered in the current record 
    already exists in the 'email' field of the related patient record.
    If a duplicate email is found, it raises a ValidationError.

    Parameters:
        self (Recordset): The current recordset.

    Raises:
        ValidationError: If a duplicate email is found.

    Returns:
    """

    @api.constrains('email')
    def _check_duplicate_email(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email == partner.email:
                raise exceptions.ValidationError('Email already exists in the patient model.')

    # ➢ Prevent users to delete any customer linked to a patient
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise exceptions.UserError("You cannot delete any customer linked to a patient")
        super().unlink()

