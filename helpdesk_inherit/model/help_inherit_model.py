from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('product.product', string='Article')
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série')

