from odoo import api, fields, models


class HospitalDoctorHistory(models.Model):
    """Personal doctor history model."""
    _name = "hospital.doctor.history"
    _description = "Personal Doctor History"
    _order = "assignment_date desc"

    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Patient",
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Doctor",
        required=True,
    )
    assignment_date = fields.Date(
        string="Assignment Date",
        required=True,
        default=fields.Date.today,
    )
    change_date = fields.Date(string="Doctor Change Date")
    active = fields.Boolean(string="Active", default=True)

    @api.onchange("assignment_date", "change_date")
    def _onchange_dates(self):
        if self.assignment_date and self.change_date:
            if self.change_date < self.assignment_date:
                return {
                    "warning": {
                        "title": "Warning",
                        "message": "Дата зміни лікаря не може бути раніше ніж дата призначення",
                    }
                }

    @api.depends(
        "patient_id.name",
        "doctor_id.name",
        "doctor_id.category_id.name",
        "assignment_date",
    )
    def _compute_display_name(self):
        for record in self:
            patient_name = record.patient_id.name or ""
            doctor_name = record.doctor_id.name or ""
            category_name = record.doctor_id.category_id.name or ""
            assignment_date = record.assignment_date or ""

            record.display_name = (
                f"{patient_name} - "
                f"{doctor_name} "
                f"({category_name}) "
                f"{assignment_date}"
            )