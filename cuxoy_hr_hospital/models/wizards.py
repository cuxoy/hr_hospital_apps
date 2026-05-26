from odoo import api, fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = "mass.reassign.doctor.wizard"
    _description = "Mass Reassign Doctor Wizard"

    new_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="New Doctor",
        required=True,
    )
    change_date = fields.Date(
        string="Change Date",
        default=fields.Date.today,
    )

    def action_reassign_doctor(self):
        active_ids = self.env.context.get("active_ids", [])
        patients = self.env["hospital.patient"].browse(active_ids)

        for patient in patients:
            old_doctor = patient.personal_doctor_id

            if old_doctor:
                old_history = self.env["hospital.doctor.history"].search([
                    ("patient_id", "=", patient.id),
                    ("doctor_id", "=", old_doctor.id),
                    ("active", "=", True),
                ], limit=1)

                if old_history:
                    old_history.write({
                        "change_date": self.change_date,
                        "active": False,
                    })

            patient.write({
                "personal_doctor_id": self.new_doctor_id.id,
            })

            self.env["hospital.doctor.history"].create({
                "patient_id": patient.id,
                "doctor_id": self.new_doctor_id.id,
                "assignment_date": self.change_date,
                "active": True,
            })

        return {"type": "ir.actions.act_window_close"}

class VisitReportWizard(models.TransientModel):
    _name = "visit.report.wizard"
    _description = "Visit Report Wizard"

    doctor_ids = fields.Many2many(
        comodel_name="hospital.doctor",
        string="Doctors",
    )
    patient_ids = fields.Many2many(
        comodel_name="hospital.patient",
        string="Patients",
    )
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    only_done = fields.Boolean(string="Only Done Visits")
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Disease",
    )

    def action_show_visits(self):
        domain = []

        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))

        if self.patient_ids:
            domain.append(("patient_id", "in", self.patient_ids.ids))

        if self.date_from:
            domain.append(("planned_datetime", ">=", self.date_from))

        if self.date_to:
            domain.append(("planned_datetime", "<=", self.date_to))

        if self.only_done:
            domain.append(("state", "=", "done"))

        if self.disease_id:
            domain.append(("disease_id", "=", self.disease_id.id))

        return {
            "type": "ir.actions.act_window",
            "name": "Visit Report",
            "res_model": "hospital.visit",
            "view_mode": "list,form",
            "domain": domain,
            "target": "current",
        }

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids", [])

        if active_model == "hospital.patient":
            res["patient_ids"] = [(6, 0, active_ids)]

        if active_model == "hospital.doctor":
            res["doctor_ids"] = [(6, 0, active_ids)]

        return res


class DiseaseMonthlyReportWizard(models.TransientModel):
    _name = "disease.monthly.report.wizard"
    _description = "Disease Monthly Report Wizard"

    doctor_ids = fields.Many2many(
        comodel_name="hospital.doctor",
        string="Doctors",
    )
    disease_ids = fields.Many2many(
        comodel_name="hospital.disease",
        string="Diseases",
    )
    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To")

    def action_show_report(self):
        domain = []

        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(("disease_id", "in", self.disease_ids.ids))

        if self.date_from:
            domain.append(("planned_datetime", ">=", self.date_from))

        if self.date_to:
            domain.append(("planned_datetime", "<=", self.date_to))

        return {
            "type": "ir.actions.act_window",
            "name": "Disease Report",
            "res_model": "hospital.visit",
            "view_mode": "list,form,pivot,graph",
            "domain": domain,
            "context": {
                "group_by": "disease_id",
            },
            "target": "current",
        }