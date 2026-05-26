from odoo import fields, models
from odoo.exceptions import UserError


class HospitalVisit(models.Model):
    """Patient visit model."""
    _name = "hospital.visit"
    _description = "Patient Visit"

    name = fields.Char(string="Visit Reference", required=True)

    state = fields.Selection(
        selection=[
            ("planned", "Заплановано"),
            ("done", "Завершено"),
            ("cancelled", "Скасовано"),
        ],
        string="Visit Status",
        default="planned",
        required=True,
    )

    planned_datetime = fields.Datetime(
        string="Planned Visit Date and Time",
    )
    actual_datetime = fields.Datetime(
        string="Actual Visit Date and Time",
    )

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
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Disease",
    )

    summary = fields.Html(string="Summary / Epicrisis")
    notes = fields.Text(string="Notes")
    active = fields.Boolean(default=True)

    def write(self, vals):
        protected_fields = {"planned_datetime", "actual_datetime", "doctor_id"}

        for visit in self:
            if visit.state == "done":
                if protected_fields.intersection(vals):
                    raise UserError(
                        "Не можна змінювати дату, час або лікаря візиту, що вже відбувся"
                    )

                if vals.get("active") is False:
                    raise UserError(
                        "Не можна архівувати візит, що вже відбувся"
                    )

        return super().write(vals)

    def unlink(self):
        for visit in self:
            if visit.state == "done":
                raise UserError(
                    "Не можна видаляти візит, що вже відбувся"
                )

        return super().unlink()

    def action_open_same_disease_visits(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Visits with Same Disease",
            "res_model": "hospital.visit",
            "view_mode": "list,form",
            "domain": [("disease_id", "=", self.disease_id.id)],
            "target": "current",
        }