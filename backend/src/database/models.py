import enum
from tortoise import fields, models
from tortoise.validators import MinValueValidator, MaxValueValidator
import datetime

"""
Tento modul definuje databázové modely (schémata) pro aplikaci Civilní obrany / Evidence úkrytů.
Využívá ORM knihovnu Tortoise ORM.

Hlavní součásti:
1. **Registr staveb (RS):** Model `Building`.
2. **Registr improvizovaných úkrytů (RIÚ):** Model `Shelter`.
3. **Pomocné číselníky:** `AssessmentStatus`, `ShelterLocation`, `VentilationType` a `ResourceStatus`.
4. **Geoprostorová data:** Model `Targets` a zjednodušený model `Shelters` pro výpočty.
"""

# ==============================================================================
# ENUMERACE (pro zajištění datové konzistence)
# ==============================================================================

class AssessmentStatus(str, enum.Enum):
    """Stav odborného posouzení stavby."""
    COMPLETED = "Provedeno"
    PLANNED = "Plánování"
    NO = "Ne"


class ShelterLocation(str, enum.Enum):
    """Umístění úkrytu v rámci budovy."""
    BASEMENT = "Suterén"
    INNER_WING = "Vnitřní trakt"


class VentilationType(str, enum.Enum):
    """Typ ventilace v úkrytu."""
    NATURAL = "Přirozené"
    OVERPRESSURE = "Přetlak"
    MISSING = "Chybí"


class ResourceStatus(str, enum.Enum):
    """Dostupnost zdroje (elektřina, voda, atd.)."""
    AVAILABLE = "V dosahu"
    MISSING = "Chybí"


# ==============================================================================
# MODEL STAVBY (REGISTR STAVEB - RS)
# ==============================================================================

class Building(models.Model):
    """
    Model reprezentující jednu stavbu v registru staveb (RS).

    Tento model slouží jako rodičovská entita pro jednotlivé úkryty (`Shelter`).
    Obsahuje základní identifikační údaje, GPS souřadnice, informace o konstrukci
    a hodnocení odolnosti budovy (koeficienty S_OK, S_SD, S_IS).

    Attributes:
        id (int): Primární klíč.
        building_code (str): Unikátní kód stavby zadaný uživatelem.
        shelters (ReverseRelation): Vztah 1:N na model `Shelter`.
    """
    # Systémová pole
    id = fields.IntField(pk=True, description="Unikátní ID záznamu v databázi")
    user_id = fields.CharField(max_length=255, index=True,
                               description="ID uživatele, který záznam vytvořil/naposledy upravil")

    # KROK A1: Identifikace
    building_code = fields.CharField(max_length=50, unique=True, index=True,
                                     description="RS_1: Identifikační kód stavby (vkládaný uživatelem)")
    name_address = fields.TextField(description="RS_2: Název / adresa stavby")
    gps_lat = fields.FloatField(null=True, description="RS_3: GPS souřadnice (šířka, WGS-84)")
    gps_long = fields.FloatField(null=True, description="RS_3: GPS souřadnice (délka, WGS-84)")
    s_jtsk_x = fields.FloatField(null=True, description="Souřadnice X v systému S-JTSK")
    s_jtsk_y = fields.FloatField(null=True, description="Souřadnice Y v systému S-JTSK")
    owner = fields.CharField(max_length=255, null=True, description="RS_4: Vlastník stavby")
    administrator = fields.CharField(max_length=255, null=True, description="RS_5: Správce stavby")
    access_restricted = fields.BooleanField(default=False, description="RS_6: Předběžné omezení vstupu")
    operation_type = fields.CharField(max_length=100, null=True, description="RS_7: Typ provozu")
    object_type = fields.CharField(max_length=100, null=True, description="RS_7: Typ objektu / účel stavby")
    has_underground = fields.BooleanField(default=False, description="RS_8: Dostupnost podzemí")
    has_basement = fields.BooleanField(default=False, description="RS_8: Dostupnost suterénu")
    has_inner_wing = fields.BooleanField(default=False, description="RS_8: Dostupnost vnitřního traktu")
    construction_limits = fields.TextField(null=True, description="RS_9: Omezení stavebních úprav")
    data_source = fields.TextField(null=True, description="RS_10: Zdroj vstupních dat")
    created_date = fields.DateField(default=datetime.date.today, description="RS_11: Datum vytvoření záznamu")
    responsible_person = fields.CharField(max_length=255, null=True, description="RS_12: Odpovědná osoba")

    # KROK A2: Analýza území
    risk_area = fields.TextField(null=True, description="RS_14: Riziková oblast")
    risk_justification = fields.TextField(null=True, description="RS_15: Odůvodnění zařazení i přes riziko")

    # KROK A3: Minimální standardy
    deficiency = fields.TextField(null=True, description="RS_16: Nedostatek (nesplnění min. standardů)")
    deficiency_justification = fields.TextField(null=True, description="RS_17: Odůvodnění zařazení i přes nedostatek")

    # KROK A4: Hodnocení odolnosti
    wall_material = fields.CharField(max_length=100, null=True, description="RS_18: Konstrukční materiál nosných stěn")
    wall_thickness = fields.IntField(null=True, description="RS_19: Tloušťka nosných stěn [mm]")
    s_ok = fields.FloatField(null=True, description="RS_20: S_OK (Skóre odolnosti konstrukce)")
    s_sd = fields.IntField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)],
                           description="RS_21: S_SD (Skóre dělící spáry)")
    s_sd_attachment = fields.JSONField(null=True, description="RS_22: Příloha k S_SD (seznam cest k souborům)")
    s_is = fields.IntField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)],
                           description="RS_23: S_IS (Skóre integrity nosných stěn)")
    s_is_attachment = fields.JSONField(null=True, description="RS_24: Příloha k S_IS (seznam cest k souborům)")
    possible_t_upravy_building = fields.TextField(null=True, description="RS_25: Možné T-úpravy (Stavba)")

    # KROK A7: Kontrola a revize
    last_control_date = fields.DateField(null=True, description="RS_26: Datum poslední kontroly údajů")
    control_deficiencies = fields.TextField(null=True, description="RS_27: Nedostatky zjištěné při kontrole")
    approver = fields.CharField(max_length=255, null=True, description="RS_28: Schvalovatel")
    assessment_status = fields.CharEnumField(AssessmentStatus, null=True,
                                             description="RS_29: Provedení odborného posouzení")
    assessment_date = fields.DateField(null=True, description="RS_30: Datum odborného posouzení")
    review_interval = fields.CharField(max_length=50, null=True, default="2 roky",
                                       description="RS_29(b): Interval revize")
    next_review_date = fields.DateField(null=True, description="RS_30(b): Datum příští revize")

    # Vztah One-to-Many k úkrytům
    shelters: fields.ReverseRelation["Shelter"]

    def __str__(self):
        return f"[{self.id}] {self.building_code}: {self.name_address}"

    class Meta:
        table = "building_register"
        ordering = ["building_code"]


