# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_pch_domicile(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap à domicile"
    reference = ["Titre 3 Chapitre 1-3 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                   La Prestation de compensation du handicap à domicile (PCH) a pour but de compenser les conséquences du handicap. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, des aides animalières, des charges spécifiques (service de téléalarme, etc.) ou exceptionnelles. 
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period):
        ressortissant_eee = individu('ressortissant_eee', period)
        situation_handicap = individu('handicap', period)
        possede_aeeh = individu.famille('aeeh', period) > 0
        possede_apa = individu('apa_domicile', period) > 0
        possede_actp = individu('actp', period)

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride',period)
        condition_handicap = situation_handicap
        condition_aides_aeeh = False if possede_aeeh else True
        condition_aides_apa = False if possede_apa else True
        condition_aides_actp = False if possede_actp else True

        return condition_residence * condition_nationalite * condition_handicap * condition_aides_aeeh * condition_aides_apa * condition_aides_actp


class eure_et_loir_eligibilite_pch_etablissement(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir,éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap en établissement"
    reference = ["Titre 3 Chapitre 2-2 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                   La PCH en établissement a pour but de compenser les conséquences du handicap durant les périodes d’interruption d’hospitalisation ou d’hébergement en établissement. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, etc.
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period):
        ressortissant_eee = individu('ressortissant_eee', period)
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride',period)
        condition_handicap = individu('handicap', period)
        condition_hebergement = individu.famille('place_hebergement', period)

        return condition_residence * condition_nationalite * condition_handicap * condition_hebergement
