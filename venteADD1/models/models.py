from odoo import models, fields, api

class SaleOrderLineHerit(models.Model):
    _inherit    = 'sale.order.line'
    price_sale = fields.Monetary(string="Prix d'achat")

class SaleOrderHerit(models.Model):
    _inherit    = 'sale.order'
    sale_marge  = fields.Float(compute="sale_marge_fuc",default=0.0, string="Marge")


    #########  Financement page
    #group 1
    sale_type    = fields.Selection([('location', 'Location'), ('vente', 'Vente')],string='Type',default='location')
    sale_leaser  = fields.Many2one( "typeleaser",string='Leaser')
    sale_finance = fields.Monetary(string="Montant financé")
    #group 2
    sale_duree   = fields.Integer(string="Durée")
    sale_accord  = fields.Char(string="N° d'accord")
    sale_loyer   = fields.Monetary(string="Loyer")
    #group 3
    sale_periodicite = fields.Selection([('mens', 'Mensuelle'), ('trim', 'Trimestrielle ')], string='Periodicité')
    sale_reglement   = fields.Selection([('mens', 'Mensuelle'), ('trim', 'Trimestrielle ')], string='Mode de reglement')
    sale_frais       = fields.Monetary(string="Frais de livraison")
    #########  Rachats page
    #group 1
    sale_vr_client      = fields.Monetary(string="VR clients")
    sale_ir_prospects   = fields.Monetary(string="IR prospects")
    sale_rachat_matriel = fields.Monetary(string="Rachat matriél")
    #groupe 2
    sale_leaser_ra = fields.Char(string="Leaser")
    sale_partenariat = fields.Monetary(string="Partenariat")
    sale_marque_reference = fields.Char(string="Marque & référence")
    #groupe 3
    sale_accord_rachat = fields.Char(string="N° d'accord")
    sale_solde_2_fois = fields.Monetary(string="Solde en 2 fois")
    sale_Gratuite = fields.Monetary(string="Gratuitée")
    #groupe 4
    sale_date_fin_F = fields.Date("Date de fin du partenariat")
    sale_date_2_solde = fields.Date("Date de 2éme solde à effectuer")

    #########  Maintenance page
    # group 1
    sale_cout_signe_nb = fields.Float(string="Cout copie Signé ",digits=(16, 4))
    sale_cout_actuel_nb = fields.Monetary(string="Cout copie Actuel ")
    sale_cout_actuel_signe_nb = fields.Monetary(string="Ecart Actuel/Signé")

    sale_cout_signe_col = fields.Float(string="Coleur: ",digits=(16, 4))
    sale_cout_actuel_col = fields.Monetary(string="Coleur: ")
    sale_cout_actuel_signe_col = fields.Monetary(string="Coleur: ")
    # group 2
    sale_forfait_signe_nb = fields.Monetary(string="Forfait copie Signé")
    sale_forfait_actuel_nb = fields.Monetary(string="Forfait copie Actuel")
    sale_forfait_actuel_signe_nb = fields.Monetary(string="Ecart Actuel/Signé")

    sale_forfait_signe_col = fields.Monetary(string="Couleur: ")
    sale_forfait_actuel_col = fields.Monetary(string="Couleur: ")
    sale_forfait_actuel_signe_col = fields.Monetary(string="Couleur: ")
    # group 3
    sale_abonnement_service = fields.Monetary(string="Abonnement Service")
    sale_autre_frais        = fields.Monetary(string="Autre frais")



    def sale_marge_fuc(self):
        for rec in self:
            rec.sale_marge = 0

    ################### calcul auto pour parc matériels
    sale_parc_id = fields.Many2one('fleet.vehicle', string='Parc Matériel')

    #################### récupurer le numéro de dossier dans parc matériels
    @api.onchange("sale_parc_id")
    def fleetDevisID(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_dossier_devis = rec.name

    ##################
    ##########                infos CONTRATS Automatique
    ##################
    @api.onchange("sale_parc_id", "sale_type")
    def fleetType(self):
        for rec in self:
            if rec.sale_parc_id:
                if rec.sale_type == 'location':
                    rec.sale_parc_id.fleet_type = 'location'
                if rec.sale_type == 'vente':
                    rec.sale_parc_id.fleet_type = 'vente'

    @api.onchange("sale_periodicite", "sale_parc_id")
    def fleetPeriodicite(self):
        for rec in self:
            if rec.sale_parc_id:
                if rec.sale_periodicite == 'trim':
                    rec.sale_parc_id.fleet_periodicite = 'trim'
                    rec.sale_parc_id.fleet_facturation = 'trim'
                if rec.sale_periodicite == 'mens':
                    rec.sale_parc_id.fleet_periodicite = 'mens'
                    rec.sale_parc_id.fleet_facturation = 'mens'

    @api.onchange("sale_parc_id", "sale_loyer")
    def fleetPrixHT(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_prix_HT = rec.sale_loyer

    @api.onchange("sale_parc_id", "sale_duree")
    def fleetDuree(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_duree = rec.sale_duree

    @api.onchange("sale_parc_id", "sale_leaser")
    def fleetLeaser(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_leaser = rec.sale_leaser

    @api.onchange("sale_parc_id", "sale_accord")
    def fleetAccord(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_accord = rec.sale_accord
    ##################
    ##########                infos MAINTENANCE Automatique
    ##################
    @api.onchange("sale_parc_id", "sale_cout_signe_col")
    def fleetCoutCouleur(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_cout_Couleur = rec.sale_cout_signe_col

    @api.onchange("sale_parc_id", "sale_forfait_signe_col")
    def fleetorForfaitCouleur(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_forfait_couleur = rec.sale_forfait_signe_col

    @api.onchange("sale_parc_id", "sale_cout_signe_nb")
    def fleetorCoutNb(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_cout_nb = rec.sale_cout_signe_nb

    @api.onchange("sale_parc_id", "sale_forfait_signe_nb")
    def fleetorForfaitNB(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_forfait_nb = rec.sale_forfait_signe_nb

    @api.onchange("sale_parc_id", "sale_abonnement_service")
    def fleetorAbonnementService(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_abonnement_service = rec.sale_abonnement_service

    @api.onchange("sale_parc_id", "sale_autre_frais")
    def fleetorAutre(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_autre = rec.sale_autre_frais
    ##################
    ##########                infos FINANCIERES Automatique
    ##################

    @api.onchange("sale_parc_id", "sale_partenariat")
    def fleetPartenariat(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_partenariat = rec.sale_partenariat

    @api.onchange("sale_parc_id", "sale_solde_2_fois")
    def fleetSoldefois(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_solde_fois = rec.sale_solde_2_fois

    @api.onchange("sale_parc_id", "sale_date_fin_F")
    def fleetDateFin(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_date_fin_F = rec.sale_date_fin_F

    @api.onchange("sale_parc_id", "sale_date_2_solde")
    def fleetDateSoldefois(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_date_2_solde = rec.sale_date_2_solde


















