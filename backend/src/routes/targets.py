from typing import List, Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from src.auth.auth import get_current_user

import src.crud.targets as crud

from src.schemas.targets import TargetInSchema, TargetOutSchema, UpdateTarget
from src.schemas.token import Status

from src.database.models import Targets
import numpy as np
from scipy.spatial import KDTree
import pyproj

from fastapi.security import OAuth2AuthorizationCodeBearer

"""
Tento modul definuje API endpointy pro správu potenciálních cílů.
Zahrnuje operace pro vytváření, čtení, mazání a aktualizaci cílů,
a také specializovaný endpoint pro výpočet vzdáleností.
"""

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
    "/user_targets",
    response_model=List[TargetOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_user_targets(token: str = Depends(oauth2_scheme)):
    """
    Získá seznam cílů, které patří aktuálně přihlášenému uživateli.

    Pokud má uživatel roli 'supervisor', vrátí všechny cíle. V opačném případě
    vrátí pouze ty cíle, které daný uživatel vytvořil.

    Args:
        token (str): OAuth2 token, automaticky injektovaný FastAPI.

    Returns:
        List[TargetOutSchema]: Seznam cílů.
    """
    current_user = await get_current_user(token)
    return await crud.get_user_targets(current_user)

@router.get(
    "/min_distance/{lat}/{lon}",
    response_model=Dict,
    dependencies=[Depends(oauth2_scheme)]
)
async def get_min_distance(lat: float, lon: float, token: str = Depends(oauth2_scheme)):
    """
    Vypočítá a vrátí nejkratší vzdálenost od zadaného bodu (GPS) k nejbližšímu existujícímu cíli.

    Tento endpoint provádí následující kroky:
    1. Načte všechny cíle a jejich souřadnice S-JTSK.
    2. Vytvoří prostorový index (KD-Tree) pro rychlé vyhledávání.
    3. Převede vstupní GPS souřadnice na S-JTSK.
    4. Pomocí KD-Tree najde vzdálenost k nejbližšímu cíli.

    Args:
        lat (float): Zeměpisná šířka (WGS-84).
        lon (float): Zeměpisná délka (WGS-84).

    Returns:
        Dict: Slovník obsahující klíč 'd' s hodnotou vzdálenosti v metrech, nebo None.
    """
    tar = await TargetOutSchema.from_queryset(Targets.all())
    if len(tar) > 0:
        m = np.asmatrix([(i.x_sjtsk, i.y_sjtsk) for i in tar])

        tree = KDTree(m)

        crs_wgs84 = pyproj.CRS("EPSG:4326")
        crs_s_jtsk = pyproj.CRS("EPSG:5514")

        transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_s_jtsk, always_xy=True)

        x, y = transformer.transform(lon, lat)

        d, _ = tree.query([x, y])
        return {'d': d}
    else:
        return {'d': None}

@router.get(
    "/targets",
    response_model=List[TargetOutSchema],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_targets(token: str = Depends(oauth2_scheme)):
    """
    Získá seznam všech cílů v systému. Určeno pro administrátory/supervisory.
    """
    return await crud.get_targets()

#https://stackoverflow.com/questions/59929028/python-fastapi-error-422-with-post-request-when-sending-json-data
@router.post(
    "/create_target",
    response_model=TargetOutSchema,
    dependencies=[Depends(oauth2_scheme)],
)
async def create_target(
        target: Dict[Any, Any],
        current_user: Dict = Depends(get_current_user)
) -> TargetOutSchema:
    """
    Vytvoří nový strategický cíl.

    Poznámka: Tento endpoint přijímá obecný slovník `Dict` místo Pydantic schématu
    `TargetInSchema`. Tím se obchází automatická validace FastAPI, což může
    být záměrné (např. kvůli flexibilitě frontendu), ale je méně bezpečné.

    Args:
        target (Dict[Any, Any]): Slovník s daty pro nový cíl.
        current_user (Dict): Objekt přihlášeného uživatele, injektovaný FastAPI.

    Returns:
        TargetOutSchema: Vytvořený cíl.
    """
    return await crud.create_target(target, current_user)


@router.delete(
    "/target/{target_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_target(
    target_id: int, token: str = Depends(oauth2_scheme)
):
    """
    Smaže cíl na základě jeho ID.

    Vyžaduje, aby byl uživatel vlastníkem cíle nebo měl roli 'supervisor'.
    Po smazání se automaticky spustí přepočet hodnocení všech úkrytů.

    Args:
        target_id (int): ID cíle ke smazání.
    """
    current_user = await get_current_user(token)
    return await crud.delete_target(target_id, current_user)


@router.patch(
    "/target/{target_id}",
    dependencies=[Depends(oauth2_scheme)],
    response_model=TargetOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_target(
    target_id: int,
    target: UpdateTarget,
    token: str = Depends(oauth2_scheme)
) -> TargetOutSchema:
    """
    Aktualizuje data existujícího cíle.

    Umožňuje měnit popisné údaje (název, adresa, popis).
    Nemění souřadnice.

    Args:
        target_id (int): ID cíle k aktualizaci.
        target (UpdateTarget): Pydantic schéma s novými daty.
    """
    current_user = await get_current_user(token)
    return await crud.update_target(target_id, target, current_user)
