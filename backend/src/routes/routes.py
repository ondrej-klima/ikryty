from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from typing import List, Dict, Any

# Importujte schémata, CRUD funkce a autentizační závislost
from src.crud import crud
from src.schemas import schemas
from src.auth.auth import get_current_user
from fastapi.security import OAuth2AuthorizationCodeBearer

from fastapi import UploadFile, File

"""
Tento modul definuje všechny API endpointy (routes) aplikace.
Zprostředkovává komunikaci mezi HTTP požadavky a logikou v `crud.py`.

Zahrnuje:
- Operace nad budovami (Buildings)
- Operace nad úkryty (Shelter Spaces)
- Nahrávání a mazání souborů (fotografie, schémata, přílohy)
- Autentizaci pomocí Keycloak
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

# ==============================================================================
# ENDPOINTY PRO STAVBY (BUILDINGS)
# ==============================================================================

@router.post("/buildings/", response_model=schemas.BuildingSimpleOutSchema, tags=["Buildings"])
async def create_building(
    building: schemas.BuildingInSchema,
    token: str = Depends(oauth2_scheme)
):
    """
    Vytvoří novou budovu v registru.

    Args:
        building (schemas.BuildingInSchema): Data nové budovy.
        token (str): OAuth2 token (získán automaticky z hlavičky).

    Returns:
        schemas.BuildingSimpleOutSchema: Vytvořená budova (základní údaje).
    """
    current_user = await get_current_user(token)
    return await crud.create_building(building_in=building, current_user=current_user)

@router.get("/buildings/", response_model=List[schemas.BuildingOutSchema], tags=["Buildings"])
async def get_all_buildings():
    """
    Vrátí seznam všech evidovaných budov.

    Returns:
        List[schemas.BuildingOutSchema]: Seznam budov včetně detailů.
    """
    return await crud.get_all_buildings()

@router.get("/buildings/{building_id}", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def get_building(
    building_id: int,
    token: str = Depends(oauth2_scheme)
):
    """
    Vrátí detailní informace o konkrétní budově.

    Args:
        building_id (int): ID budovy.
    """
    current_user = await get_current_user(token)
    return await crud.get_building(building_id=building_id, current_user=current_user)

@router.delete("/buildings/{building_id}", response_model=schemas.Status, tags=["Buildings"])
async def delete_building(
    building_id: int,
    token: str = Depends(oauth2_scheme)
):
    """
    Smaže budovu a všechny její podřízené úkryty.

    Args:
        building_id (int): ID budovy ke smazání.
    """
    current_user = await get_current_user(token)
    return await crud.delete_building(building_id=building_id, current_user=current_user)

# --- Specializované UPDATE endpointy pro stavby ---

@router.patch(
    "/buildings/{building_id}/", # Cesta bez '/stepX'
    response_model=schemas.BuildingOutSchema,
    tags=["Buildings"],
    summary="Obecná aktualizace stavby (pro krok A1)"
)
async def update_building(
    building_id: int,
    data_in: schemas.BuildingStep1UpdateSchema, # Použijte nové schéma
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace základních identifikačních údajů budovy (Krok 1)."""
    current_user = await get_current_user(token)
    # V crud.py musíte mít také odpovídající obecnou update funkci
    return await crud.update_building_step1(building_id, data_in, current_user)

