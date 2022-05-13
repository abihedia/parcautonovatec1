from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class SaleOrderLineHerit(models.Model):
    _inherit    = 'sale.order.line'
    price_sale = fields.Monetary(string="Prix d'achat")
    designation = fields.Char(compute="compute_designation",string="Désignation")

    @api.depends('name')
    def compute_designation(self):
        for rec in self:
            if rec.name:
                chaine = rec.name.split()
                rec.designation = " ".join(chaine[1:])
            else:
                rec.designation = False

class SaleOrderHerit(models.Model):
    _inherit    = 'sale.order'
    sale_total_vente = fields.Monetary(string="Total vente",default=0.0,compute="sale_total_vente_func")
    sale_marge  = fields.Monetary(compute="sale_marge_fuc",default=0.0, string="Marge commerciale")
    sale_marge_reel = fields.Monetary(default=0.0, string="Marge réelle")
    sale_date_traitement = fields.Date("Date de traitement",compute="sale_total_date_traitement")

    ############ zip street city
    street_client = fields.Char(compute="compute_street_client")
    zip_client = fields.Char(compute="compute_zip_client")
    city_client = fields.Char(compute="compute_city_client")

    @api.onchange("partner_id")
    def compute_street_client(self):
        for rec in self:
            if rec.partner_id:
                rec.street_client = rec.partner_id.street
            else:
                rec.street_client = False

    @api.onchange("partner_id")
    def compute_zip_client(self):
        for rec in self:
            if rec.partner_id:
                rec.zip_client = rec.partner_id.zip
            else:
                rec.zip_client = False

    @api.onchange("partner_id")
    def compute_city_client(self):
        for rec in self:
            if rec.partner_id:
                rec.city_client = rec.partner_id.city
            else:
                rec.city_client = False

    street_fact = fields.Char(compute="compute_street_fact")
    zip_fact = fields.Char(compute="compute_zip_fact")
    city_fact = fields.Char(compute="compute_city_fact")

    @api.onchange("partner_invoice_id")
    def compute_street_fact(self):
        for rec in self:
            if rec.partner_invoice_id:
                rec.street_fact = rec.partner_invoice_id.street
            else:
                rec.street_fact = False

    @api.onchange("partner_invoice_id")
    def compute_zip_fact(self):
        for rec in self:
            if rec.partner_invoice_id:
                rec.zip_fact = rec.partner_invoice_id.zip
            else:
                rec.zip_fact = False

    @api.onchange("partner_invoice_id")
    def compute_city_fact(self):
        for rec in self:
            if rec.partner_invoice_id:
                rec.city_fact = rec.partner_invoice_id.city
            else:
                rec.city_fact = False

    street_livraison = fields.Char(compute="compute_street_livraison")
    zip_livraison = fields.Char(compute="compute_zip_livraison")
    city_livraison = fields.Char(compute="compute_city_livraison")

    @api.onchange("partner_shipping_id")
    def compute_street_livraison(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.street_livraison = rec.partner_shipping_id.street
            else:
                rec.street_livraison = False

    @api.onchange("partner_shipping_id")
    def compute_zip_livraison(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.zip_livraison = rec.partner_shipping_id.zip
            else:
                rec.zip_livraison = False

    @api.onchange("partner_invoice_id")
    def compute_city_livraison(self):
        for rec in self:
            if rec.partner_invoice_id:
                rec.city_livraison = rec.partner_invoice_id.city
            else:
                rec.city_livraison = False

    ##################### fin




    def sale_total_date_traitement(self):
        for rec in self:
            rec.sale_date_traitement =date.today()



    #########  Financement page
    #group 1
    sale_type    = fields.Selection([('location', 'Location'), ('vente', 'Vente')],string='Type',default='location')
    sale_leaser  = fields.Many2one( "typeleaser",string='Leaser')
    sale_finance = fields.Monetary(string="Montant financé")
    sale_frais_restitution = fields.Monetary(string="Frais de restitution")
    #group 2
    sale_duree   = fields.Integer(string="Durée")
    sale_accord  = fields.Char(string="N° d'accord")
    sale_loyer   = fields.Monetary(string="Loyer")
    #group 3
    sale_periodicite = fields.Selection([('mens', 'Mensuelle'), ('trim', 'Trimestrielle ')], string='Periodicité')
    sale_reglement   = fields.Selection([('prelevement ', 'Prélevement'), ('mandat', 'Mandat administratif'),('virement', 'Virement '),('cheque', 'Chéque')], string='Mode de reglement')
    sale_frais       = fields.Monetary(string="Frais de livraison")
    #########  Rachats page
    #group 1
    sale_vr_client      = fields.Monetary(string="Montant du rachat")
    sale_ir_prospects   = fields.Monetary(string="Montant du rachat")
    sale_rachat_matriel = fields.Monetary(string="Montant sponsoring")
    sale_date_rachat_prevue = fields.Date("Date de rachat prévue")
    sale_marque_reference = fields.Char(string="Matériels rachetés")
    #groupe 2
    sale_leaser_ra = fields.Many2one( "typeleaser",string='Leaser')
    sale_partenariat = fields.Monetary(string="Montant total de partenariat")
    sale_marque_reference_prospect = fields.Char(string="Matériels rachetés")
    #groupe 3
    sale_accord_rachat = fields.Char(string="Dossier N°")
    sale_solde_2_fois = fields.Monetary(string="Montant solde en 2 fois")
    sale_Gratuite = fields.Monetary(string="Gratuitée copie")
    #groupe 4
    sale_date_fin_F = fields.Date("Date de fin du partenariat")
    sale_date_2_solde = fields.Date("Date de 2éme solde à effectuer")
    # groupe 5 client 2
    sale_vr_client_2 = fields.Monetary(string="Montant du rachat")
    sale_leaser_ra_client_2 = fields.Many2one("typeleaser", string='Leaser')
    sale_accord_rachat_client_2 = fields.Char(string="Dossier N°")
    sale_date_rachat_prevue_client_2 = fields.Date("Date de rachat prévue")
    sale_marque_reference_client_2 = fields.Char(string="Matériels rachetés")



    #########  Maintenance page
    # group 1
    sale_cout_signe_nb = fields.Float(string="Cout copie Signé ",digits=(16, 4))
    sale_cout_actuel_nb = fields.Monetary(string="Cout copie Actuel ")
    sale_cout_actuel_signe_nb = fields.Monetary(compute="ecart_actuel_signe_nb",string="Ecart Actuel/Signé")

    @api.onchange("sale_cout_signe_nb","sale_cout_actuel_nb")
    def ecart_actuel_signe_nb(self):
        for rec in self:
            rec.sale_cout_actuel_signe_nb = rec.sale_cout_signe_nb-rec.sale_cout_actuel_nb

    sale_cout_signe_col = fields.Float(string="Coleur: ",digits=(16, 4))
    sale_cout_actuel_col = fields.Monetary(string="Coleur: ")
    sale_cout_actuel_signe_col = fields.Monetary(compute="ecart_actuel_signe_col",string="Coleur: ")

    @api.onchange("sale_cout_signe_col", "sale_cout_actuel_col")
    def ecart_actuel_signe_col(self):
        for rec in self:
            rec.sale_cout_actuel_signe_col = rec.sale_cout_signe_col - rec.sale_cout_actuel_col
    # group 2
    sale_forfait_signe_nb = fields.Monetary(string="Forfait copie Signé")
    sale_forfait_actuel_nb = fields.Monetary(string="Forfait copie Actuel")
    sale_forfait_actuel_signe_nb = fields.Monetary(compute="ecart_forfait_actuel_signe_nb",string="Ecart Actuel/Signé")

    @api.onchange("sale_forfait_signe_nb", "sale_forfait_actuel_nb")
    def ecart_forfait_actuel_signe_nb(self):
        for rec in self:
            rec.sale_forfait_actuel_signe_nb = rec.sale_forfait_signe_nb - rec.sale_forfait_actuel_nb

    sale_forfait_signe_col = fields.Monetary(string="Couleur: ")
    sale_forfait_actuel_col = fields.Monetary(string="Couleur: ")
    sale_forfait_actuel_signe_col = fields.Monetary(compute="ecart_forfait_actuel_signe_col",string="Couleur: ")

    @api.onchange("sale_forfait_signe_col", "sale_forfait_actuel_col")
    def ecart_forfait_actuel_signe_col(self):
        for rec in self:
            rec.sale_forfait_actuel_signe_col = rec.sale_forfait_signe_col - rec.sale_forfait_actuel_col
    # group 3
    sale_abonnement_service = fields.Monetary(string="Abonnement Service")
    sale_autre_frais        = fields.Monetary(string="Autre frais")

    @api.onchange("sale_total_vente","sale_finance","sale_frais","sale_frais_restitution","sale_vr_client","sale_ir_prospects","sale_vr_client_2","sale_rachat_matriel","sale_Gratuite","sale_partenariat","sale_solde_2_fois")
    def sale_marge_fuc(self):
        for rec in self:
            rec.sale_marge = rec.sale_finance + rec.sale_frais -rec.sale_total_vente- rec.sale_frais_restitution -rec.sale_vr_client-rec.sale_ir_prospects-rec.sale_vr_client_2-rec.sale_rachat_matriel-rec.sale_Gratuite-rec.sale_partenariat-rec.sale_solde_2_fois


    @api.onchange("tax_totals_json")
    def sale_total_vente_func(self):
        for rec in self:
            rec.sale_total_vente = rec.amount_total


    ################### calcul auto pour parc matériels
    sale_parc_id = fields.Many2one('fleet.vehicle', string='Parc Matériel')

    #################### récupurer le numéro de dossier dans parc matériels
    @api.onchange("sale_parc_id","name")
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

    @api.onchange("sale_parc_id","sale_periodicite","sale_duree")
    def fleetDateEXpiration(self):
        for rec in self:
            if rec.sale_parc_id:
                    if rec.sale_periodicite == 'mens':
                        if rec.sale_duree > 0:
                            rec.sale_parc_id.fleet_expiration_date = date.today() + relativedelta(
                                months=rec.sale_duree) - relativedelta(days=1)
                        else:
                            rec.sale_parc_id.fleet_expiration_date = date.today()

                    if rec.sale_periodicite == 'trim':
                        if rec.sale_duree > 0:
                            rec.sale_parc_id.fleet_expiration_date = date.today() + relativedelta(
                                months=(rec.sale_duree * 3)) - relativedelta(days=1)
                        else:
                            rec.sale_parc_id.fleet_expiration_date = date.today()

    @api.onchange("sale_parc_id")
    def fleetDateInstalation(self):
        for rec in self:
            if rec.sale_parc_id:
                rec.sale_parc_id.fleet_date_inst =date.today()

    ########## fin auto



















