from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LogisticsShipment(models.Model):
    _name = "logistics.shipment"
    _description = "Logistics Shipment"
    _order = "entry_date desc, id desc"

    name = fields.Char(
        string="Shipment Reference",
        required=True,
        copy=False,
        default="New",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        tracking=True,
    )
    entry_date = fields.Date(
        string="Entry Date",
        required=True,
        default=fields.Date.context_today,
    )
    exit_date = fields.Date(string="Exit Date")
    quantity = fields.Float(string="Quantity", default=1.0)
    cbm = fields.Float(string="CBM")
    storage_rate = fields.Monetary(
        string="Storage Rate / Day",
        currency_field="currency_id",
    )
    storage_days = fields.Integer(
        string="Storage Days",
        compute="_compute_storage_values",
        store=True,
    )
    storage_amount = fields.Monetary(
        string="Storage Amount",
        compute="_compute_storage_values",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("stored", "Stored"),
            ("outbound", "Outbound"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
    notes = fields.Text(string="Notes")

    @api.depends("entry_date", "exit_date", "storage_rate")
    def _compute_storage_values(self):
        today = fields.Date.context_today(self)
        for shipment in self:
            if not shipment.entry_date:
                shipment.storage_days = 0
                shipment.storage_amount = 0.0
                continue

            end_date = shipment.exit_date or today
            days = max((end_date - shipment.entry_date).days + 1, 0)
            shipment.storage_days = days
            shipment.storage_amount = days * shipment.storage_rate

    @api.constrains("entry_date", "exit_date")
    def _check_dates(self):
        for shipment in self:
            if shipment.exit_date and shipment.entry_date and shipment.exit_date < shipment.entry_date:
                raise ValidationError("Exit Date cannot be earlier than Entry Date.")

    def action_set_stored(self):
        self.write({"state": "stored"})

    def action_set_outbound(self):
        self.write({"state": "outbound"})

    def action_set_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancel"})
