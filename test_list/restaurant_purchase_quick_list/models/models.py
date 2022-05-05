from odoo import models, fields, api
import datetime


class PurchaseOrderveHerit(models.Model):
    _inherit = 'purchase.order'
    lien_vers_al = fields.Many2one('quicklast', string='Lien vers quick list')


class ProductTemplateInherit(models.Model):
    _inherit = 'product.product'
    qte_product = fields.Float('Quantity ',default='0',store=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_purchase = fields.Float('Purchase price',default='0')

class ProductQuick(models.Model):
    _name = 'productquicktemplate'
    quick_product_id =  fields.Many2one('product.product',string='Product')
    quick_qte_product = fields.Float('Quantity ', default='0', store=True)
    quick_vendor_num = fields.Many2one('res.partner', string='Vendor')
    quick_price_purchase = fields.Float('Purchase price', default='0')
    quick_quicklast = fields.Many2one('quicklast', string='QuickID')

    def action_add(self):
        self.quick_qte_product +=1
        self.quick_product_id.qte_product = self.quick_qte_product
    def action_remove(self):
        if self.quick_qte_product > 0:
            self.quick_qte_product -= 1
            self.quick_product_id.qte_product = self.quick_qte_product
        else:
            self.quick_qte_product = 0
            self.quick_product_id.qte_product = self.quick_qte_product

    @api.onchange('quick_vendor_num','quick_price_purchase')
    def update(self):
        self.quick_product_id.partner_id = self.quick_vendor_num
        self.quick_product_id.price_purchase = self.quick_price_purchase

    @api.onchange('quick_qte_product')
    def update_qte(self):
        self.quick_product_id.qte_product = self.quick_qte_product


class QuikListlast(models.Model):
    _name = 'quicklast'
    _description = 'Quik List help'
    name = fields.Char('Name', default="Quick Order list")
    qck_ProductQuick_id = fields.One2many('productquicktemplate', string=False, inverse_name='quick_quicklast')
    def name_get(self):
        cour_s = []
        for rec in self:
            cour_s.append((rec.id, 'Quick List' ))
        return cour_s

    def refrech_po(self):
        products_ids = self.env['product.product'].search([])
        product_lines = []
        product_ids = []
        for product in self.qck_ProductQuick_id:
            product_ids.append(product.quick_product_id.id)
        for line in products_ids:
            if line.id not in product_ids:
                product_lines.append((0, 0, {

                    'quick_product_id': line.id,

            }))
        self.qck_ProductQuick_id = product_lines

    def send_po(self):
        products_ids = self.env['product.product'].search([])
        product_list = []
        partner_ids = []
        for product in products_ids:
            if product.qte_product > 0:
                product_list.append(product)
                if product.partner_id:
                    partner = product.partner_id
                    if product.partner_id not in partner_ids:
                        partner_ids.append(partner)
        for partner in partner_ids:
            vals = {'partner_id': partner.id,
                    'company_id': self.env.user.company_id.id,
                    'date_planned': datetime.datetime.now(),
                    'lien_vers_al': self.id,
                    'state':'purchase',
                    'date_approve':datetime.datetime.now(),
                    }
            purchase_id = self.env['purchase.order'].sudo().create(vals)
            for product in product_list:
                if product.partner_id == partner:
                    vals = {'product_id': product.id,
                            'name': product.name,
                            'order_id': purchase_id.id,
                            'price_unit': product.price_purchase,
                            'product_qty': product.qte_product,
                            }
                    self.env['purchase.order.line'].create(vals)
                    product.update({'qte_product': 0, })
            for line in self.qck_ProductQuick_id:
                line.quick_qte_product = 0

    #lien vers purchase order



    purcahse_order_count = fields.Integer(string="Purchase Count", compute="compute_purchase_count")

    def compute_purchase_count(self):
        for rec in self:
            order_count = self.env['purchase.order'].search_count([('lien_vers_al', '=', rec.id)])
            rec.purcahse_order_count = order_count

    def action_open_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'domain': [('lien_vers_al', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }




