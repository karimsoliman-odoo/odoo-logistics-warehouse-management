from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestLogisticsShipment(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Demo Logistics Customer",
        })

    def test_sequence_is_generated(self):
        shipment = self.env["logistics.shipment"].create({
            "partner_id": self.partner.id,
        })
        self.assertNotEqual(shipment.name, "New")
        self.assertTrue(shipment.name.startswith("SHP/"))

    def test_storage_amount(self):
        shipment = self.env["logistics.shipment"].create({
            "partner_id": self.partner.id,
            "entry_date": "2026-01-01",
            "exit_date": "2026-01-10",
            "storage_rate": 25.0,
        })
        self.assertEqual(shipment.storage_days, 10)
        self.assertEqual(shipment.storage_amount, 250.0)

    def test_invalid_exit_date(self):
        with self.assertRaises(ValidationError):
            self.env["logistics.shipment"].create({
                "partner_id": self.partner.id,
                "entry_date": "2026-01-10",
                "exit_date": "2026-01-01",
            })

    def test_negative_storage_rate(self):
        with self.assertRaises(ValidationError):
            self.env["logistics.shipment"].create({
                "partner_id": self.partner.id,
                "storage_rate": -1.0,
            })

    def test_workflow(self):
        shipment = self.env["logistics.shipment"].create({
            "partner_id": self.partner.id,
        })
        shipment.action_set_stored()
        self.assertEqual(shipment.state, "stored")
        shipment.action_set_outbound()
        self.assertEqual(shipment.state, "outbound")
        shipment.action_set_done()
        self.assertEqual(shipment.state, "done")
