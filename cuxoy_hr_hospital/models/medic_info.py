from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    _name = "hospital.medic.info"
    _description = "Medical Information"

    blood_group = fields.Selection(
        selection=[
            ("o_pos", "O(I) Rh+"),
            ("o_neg", "O(I) Rh-"),
            ("a_pos", "A(II) Rh+"),
            ("a_neg", "A(II) Rh-"),
            ("b_pos", "B(III) Rh+"),
            ("b_neg", "B(III) Rh-"),
            ("ab_pos", "AB(IV) Rh+"),
            ("ab_neg", "AB(IV) Rh-"),
        ],
        string="Blood Group",
    )

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
    )

    birth_date = fields.Date(string="Birth Date")

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True,
    )

    @api.depends("birth_date")
    def _compute_age(self):
        today = date.today()

        for record in self:
            if record.birth_date:
                birth_date = record.birth_date
                record.age = (
                    today.year
                    - birth_date.year
                    - (
                        (today.month, today.day)
                        < (birth_date.month, birth_date.day)
                    )
                )
            else:
                record.age = 0