# ==============================================================================
# MODEL ÚKRYTU (REGISTR IMPROVIZOVANÝCH ÚKRYTŮ - RIÚ)
# ==============================================================================

class Shelter(models.Model):
    """
    Model reprezentující jeden improvizovaný úkryt (IÚ) v rámci stavby.

    Každý záznam je vázán na konkrétní budovu (`building_id`).
    Model obsahuje technické parametry úkrytu, kapacity, vybavení a
    vypočítaná skóre (S_OV, S_O, S_C).
    """
    # Systémová pole
    id = fields.IntField(pk=True, description="Unikátní ID záznamu v databázi")
    user_id = fields.CharField(max_length=255, index=True,
                               description="ID uživatele, který záznam vytvořil/naposledy upravil")

    # Vztah Many-to-One ke stavbě
    building = fields.ForeignKeyField("models.Building", related_name="shelters",
                                      description="Propojení na stavbu (RS)")

    # KROK A3: Identifikace IÚ
    shelter_code = fields.CharField(max_length=60, description="RIÚ_4: Identifikační kód IÚ (např. S1-1)")
    location = fields.CharEnumField(ShelterLocation, null=True, description="RIÚ_5: Umístění IÚ")
    schema_path = fields.JSONField(null=True, description="RIÚ_6: Schéma prostoru (cesta k souboru)")
    photo_paths = fields.JSONField(null=True, description="RIÚ_7: Fotodokumentace (seznam cest k souborům)")
    area = fields.FloatField(null=True, description="RIÚ_8: S [m^2] Plocha IÚ")
    height = fields.FloatField(null=True, description="RIÚ_9: h [m] Světlá výška IÚ")
    obstacles_volume = fields.FloatField(null=True, description="RIÚ_10: V_TP [m^3] Objem trvalých překážek")
    usable_volume = fields.FloatField(null=True, description="RIÚ_11: V [m^3] Užitný objem vzduchu (vypočteno)")
    capacity_short = fields.IntField(null=True, description="RIÚ_12: N_K Kapacita (krátkodobá, <2h)")
    capacity_medium = fields.IntField(null=True, description="RIÚ_13: N_KS Kapacita (střední, 2-6h)")
    capacity_long = fields.IntField(null=True, description="RIÚ_14: N_KD Kapacita (dlouhodobá, >6h)")
    expected_persons = fields.IntField(null=True, description="RIÚ_15: N_KO Očekávaný počet osob")
    ventilation = fields.CharEnumField(VentilationType, null=True, description="RIÚ_16: Větrání")
    emergency_exits = fields.CharField(max_length=255, null=True, description="RIÚ_17: Nouzové východy / výlezy")
    power_supply = fields.CharEnumField(ResourceStatus, null=True, description="RIÚ_18: Elektrická energie")
    energy_cutoff = fields.CharEnumField(ResourceStatus, null=True, description="RIÚ_19: Technická uzávěra energií")

    # CHÚC - Chráněné únikové cesty
    is_chuc = fields.BooleanField(default=False, description="Zda je IÚ v prostoru CHÚC")
    chuc_type = fields.CharField(max_length=1, null=True, description="RIÚ_20: Označení a typ CHÚC (A/B/C)")
    chuc_length = fields.FloatField(null=True, description="RIÚ_21: Skutečná délka trasy CHÚC [m]")
    chuc_ventilation = fields.CharField(max_length=50, null=True, description="RIÚ_22: Způsob větrání CHÚC")
    chuc_walls = fields.TextField(null=True, description="RIÚ_23: Nosné stěny v obálce CHÚC")

    # KROK A4: Hodnocení odolnosti IÚ
    s_pu = fields.IntField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)],
                           description="RIÚ_29: S_PU (Skóre prostoru umístění IÚ)")
    s_chuc = fields.IntField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)],
                             description="RIÚ_30: S_CHUC (Skóre umístění IÚ v CHÚC)")
    s_ov = fields.FloatField(null=True, description="RIÚ_31: S_OV (Skóre ochranných vlastností IÚ, vypočteno)")
    # Pole RIÚ_32 bylo na žádost odstraněno

    # KROK A5: Hodnocení ohroženosti
    distance_to_target = fields.IntField(null=True,
                                         description="RIÚ_33: Vzdálenost od nejbližšího možného terče útoku [m]")
    s_o = fields.IntField(null=True, validators=[MinValueValidator(1), MaxValueValidator(3)],
                          description="RIÚ_34: S_O (Skóre ohroženosti IÚ, vypočteno)")

    # KROK A6: Celkové hodnocení
    s_c = fields.FloatField(null=True, description="RIÚ_35: S_C (Skóre celkové vhodnosti IÚ, vypočteno)")
    iu_class = fields.CharField(max_length=20, null=True, description="RIÚ_36: Třída IÚ")
    assessment_needed = fields.CharField(max_length=3, null=True,
                                         description="RIÚ_37: Nezbytnost provedení odborného posouzení (ANO/NE)")

    def __str__(self):
        return f"[{self.id}] Úkryt {self.shelter_code} v budově {self.building_id}"

    class Meta:
        table = "shelter_register"
        ordering = ["building_id", "shelter_code"]
        # Kód úkrytu musí být unikátní v rámci jedné stavby
        unique_together = (("building", "shelter_code"),)

