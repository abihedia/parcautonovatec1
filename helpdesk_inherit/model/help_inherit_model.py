from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('product.product', string='Article', default= lambda self:self.env['product.product'].search([('id','in',[a['fleet_artic_id'][0] for a in self.env['fleet.vehicle'].search_read([('partner_id', '=', self.partner_id.id)],['fleet_artic_id'])])]))
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série', help="Lot/Serial number", domain="[('product_id', '=', products_id)]")
    
   
    
    
    
    

            
                
            
