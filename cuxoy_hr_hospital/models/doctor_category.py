from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    """Doctor category model."""
    _name = "hospital.doctor.category"
    _description = "Doctor Qualification"
    _order = "quality_level desc, name"

    name = fields.Char(string="Name", required=True)
    quality_level = fields.Integer(string="Quality Level", default=1)
    doctor_ids = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="category_id",
        string="Doctors",
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Qualification name must be unique!",
    )


