from odoo import models, fields, api

class PartnerModelHerit(models.Model):
    _inherit = 'res.partner'

    type_contact = fields.Selection([('Prospect', 'Prospect'), ('Client', 'Client')])
    parc_machine = fields.One2many('fleet.vehicle', 'partner_id')
    num_siren = fields.Char('N° SIREN')
    activity = fields.Char('activité')
    origine = fields.Many2one('partner.origin', ondelete='Set null', string='Origine', index=True)


class OriginPartner(models.Model):
    _name = 'partner.origin'
    _description ='Origin'

    Name = fields.Char('Nom')

