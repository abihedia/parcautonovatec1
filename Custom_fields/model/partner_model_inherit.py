from odoo import models, fields, api

class PartnerModelHerit(models.Model):
    _inherit = 'res.partner'

    type_contact = fields.Selection([('Prospect', 'Prospect'), ('Client', 'Client')])
    parc_machine = fields.One2many('fleet.vehicle', 'partner_id')
    num_siren = fields.Char('N° SIREN')
    activity = fields.Char('activité')
    origine = fields.Many2one('partner.origin', string='Origine')
    montant_tot_partenariat = fields.Float('Montant total du partenariat')
    montant_rest_regl = fields.Float('Montant restant à régler')
    factures_partner = fields.One2many('account.move', 'partner_id')


class OriginPartner(models.Model):
    _name = 'partner.origin'
    _description ='Origin'

    name = fields.Char('Nom')

