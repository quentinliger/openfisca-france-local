 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class garantie_jeune_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Variable NEET - Not in Employement, Education or Training"

    def formula(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        scolarite = individu('scolarite', period)
        activite = individu('activite', period)
        not_in_education = (scolarite == TypesScolarite.inconnue) * (activite != TypesActivite.etudiant)

        no_indemnites_stage = individu('indemnites_stage', period) == 0
        no_revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period) == 0
        not_in_training = no_indemnites_stage * no_revenus_stage_formation_pro

        return not_in_employment * not_in_education * not_in_training


class garantie_jeune_max(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Montant maximal de l'allocation Garantie Jeune"
    reference = [
        'Article D5131-20 du code du travail',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=DED54A598193DDE1DF59E0AE16BDE87D.tplgfr21s_3?idArticle=LEGIARTI000033709227&cidTexte=LEGITEXT000006072050'
        ]

    def formula(individu, period, parameters):
        params = parameters(period).prestations.minima_sociaux.rsa
        montant_base = params.montant_de_base_du_rsa
        taux_1_personne = params.forfait_logement.taux_1_personne

        return (individu('age', period) > 0) * montant_base * (1 - taux_1_personne)
