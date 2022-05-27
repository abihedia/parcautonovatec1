from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('fleet.vehicle', string='Article', domain="[('partner_id', '=', partner_id)]")
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série', help="Lot/Serial number")
