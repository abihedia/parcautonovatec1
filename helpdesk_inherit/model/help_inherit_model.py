from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('product.product', string='Article', default=lambda self: self.env['fleet.vehicle'].search([('partner_id', '=', self.partner_id.id)]).fleet_artic_id, domain="[('partner_id', '=', partner_id)]")
    tracking = fields.Selection(related='products_id.tracking')
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série', help="Lot/Serial number", domain="[('product_id', '=', products_id)]")

            
                
            