@router.patch("/buildings/{building_id}/step2", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def update_building_step2(
    building_id: int,
    data_in: schemas.BuildingStep2UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace konstrukčních údajů budovy (Krok 2)."""
    current_user = await get_current_user(token)
    return await crud.update_building_step2(building_id, data_in, current_user)

@router.patch("/buildings/{building_id}/step3", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def update_building_step3(
    building_id: int,
    data_in: schemas.BuildingStep3UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace údajů o okolí budovy (Krok 3)."""
    current_user = await get_current_user(token)
    return await crud.update_building_step3(building_id, data_in, current_user)

@router.patch("/buildings/{building_id}/step4", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def update_building_step4(
    building_id: int,
    data_in: schemas.BuildingStep4UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace doplňkových údajů budovy (Krok 4)."""
    current_user = await get_current_user(token)
    return await crud.update_building_step4(building_id, data_in, current_user)

@router.patch("/buildings/{building_id}/step7", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def update_building_step7(
    building_id: int,
    data_in: schemas.BuildingStep7UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace revizních údajů budovy (Krok 7)."""
    current_user = await get_current_user(token)
    return await crud.update_building_step7(building_id, data_in, current_user)

# ==============================================================================
# ENDPOINTY PRO PROSTORY ÚKRYTŮ (SHELTER SPACES)
# ==============================================================================

@router.post("/shelter_spaces/", response_model=schemas.ShelterOutSchema, tags=["Shelter Spaces"])
async def create_shelter_space(
    shelter: schemas.ShelterInSchema,
    token: str = Depends(oauth2_scheme)
):
    """
    Vytvoří nový úkryt v rámci existující budovy.

    Args:
        shelter (schemas.ShelterInSchema): Data úkrytu (musí obsahovat building_id).
    """
    current_user = await get_current_user(token)
    return await crud.create_shelter(shelter_in=shelter, current_user=current_user)

@router.delete("/shelter_spaces/{shelter_id}", response_model=schemas.Status, tags=["Shelter Spaces"])
async def delete_shelter_space(
    shelter_id: int,
    token: str = Depends(oauth2_scheme)
):
    """Smaže konkrétní úkryt."""
    current_user = await get_current_user(token)
    return await crud.delete_shelter(shelter_id=shelter_id, current_user=current_user)

# --- Specializované UPDATE endpointy pro prostory úkrytů ---

@router.patch("/shelter_spaces/{shelter_id}/step3", response_model=schemas.ShelterOutSchema, tags=["Shelter Spaces"])
async def update_shelter_space_step3(
    shelter_id: int,
    data_in: schemas.ShelterInSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace parametrů úkrytu (Krok 3)."""
    current_user = await get_current_user(token)
    return await crud.update_shelter_step3(shelter_id, data_in, current_user)

@router.patch("/shelter_spaces/{shelter_id}/step4", response_model=schemas.ShelterOutSchema, tags=["Shelter Spaces"])
async def update_shelter_space_step4(
    shelter_id: int,
    data_in: schemas.ShelterStep4UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace specifikací úkrytu (Krok 4)."""
    current_user = await get_current_user(token)
    return await crud.update_shelter_step4(shelter_id, data_in, current_user)

@router.patch("/shelter_spaces/{shelter_id}/step5", response_model=schemas.ShelterOutSchema, tags=["Shelter Spaces"])
async def update_shelter_space_step5(
    shelter_id: int,
    data_in: schemas.ShelterStep5UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Aktualizace dalších vlastností úkrytu (Krok 5)."""
    current_user = await get_current_user(token)
    return await crud.update_shelter_step5(shelter_id, data_in, current_user)

@router.patch("/shelter_spaces/{shelter_id}/step6", response_model=schemas.ShelterOutSchema, tags=["Shelter Spaces"])
async def update_shelter_space_step6(
    shelter_id: int,
    data_in: schemas.ShelterStep6UpdateSchema,
    token: str = Depends(oauth2_scheme)
):
    """Závěrečná aktualizace úkrytu (Krok 6)."""
    current_user = await get_current_user(token)
    return await crud.update_shelter_step6(shelter_id, data_in, current_user)

@router.post(
    "/shelter_spaces/{shelter_id}/photos",
    response_model=schemas.ShelterOutSchema,
    tags=["Shelter Spaces"],
    summary="Nahrát fotografie k úkrytu"
)
async def upload_shelter_photos(
    shelter_id: int,
    files: List[UploadFile] = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Nahraje jednu nebo více fotografií a přiřadí je k existujícímu úkrytu.

    Args:
        shelter_id (int): ID úkrytu.
        files (List[UploadFile]): Soubory odeslané jako 'multipart/form-data'.
    """
    return await crud.upload_photos_for_shelter(shelter_id, files, current_user)


@router.delete(
    "/shelter_spaces/{shelter_id}/photos/{filename}",
    response_model=schemas.Status,
    tags=["Shelter Spaces"],
    summary="Smazat fotografii u úkrytu"
)
async def delete_shelter_photo(
    shelter_id: int,
    filename: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Smaže specifickou fotografii z databáze a z disku.

    Args:
        shelter_id (int): ID úkrytu.
        filename (str): Název souboru (pouze název, ne celá cesta).
    """
    return await crud.delete_photo_for_shelter(shelter_id, filename, current_user)

@router.post(
    "/shelter_spaces/{shelter_id}/schemas",
    response_model=schemas.ShelterOutSchema,
    tags=["Shelter Spaces"],
    summary="Nahrát schémata k úkrytu"
)
async def upload_shelter_schemas(
    shelter_id: int,
    files: List[UploadFile] = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Nahraje jeden nebo více souborů schémat a přiřadí je k existujícímu úkrytu."""
    return await crud.upload_shelter_schemas(shelter_id, files, current_user)

@router.delete(
    "/shelter_spaces/{shelter_id}/schemas/{filename}",
    response_model=schemas.Status,
    tags=["Shelter Spaces"],
    summary="Smazat schéma u úkrytu"
)
async def delete_shelter_schema(
    shelter_id: int,
    filename: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Smaže specifický soubor schématu z databáze a z disku."""
    return await crud.delete_shelter_schema(shelter_id, filename, current_user)

@router.get(
    "/buildings_summary",
    response_model=List[schemas.BuildingSummarySchema],
    tags=["Buildings"],
    summary="Získat seznam staveb s nejvyšším S_C skóre",
)
async def get_buildings_summary(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Vrátí seznam všech staveb optimalizovaný pro zobrazení na mapě.

    Každá stavba je doplněna o nejvyšší `s_c` skóre (koeficient ochrany)
    ze všech svých přiřazených úkrytů.
    """
    return await crud.get_buildings_summary(current_user)


@router.get(
    "/buildings/export/xlsx",
    tags=["Buildings"],
    summary="Exportovat viditelné budovy a úkryty do Excelu",
)
async def export_buildings_xlsx(current_user: Dict[str, Any] = Depends(get_current_user)):
    workbook_bytes = await crud.export_visible_buildings_and_shelters(current_user)
    return Response(
        content=workbook_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="ikryty-export.xlsx"'
        },
    )


@router.post(
    "/buildings/export/xlsx",
    tags=["Buildings"],
    summary="Exportovat filtrované budovy a úkryty do Excelu",
)
async def export_filtered_buildings_xlsx(
    export_filter: schemas.BuildingExportFilterSchema,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    workbook_bytes = await crud.export_visible_buildings_and_shelters(
        current_user,
        building_ids=export_filter.building_ids,
        target_ids=export_filter.target_ids,
    )
    return Response(
        content=workbook_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="ikryty-export.xlsx"'
        },
    )

@router.post("/buildings/{building_id}/ssd_attachments", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def upload_ssd_attachments(
    building_id: int,
    files: List[UploadFile] = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Nahraje jednu nebo více příloh pro parametr S_SD (dělící spára) budovy."""
    return await crud.upload_building_ssd_attachments(building_id, files, current_user)

@router.delete("/buildings/{building_id}/ssd_attachments/{filename}", response_model=schemas.Status, tags=["Buildings"])
async def delete_ssd_attachment(building_id: int, filename: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Smaže specifickou přílohu pro S_SD."""
    return await crud.delete_building_ssd_attachment(building_id, filename, current_user)

@router.post("/buildings/{building_id}/sis_attachments", response_model=schemas.BuildingOutSchema, tags=["Buildings"])
async def upload_sis_attachments(
    building_id: int,
    files: List[UploadFile] = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Nahraje jednu nebo více příloh pro parametr S_IS (integrita stěn) budovy."""
    return await crud.upload_building_sis_attachments(building_id, files, current_user)

@router.delete("/buildings/{building_id}/sis_attachments/{filename}", response_model=schemas.Status, tags=["Buildings"])
async def delete_sis_attachment(building_id: int, filename: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Smaže specifickou přílohu pro S_IS."""
    return await crud.delete_building_sis_attachment(building_id, filename, current_user)
