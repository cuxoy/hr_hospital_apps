from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


class TestHospitalModels(TransactionCase):
    """Tests for hospital model methods."""

    def setUp(self):
        super().setUp()

        self.category = self.env["hospital.doctor.category"].create({
            "name": "Test Category",
            "quality_level": 1,
        })
        self.doctor = self.env["hospital.doctor"].create({
            "name": "Dr Test",
            "category_id": self.category.id,
        })
        self.patient = self.env["hospital.patient"].create({
            "name": "Patient Test",
        })
        self.disease = self.env["hospital.disease"].create({
            "name": "Disease Test",
        })

    def test_doctor_history_display_name(self):
        """Check doctor history display name."""
        history = self.env["hospital.doctor.history"].create({
            "patient_id": self.patient.id,
            "doctor_id": self.doctor.id,
        })
        history._compute_display_name()
        self.assertIn("Patient Test", history.display_name)

    def test_visit_done_write_protection(self):
        """Check that completed visit cannot change doctor."""
        visit = self.env["hospital.visit"].create({
            "name": "VISIT-TEST",
            "state": "done",
            "patient_id": self.patient.id,
            "doctor_id": self.doctor.id,
            "disease_id": self.disease.id,
        })

        with self.assertRaises(UserError):
            visit.write({"doctor_id": False})

    def test_disease_self_parent_validation(self):
        """Check disease cannot be parent of itself."""

        with self.assertRaises(UserError):
            self.disease.write({'parent_id': self.disease.id})