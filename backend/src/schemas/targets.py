from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator

from pydantic import BaseModel
from src.database.models import Targets

"""
Tento modul definuje Pydantic schémata pro entitu `Targets` (potenciální cíle).
Využívá helper `pydantic_model_creator` z Tortoise ORM pro automatické generování
schémat na základě definice databázového modelu.
"""

TargetInSchema = pydantic_model_creator(
    Targets, name="TargetIn", exclude=["user_id"], exclude_readonly=True
)
"""
Vstupní schéma pro vytvoření nového cíle.
Automaticky vylučuje pole, která klient nesmí zadat (ID, user_id).
"""

TargetOutSchema = pydantic_model_creator(
    Targets, name="TargetOut"
)
"""
Výstupní schéma pro odeslání dat o cíli klientovi.
Obsahuje všechna pole včetně ID a vypočítaných souřadnic.
"""

TargetDatabaseSchema = pydantic_model_creator(
    Targets, name="Target"
)
"""
Kompletní schéma reprezentující záznam v databázi.
V kontextu tohoto API je často totožné s TargetOutSchema.
"""

class UpdateTarget(BaseModel):
    """
    Schéma pro částečnou aktualizaci cíle (PATCH).
    Všechna pole jsou volitelná.

    Attributes:
        name (Optional[str]): Název cíle.
        description (Optional[str]): Popis cíle.
        address (Optional[str]): Adresa.
        x (Optional[float]): GPS zeměpisná šířka (WGS-84).
        y (Optional[float]): GPS zeměpisná délka (WGS-84).
    """

    name: Optional[str]
    description: Optional[str]
    address: Optional[str]
    x: Optional[float]
    y: Optional[float]


