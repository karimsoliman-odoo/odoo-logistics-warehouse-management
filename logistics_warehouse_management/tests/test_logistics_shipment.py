from odoo.tests.common import TransactionCase


class TestLogisticsShipment(TransactionCase):

    def test_storage_amount(self):
        shipment = self.env["logistics.shipment"].create({
            "partner_id": self.env.ref("base.res_partner_1").id,
            "entry_date": "2026-01-01",
            "exit_date": "2026-01-10",
            "storage_rate": 25.0,
        })
        self.assertEqual(shipment.storage_days, 10)
        self.assertEqual(shipment.storage_amount, 250.0)
