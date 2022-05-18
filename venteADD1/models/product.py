from odoo import api, fields, models


class ProductProductInherit(models.Model):
    _inherit = "product.template"
    parc_ok = fields.Boolean(default=False, string="Peut être un Parc")
    serie_number_materiel = fields.Char(string="N° serie")
