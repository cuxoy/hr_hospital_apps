from odoo import fields, models


class HospitalPatient(models.Model):
    """Hospital patient model."""
    _name = "hospital.patient"
    _inherit = ["hospital.medic.info"]
    _description = "Patient"

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="System User",
    )

    name = fields.Char(string="Patient Name", required=True)
    phone = fields.Char(string="Phone")
    personal_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Personal Doctor",
    )
    doctor_history_ids = fields.One2many(
        comodel_name="hospital.doctor.history",
        inverse_name="patient_id",
        string="Personal Doctor History",
    )
    insurance_policy_number = fields.Char(
        string="Insurance Policy Number",
        size=20,
    )
    active = fields.Boolean(default=True)

    def action_open_patient_visits(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Patient Visits",
            "res_model": "hospital.visit",
            "view_mode": "list,form,calendar,pivot,graph",
            "domain": [("patient_id", "=", self.id)],
            "context": {
                "default_patient_id": self.id,
            },
        }

    def action_create_visit(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "New Visit",
            "res_model": "hospital.visit",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_patient_id": self.id,
                "default_doctor_id": self.personal_doctor_id.id,
                "default_name": "New Visit",
                "default_state": "planned",
            },
        }