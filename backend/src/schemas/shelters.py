from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator

from pydantic import BaseModel
from src.database.models import Shelters, ProtectiveSpace
from src.database.models import BuildingType, BuildingSubType, MaterialType, MaterialSubType

ShelterInSchema = pydantic_model_creator(
    Shelters, name="ShelterIn", exclude=["user_id"], exclude_readonly=True
)

ShelterOutSchema = pydantic_model_creator(
    Shelters, name="ShelterOut"
)

ShelterDatabaseSchema = pydantic_model_creator(
    Shelters, name="Shelter"
)

BuildingTypeOutSchema = pydantic_model_creator(
    BuildingType, name="BuildingTypeOut"
)

BuildingSubTypeOutSchema = pydantic_model_creator(
    BuildingSubType, name="BuildingSubTypeOut"
)

MaterialTypeOutSchema = pydantic_model_creator(
    MaterialType, name="MaterialTypeOut"
)

MaterialSubTypeOutSchema = pydantic_model_creator(
    MaterialSubType, name="MaterialSubTypeOut"
)

ProtectiveSpaceInSchema = pydantic_model_creator(
    ProtectiveSpace, name="ProtectiveSpaceIn"
)

ProtectiveSpaceOutSchema = pydantic_model_creator(
    ProtectiveSpace, name="ProtectiveSpaceOut"
)


#class UpdateShelter(BaseModel):
#    name: Optional[str]
#    x: Optional[float]
#    y: Optional[float]

class UpdateShelter(BaseModel):
    name: Optional[str]
    address: Optional[str]
    description: Optional[str]
    x: Optional[float]
    y: Optional[float]
    buildingType: Optional[int]
    buildingSubType: Optional[int]
    materialType: Optional[int]
    materialSubType: Optional[int]
    width: Optional[float]
    height: Optional[float]
    depth: Optional[float]
    thickness: Optional[float]
    type: Optional[int]
    TP: Optional[int]
    NC: Optional[int]
    NV: Optional[int]
    SOV: Optional[float]
    SV: Optional[int]
    SO: Optional[int]
    SC: Optional[float]