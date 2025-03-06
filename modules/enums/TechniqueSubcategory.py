# external modules import
from enum import Enum


# enumerate definition
class TechniqueSubcategory(Enum):
    MARINATURA = 'Marinatura'
    AFFUMICATURA = 'Affumicatura'
    FERMENTAZIONE = 'Fermentazione'
    TECNICHE_DI_IMPASTO = 'Tecniche di Impasto'
    SURGELAMENTO = 'Surgelamento'

    BOLLITURA = 'Bollitura'
    GRIGLIARE = 'Grigliare'
    FORNO = 'Forno'
    VAPORE = 'Vapore'
    SOTTOVUOTO = 'Sottovuoto'
    SALTARE_IN_PADELLA = 'Saltare in Padella'

    DECOSTRUZIONE = 'Decostruzione'
    SFERIFICAZIONE = 'Sferificazione'
    TECNICHE_DI_TAGLIO = 'Tecniche di Taglio'
