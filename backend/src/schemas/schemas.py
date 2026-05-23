# schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database import models

"""
Tento modul definuje Pydantic schémata (modely) používaná pro validaci vstupních dat (API request)
a serializaci výstupních dat (API response).

Rozdělení:
- **Output Schemas:** Generována automaticky z Tortoise ORM modelů.
- **Input Schemas (Create):** Definují povinná pole pro vytvoření záznamů.
- **Update Schemas:** Definují volitelná pole pro částečné aktualizace (PATCH), rozdělená podle kroků formuláře/metodiky.
"""

# ==============================================================================
# SCHÉMA PRO STAVOVÉ ODPOVĚDI
# ==============================================================================

class Status(BaseModel):
    """
    Jednoduché schéma pro potvrzovací zprávy z API.
    Např. při úspěšném smazání záznamu.
    """
    message: str


# ==============================================================================
# VÝSTUPNÍ SCHÉMATA (pro odpovědi z API)
# ==============================================================================

ShelterOutSchema = pydantic_model_creator(
    models.Shelter,
    name="ShelterOutSchema"
)

BuildingOutSchema = pydantic_model_creator(
    models.Building,
    name="BuildingOutSchema"
)

# NOVÉ schéma specificky pro odpovědi, kde nechceme vnořené úkryty
BuildingSimpleOutSchema = pydantic_model_creator(
    models.Building,
    name="BuildingSimpleOutSchema",
    exclude=("shelters",) # Explicitně vyloučíme zpětný vztah
)

# ==============================================================================
# VSTUPNÍ SCHÉMATA (CREATE)
# ==============================================================================

class BuildingInSchema(BaseModel):
    """
    Vstupní data pro vytvoření nové budovy.
    Obsahuje základní identifikační údaje a parametry, které lze zadat při zakládání.
    """
    building_code: str
    name_address: str
    gps_lat: Optional[float] = None
    gps_long: Optional[float] = None
    s_jtsk_x: Optional[float] = None
    s_jtsk_y: Optional[float] = None
    owner: Optional[str] = None
    administrator: Optional[str] = None
    access_restricted: bool = False
    operation_type: Optional[str] = None
    object_type: Optional[str] = None
    has_underground: bool = False
    has_basement: bool = False
    has_inner_wing: bool = False
    construction_limits: Optional[str] = None
    data_source: Optional[str] = None
    responsible_person: Optional[str] = None


class ShelterInSchema(BaseModel):
    """
    Vstupní data pro vytvoření nového úkrytu.

    Attributes:
        building_id (int): Povinné ID rodičovské budovy.
        shelter_code (str): Unikátní kód úkrytu v rámci budovy.
    """
    building_id: int
    shelter_code: str
    location: Optional[models.ShelterLocation] = None
    area: Optional[float] = None
    height: Optional[float] = None
    obstacles_volume: Optional[float] = None
    expected_persons: Optional[int] = None
    ventilation: Optional[models.VentilationType] = None
    emergency_exits: Optional[str] = None
    power_supply: Optional[models.ResourceStatus] = None
    energy_cutoff: Optional[models.ResourceStatus] = None
    is_chuc: bool = False
    chuc_type: Optional[str] = None
    chuc_length: Optional[float] = None
    chuc_ventilation: Optional[str] = None
    chuc_walls: Optional[str] = None


# ==============================================================================
# VSTUPNÍ SCHÉMATA (UPDATE - DLE JEDNOTLIVÝCH KROKŮ)
# ==============================================================================

class BuildingStep1UpdateSchema(BaseModel):
    """
    Aktualizace údajů budovy - Krok A1 (Základní identifikace a dispozice).
    Všechna pole jsou volitelná (Optional) pro PATCH requesty.
    """
    # building_code se obvykle nemění, ale pro flexibilitu ho zde můžeme povolit
    building_code: Optional[str] = None
    name_address: Optional[str] = None
    gps_lat: Optional[float] = None
    gps_long: Optional[float] = None
    s_jtsk_x: Optional[float] = None
    s_jtsk_y: Optional[float] = None
    owner: Optional[str] = None
    administrator: Optional[str] = None
    access_restricted: Optional[bool] = None
    operation_type: Optional[str] = None
    object_type: Optional[str] = None
    has_underground: Optional[bool] = None
    has_basement: Optional[bool] = None
    has_inner_wing: Optional[bool] = None
    construction_limits: Optional[str] = None
    data_source: Optional[str] = None
    responsible_person: Optional[str] = None

