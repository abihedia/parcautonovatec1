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
    montant_tot_partenariat = fields.Float('Montant total du partenariat')
    montant_rest_regl = fields.Float('Montant restant à régler', compute='_compute_amount_partner')
    factures_partner = fields.One2many('account.move', 'partner_id')
    code_client = fields.Char('Numéro client', readonly=True)
    partenariat_ids = fields.One2many('budget.partenariat','partner_id')

    @api.onchange('partenariat_ids')
    def addline(self):
        if len(self.partenariat_ids) > 5:
            raise  ValidationError('Vous avez dépassé la limite de 5 lignes')

    @api.onchange('name')
    def addpartenariat(self):
        for rec in self:
            if rec.name :
                vals = {'partner_id': self.id,
                        'annee': "2022",
                        }
                self.env['budget.partenariat'].create(vals)
                vals = {'partner_id': self.id,
                        'annee': "2023",
                        }
                self.env['budget.partenariat'].create(vals)
                vals = {'partner_id': self.id,
                        'annee': "2024",
                        }
                self.env['budget.partenariat'].create(vals)
                vals = {'partner_id': self.id,
                        'annee': "2025",
                        }
                self.env['budget.partenariat'].create(vals)
                vals = {'partner_id': self.id,
                        'annee': "2026",
                        }
                self.env['budget.partenariat'].create(vals)


    @api.model
    def create(self, vals):
        record = super(PartnerModelHerit, self).create(vals)
        record['code_client'] = self.env['ir.sequence'].next_by_code('code.client')
        return record

    @api.depends('partenariat_ids.montant_a_regler')
    def _compute_amount_partner(self):
        amount = 0.0
        for par in self:
            for rec in par.partenariat_ids:
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


    annee = fields.Char(string='Annee')
    statut = fields.Selection([('A régler', 'A régler'), ('Réglé', 'Réglé'), ('En attente de facture', 'En attente de facture')])
    montant_a_regler = fields.Float('Montant a regler')
    partner_id = fields.Many2one('res.partner', string='partner')
    date_reglement = fields.Date(string='Date de réglement')

