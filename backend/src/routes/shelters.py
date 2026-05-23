from typing import List, Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Security
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.auth.auth import get_current_user

import src.crud.shelters as crud

from src.schemas.shelters import ShelterInSchema, ShelterOutSchema, UpdateShelter
from src.schemas.token import Status
from src.schemas.shelters import BuildingTypeOutSchema, BuildingSubTypeOutSchema
from src.schemas.shelters import MaterialTypeOutSchema, MaterialSubTypeOutSchema

from fastapi.security import OAuth2AuthorizationCodeBearer

# --- Configuration ---
KEYCLOAK_URL = "https://civildefense.fit.vutbr.cz:8443"
REALM = "myrealm"

# 1. Define the OAuth2 scheme right here in the router file.
# This object is what FastAPI inspects to build the Swagger UI security requirements.
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token",
    scopes={"roles": "Read user roles"} # Define the scopes that can be requested
)


router = APIRouter()


@router.get(
    "/user_shelters",
    response_model=List[ShelterOutSchema],
    dependencies=[Depends(oauth2_scheme)]
)
async def get_user_shelters(token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)
    return await crud.get_user_shelters(current_user)


@router.get(
    "/shelters",
    response_model=List[ShelterOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_shelters(token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)
    return await crud.get_shelters()

#https://stackoverflow.com/questions/59929028/python-fastapi-error-422-with-post-request-when-sending-json-data
@router.post(
    "/create_shelter",
    response_model=ShelterOutSchema,
    dependencies=[Depends(oauth2_scheme)],
)
async def create_shelter(
        shelter: Dict[Any, Any],
        token: str = Depends(oauth2_scheme)
) -> ShelterOutSchema:
    current_user = await get_current_user(token)
    return await crud.create_shelter(shelter, current_user)


@router.delete(
    "/shelter/{shelter_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_shelter(
    shelter_id: int, token: str = Depends(oauth2_scheme)
):
    current_user = await get_current_user(token)
    return await crud.delete_shelter(shelter_id, current_user)


@router.patch(
    "/shelter/{shelter_id}",
    dependencies=[Depends(oauth2_scheme)],
    response_model=ShelterOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_shelter(
    shelter_id: int,
    shelter: UpdateShelter,
    token: str = Depends(oauth2_scheme)
) -> ShelterOutSchema:
    current_user = await get_current_user(token)
    return await crud.update_shelter(shelter_id, shelter, current_user)


@router.get(
    "/buildingtypes",
    response_model=List[BuildingTypeOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_buildingtypes(token: str = Depends(oauth2_scheme)):
    return await crud.get_building_types()


@router.get(
    "/buildingsubtypes",
    response_model=List[BuildingSubTypeOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_buildingsubtypes(token: str = Depends(oauth2_scheme)):
    return await crud.get_building_sub_types()


@router.get(
    "/materialtypes",
    response_model=List[MaterialTypeOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_materialtypes(token: str = Depends(oauth2_scheme)):
    return await crud.get_material_types()


@router.get(
    "/materialsubtypes",
    response_model=List[MaterialSubTypeOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_materialsubtypes(token: str = Depends(oauth2_scheme)):
    return await crud.get_material_sub_types()

