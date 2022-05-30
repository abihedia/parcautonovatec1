from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('fleet.vehicle', string='Article', default=lambda self: self.env['fleet.vehicle'].search([('partner_id', '=', self.partner_id.id)]), domain="[('partner_id', '=', partner_id)]")
    fleet_id = fields.Many2one('product.product', default="computeProduct")
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série', help="Lot/Serial number")
    
    def computeProduct(self):
        partner_fleet = self.env['fleet.vehicle'].search([('partner_id', '=', self.partner_id.id)]) 
        liste_product =[]
        for rec in partner_fleet:
            liste_product.append(rec.fleet_artic_id)
        return liste_product
            
                
            
