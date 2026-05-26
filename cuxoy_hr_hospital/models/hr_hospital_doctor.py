from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    """Hospital doctor model."""
    _name = "hospital.doctor"
    _inherit = ["hospital.medic.info"]
    _description = "Doctor"

    name = fields.Char(string="Doctor Name", required=True)
    phone = fields.Char(string="Phone")
    specialty = fields.Char(string="Specialty")
    active = fields.Boolean(default=True)

    category_id = fields.Many2one(
        comodel_name="hospital.doctor.category",
        string="Category",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="System User",
    )
    is_intern = fields.Boolean(
        string="Doctor is Intern",
        compute="_compute_is_intern",
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Mentor",
        domain="[('is_intern', '=', False)]",
    )

    @api.depends("category_id")
    def _compute_is_intern(self):
        for doctor in self:
            doctor.is_intern = doctor.category_id.name == "Лікар-інтерн"

    @api.constrains("mentor_id")
    def _check_mentor_is_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError("Ментор не може бути лікарем-інтерном")

    intern_ids = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="mentor_id",
        string="Interns",
    )

    def action_create_visit(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "New Visit",
            "res_model": "hospital.visit",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_doctor_id": self.id,
                "default_name": "New Visit",
                "default_state": "planned",
            },
        }