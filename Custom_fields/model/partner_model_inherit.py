from odoo import models, fields, api
from datetime import datetime

class PartnerModelHerit(models.Model):
    _inherit = 'res.partner'

    type_contact = fields.Selection([('Prospect', 'Prospect'), ('Client', 'Client')])
    parc_machine = fields.One2many('fleet.vehicle', 'partner_id')
    num_siren = fields.Char('N° SIREN')
    activity = fields.Many2one('partner.activity', string='Activité')
    origine = fields.Many2one('partner.origin', string='Origine')
    montant_tot_partenariat = fields.Float('Montant total du partenariat')
    montant_rest_regl = fields.Float('Montant restant à régler', compute='_compute_amount_partner')
    factures_partner = fields.One2many('account.move', 'partner_id')
    code_client = fields.Char('Numéro client', readonly=True)
    factures_ids = fields.One2many('account.move', compute="compute_state_facture")

    @api.depends('factures_partner')
    def compute_state_facture(self):
        for rec in self:
            rec.factures_ids =  self.self.env['account.move'].search([('move_type', '=', 'out_invoice'),('partner_id', '=', rec.id)])




    @api.model
    def create(self, vals):
        record = super(PartnerModelHerit, self).create(vals)
        record['code_client'] = self.env['ir.sequence'].next_by_code('code.client')
        return record

    @api.depends('factures_ids.amount_total_signed')
    def _compute_amount_partner(self):
        amount = 0.0
        for par in self:
            for rec in par.factures_ids:
                amount += rec.amount_total_signed
            par.montant_rest_regl = par.montant_tot_partenariat - amount

class OriginPartner(models.Model):
    _name = 'partner.origin'
    _description ='Origin'

    name = fields.Char('Nom')


class OriginPartner(models.Model):
    _name = 'partner.activity'
    _description ='Activity'

    name = fields.Char('Nom')