class BuildingStep2UpdateSchema(BaseModel):
    """Aktualizace údajů budovy - Krok A2 (Analýza území a rizika)."""
    risk_area: Optional[str] = None
    risk_justification: Optional[str] = None


class BuildingStep3UpdateSchema(BaseModel):
    """Aktualizace údajů budovy - Krok A3 (Minimální standardy a nedostatky)."""
    deficiency: Optional[str] = None
    deficiency_justification: Optional[str] = None


class BuildingStep4UpdateSchema(BaseModel):
    """
    Aktualizace údajů budovy - Krok A4 (Hodnocení odolnosti).
    Zahrnuje materiály stěn a koeficienty (S_OK, S_SD, S_IS).
    """
    wall_material: Optional[str] = None
    wall_thickness: Optional[int] = None
    s_ok: Optional[float] = None
    s_sd: Optional[int] = None
    s_is: Optional[int] = None
    possible_t_upravy_building: Optional[str] = None


class BuildingStep7UpdateSchema(BaseModel):
    """Aktualizace údajů budovy - Krok A7 (Kontrola, revize a schválení)."""
    last_control_date: Optional[date] = None
    control_deficiencies: Optional[str] = None
    approver: Optional[str] = None
    assessment_status: Optional[models.AssessmentStatus] = None
    assessment_date: Optional[date] = None
    review_interval: Optional[str] = None
    next_review_date: Optional[date] = None


class ShelterStep3UpdateSchema(BaseModel):
    """
    Aktualizace údajů úkrytu - Krok A3 (Parametry úkrytu).
    Zahrnuje rozměry, kapacity, ventilaci a CHÚC.
    """
    shelter_code: Optional[str] = None
    location: Optional[models.ShelterLocation] = None
    area: Optional[float] = None
    height: Optional[float] = None
    obstacles_volume: Optional[float] = None
    expected_persons: Optional[int] = None
    ventilation: Optional[models.VentilationType] = None
    emergency_exits: Optional[str] = None
    power_supply: Optional[models.ResourceStatus] = None
    energy_cutoff: Optional[models.ResourceStatus] = None
    is_chuc: Optional[bool] = None
    chuc_type: Optional[str] = None
    chuc_length: Optional[float] = None
    chuc_ventilation: Optional[str] = None
    chuc_walls: Optional[str] = None

class ShelterStep4UpdateSchema(BaseModel):
    """
    Aktualizace údajů úkrytu - Krok A4 (Specifikace odolnosti).
    Koeficienty prostoru (S_PU) a CHÚC (S_CHUC).
    """
    s_pu: Optional[int] = None
    s_chuc: Optional[int] = None


class ShelterStep5UpdateSchema(BaseModel):
    """
    Aktualizace údajů úkrytu - Krok A5 (Ohroženost).
    Vzdálenost k cíli útoku.
    """
    distance_to_target: Optional[int] = None


class ShelterStep6UpdateSchema(BaseModel):
    """
    Aktualizace údajů úkrytu - Krok A6 (Výsledky hodnocení).
    Výsledné skóre S_C a zařazení do třídy (IÚ/KIÚ).
    """
    s_c: Optional[float] = None
    iu_class: Optional[str] = None
    assessment_needed: Optional[str] = None


# ADD THIS NEW SCHEMA
class BuildingSummarySchema(BaseModel):
    """
    Schéma pro souhrnný seznam budov (např. pro zobrazení na mapě).

    Oproti běžnému schématu obsahuje navíc pole `max_s_c`, které reprezentuje
    nejvyšší ochranný koeficient ze všech úkrytů v dané budově.
    """
    id: int
    building_code: str
    user_id: str
    name_address: str
    gps_lat: Optional[float] = None
    gps_long: Optional[float] = None
    max_s_c: Optional[float] = None
    total_n_k: int = 0
    total_n_ks: int = 0
    total_n_kd: int = 0


class BuildingExportFilterSchema(BaseModel):
    building_ids: List[int] = []