class Targets(models.Model):
    """
    Model strategických cílů (potenciálních terčů útoku).
    Slouží pro výpočet vzdálenosti úkrytů od nebezpečí a určení skóre ohrožení (S_O).
    """

    id = fields.IntField(pk=True)
    user = fields.CharField(max_length=256, null=False)
    name = fields.CharField(max_length=256, null=True)
    description = fields.TextField(null=True)
    address = fields.CharField(max_length=256, null=True)
    x = fields.FloatField(null=False)
    y = fields.FloatField(null=False)
    x_sjtsk = fields.FloatField(null=False)
    y_sjtsk = fields.FloatField(null=False)


class Shelters(models.Model):
    id = fields.IntField(pk=True)
    user = fields.CharField(max_length=256, null=False)
    address = fields.CharField(max_length=256, null=True)
    x = fields.FloatField(null=False)
    y = fields.FloatField(null=False)
    x_sjtsk = fields.FloatField(null=False)
    y_sjtsk = fields.FloatField(null=False)
    building_subtype = fields.ForeignKeyField('models.BuildingSubType', null=True)
    name = fields.CharField(max_length=256, null=True)
    description = fields.TextField(null=True)
    TP = fields.IntField(null=True)
    NV = fields.IntField(null=True)
    SV = fields.IntField(null=True)
    SOV = fields.FloatField(null=True)
    NC = fields.IntField(null=True)
    SO = fields.IntField(null=True)
    SC = fields.FloatField(null=True)


class BuildingType(models.Model):
    id = fields.IntField(pk=True)
    caption = fields.CharField(max_length=256, null=False)


class BuildingSubType(models.Model):
    id = fields.IntField(pk=True)
    building_type = fields.ForeignKeyField('models.BuildingType')
    caption = fields.CharField(max_length=256, null=False)


class MaterialType(models.Model):
    id = fields.IntField(pk=True)
    caption = fields.CharField(max_length=256, null=False)


class MaterialSubType(models.Model):
    id = fields.IntField(pk=True)
    material_type = fields.ForeignKeyField('models.MaterialType')
    caption = fields.CharField(max_length=256, null=False)


class ProtectiveSpace(models.Model):
    id = fields.IntField(pk=True)
    shelter = fields.ForeignKeyField('models.Shelters')
    type = fields.IntField(null=True)
    width = fields.FloatField(null=True)
    height = fields.FloatField(null=True)
    depth = fields.FloatField(null=True)
    thickness = fields.FloatField(null=True)
    material_subtype = fields.ForeignKeyField('models.MaterialSubType', null=True)