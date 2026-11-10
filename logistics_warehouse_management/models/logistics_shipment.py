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
        readonly=True,
        default="New",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    entry_date = fields.Date(
        string="Entry Date",
        required=True,
        default=fields.Date.context_today,
        index=True,
    )
    exit_date = fields.Date(string="Exit Date", index=True)
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
        index=True,
    )
    notes = fields.Text(string="Notes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "logistics.shipment"
                ) or "New"
        return super().create(vals_list)

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
            if (
                shipment.exit_date
                and shipment.entry_date
                and shipment.exit_date < shipment.entry_date
            ):
                raise ValidationError(
                    "Exit Date cannot be earlier than Entry Date."
                )

    @api.constrains("quantity", "cbm", "storage_rate")
    def _check_positive_values(self):
        for shipment in self:
            if shipment.quantity < 0:
                raise ValidationError("Quantity cannot be negative.")
            if shipment.cbm < 0:
                raise ValidationError("CBM cannot be negative.")
            if shipment.storage_rate < 0:
                raise ValidationError("Storage Rate cannot be negative.")

    def action_set_stored(self):
        self.write({"state": "stored"})

    def action_set_outbound(self):
        self.write({"state": "outbound"})

    def action_set_done(self):
        self.write({"state": "done"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})

    def action_cancel(self):
        self.write({"state": "cancel"})
