from odoo import models, fields, api

class PartnerModelHerit(models.Model):
    _inherit = 'res.partner'

    type_contact = fields.Selection([('Prospect', 'Prospect'), ('Client', 'Client')])
    parc_machine = fields.One2many('fleet.vehicle', 'partner_id')
    num_siren = fields.Char('N° SIREN')
    activity = fields.Many2one('mail.activity', String="Activité")
    origine = fields.Many2one('partner.origin', string='Origine')
    montant_tot_partenariat = fields.Float('Montant total du partenariat')
    montant_rest_regl = fields.Float('Montant restant à régler', compute='_compute_amount_partner')
    factures_partner = fields.One2many('account.move', 'partner_id')

    @api.depends('factures_partner.amount_residual_signed')
    def _compute_amount_partner(self):
        amount = 0.0
        for par in self:
            for rec in par.factures_partner:
                amount += rec.amount_residual_signed
            par.montant_rest_regl = par.montant_tot_partenariat - amount

class OriginPartner(models.Model):
    _name = 'partner.origin'
    _description ='Origin'

    name = fields.Char('Nom')

