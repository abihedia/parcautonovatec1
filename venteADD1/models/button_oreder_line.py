from odoo import models, fields, api

class StocklotInherit(models.Model):
    _inherit = "stock.production.lot"
    seriel_id = fields.Many2one( "creatseriel",string='Numéro de série')

class SaleOrderLineHeritEND(models.Model):
    _inherit    = 'sale.order.line'
    def action_add_serial_number(self):
            product_id = self.product_id.id
            print(product_id)
            return {
                    'type': 'ir.actions.act_window',
                    'name': " ",
                    'res_model': 'creatseriel',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_product_id': product_id},
                }

class CreatSerielNumber(models.Model):
    _name = 'creatseriel'
    _description = 'Creat Seriel Number'
    product_id = fields.Many2one( "product.template",string='Article')
    serial_ids = fields.One2many('stock.production.lot', 'seriel_id',compute='serial_ids_function')


    def serial_ids_function(self):
        self.serial_ids = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id)])


    def create_creatseriel(self):
        print("bonjour......")

