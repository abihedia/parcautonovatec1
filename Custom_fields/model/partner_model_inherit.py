from odoo import models, fields, api
from odoo.exceptions import ValidationError,Warning

from datetime import datetime


class PartnerModelHerit(models.Model):
    _inherit = 'res.partner'

    type_contact = fields.Selection([('Prospect', 'Prospect'), ('Client', 'Client')])
    parc_machine = fields.One2many('fleet.vehicle', 'partner_id')
    num_siren = fields.Char('N° SIREN')
    activity = fields.Many2one('partner.activity', string='Activité')
    origine = fields.Many2one('partner.origin', string='Origine')
    montant_tot_partenariat = fields.Monetary('Montant total du partenariat', compute='compute_montant_partenariat')
    montant_rest_regl = fields.Monetary('Montant restant à régler', compute='_compute_amount_partner')
    code_client = fields.Char('Numéro client', readonly=True)
    partenariat_ids = fields.One2many('budget.partenariat','partner_id')

    @api.onchange('partenariat_ids')
    def addline(self):
        if len(self.partenariat_ids) > 5:
            raise  ValidationError('Vous avez dépassé la limite de 5 lignes')


    @api.model
    def create(self, vals):
        record = super(PartnerModelHerit, self).create(vals)
        record['code_client'] = self.env['ir.sequence'].next_by_code('code.client')
        return record
    
    
    @api.depends('sale_order_ids.sale_partenariat')
    def compute_montant_partenariat(self):
        part_amount = 0.0
        for rec in self:
            for par in self.sale_order_ids:
                part_amount += par.sale_partenariat
            rec.montant_tot_partenariat = part_amount

            

    @api.depends('partenariat_ids.montant_a_regler')
    def _compute_amount_partner(self):
        amount = 0.0
        for par in self:
            for rec in par.partenariat_ids:
                if rec.statut == "Réglé" :
                    amount += rec.montant_a_regler
            par.montant_rest_regl = par.montant_tot_partenariat - amount

class OriginPartner(models.Model):
    _name = 'partner.origin'
    _description ='Origin'

    name = fields.Char('Nom')


class OriginPartner(models.Model):
    _name = 'partner.activity'
    _description ='Activity'

    name = fields.Char('Nom')

class BudgetPartenariat(models.Model):
    _name = 'budget.partenariat'
    _description ='Partenariat'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    annee = fields.Char(string='Annee')
    statut = fields.Selection([('A régler', 'A régler'), ('Réglé', 'Réglé'), ('En attente de facture', 'En attente de facture')])
    montant_a_regler = fields.Monetary('Montant a regler')
    partner_id = fields.Many2one('res.partner', string='partner')
    date_reglement = fields.Date(string='Date de réglement')

