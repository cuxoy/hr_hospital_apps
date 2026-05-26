from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    """Disease model with hierarchy."""
    _name = "hospital.disease"
    _description = "Disease"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "complete_name"

    name = fields.Char(string="Disease Name", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")

    parent_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Parent Disease",
        index=True,
        ondelete="restrict",
    )
    parent_path = fields.Char(index=True)

    child_ids = fields.One2many(
        comodel_name="hospital.disease",
        inverse_name="parent_id",
        string="Child Diseases",
    )

    complete_name = fields.Char(
        string="Full Name",
        compute="_compute_complete_name",
        recursive=True,
        store=True,
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for disease in self:
            if disease.parent_id:
                disease.complete_name = f"{disease.parent_id.complete_name} / {disease.name}"
            else:
                disease.complete_name = disease.name

    @api.depends("complete_name")
    def _compute_display_name(self):
        for disease in self:
            disease.display_name = disease.complete_name

    @api.constrains("parent_id")
    def _check_parent_id(self):
        for disease in self:
            if disease.parent_id == disease:
                raise ValidationError("Disease cannot be parent of itself.")

            if disease._has_cycle():
                raise ValidationError("You cannot create recursive disease categories.")