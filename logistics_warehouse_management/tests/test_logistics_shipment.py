from odoo.tests.common import TransactionCase


class TestLogisticsShipment(TransactionCase):

    def test_storage_amount(self):
        partner = self.env["res.partner"].create({
            "name": "Demo Logistics Customer",
        })
        shipment = self.env["logistics.shipment"].create({
            "partner_id": partner.id,
            "entry_date": "2026-01-01",
            "exit_date": "2026-01-10",
            "storage_rate": 25.0,
        })
        self.assertEqual(shipment.storage_days, 10)
        self.assertEqual(shipment.storage_amount, 250.0)
