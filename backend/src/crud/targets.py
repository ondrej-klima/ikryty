from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Targets
from src.schemas.targets import TargetOutSchema
from src.schemas.token import Status

from src.crud.shelters import update_shelters_evaluation

import pyproj

"""
Modul pro správu strategických cílů a geoprostorové výpočty (Targets).

Tento modul implementuje logiku pro evidenci potenciálních cílů útoku (Targets)
a jejich vliv na hodnocení bezpečnosti úkrytů. Je klíčovou součástí systému
pro automatické určování stupně ohrožení (S_O).

Hlavní zodpovědnosti modulu:
----------------------------
1.  **CRUD operace nad cíli:**
    - Vytváření, čtení, editace a mazání strategických cílů.
    - Automatická transformace vstupních GPS souřadnic (WGS-84) do 
      národního systému S-JTSK pomocí knihovny `pyproj`.

2.  **Geoprostorová analýza a hodnocení (KDTree):**
    - Obsahuje funkci `update_shelters_evaluation`, která využívá algoritmus `KDTree`
      (z knihovny `scipy`) pro efektivní vyhledávání nejbližšího souseda.
    - Na základě vzdálenosti úkrytu od nejbližšího cíle automaticky vypočítává:
        - **S_O (Stupeň ohrožení):** 3 (vysoké), 2 (střední) nebo 1 (nízké).
        - **S_C (Koeficient ochrany):** Přepočítává se se zahrnutím penalizace za blízkost cíle.

3.  **Hromadné aktualizace:**
    - Při vytvoření nebo smazání cíle dochází k hromadnému přepočtu hodnocení 
      všech úkrytů v databázi, aby data reflektovala aktuální bezpečnostní situaci.

4.  **Autorizace:**
    - Rozlišuje přístup pro běžné uživatele (vidí/upravují jen své cíle) 
      a pro roli 'supervisor' (vidí/upravuje vše).

Závislosti:
-----------
- `scipy.spatial.KDTree`: Pro rychlé prostorové dotazy.
- `numpy`: Pro efektivní práci s maticemi souřadnic.
- `pyproj`: Pro transformaci souřadnic.
- `src.crud.shelters`: Pro přístup k datům úkrytů při přepočtu.
"""
async def update_shelters_evaluation():
    """
    Přepočítá hodnocení (SO, SC) pro všechny úkryty na základě jejich vzdálenosti k nejbližšímu cíli.

    Tato funkce využívá algoritmus KDTree pro rychlé vyhledávání nejbližšího souseda
    v prostoru souřadnic S-JTSK.

    Vypočítává:
    - **SO (Stupeň ohrožení):**
        - 3 (vysoké) při vzdálenosti < 100 m
        - 2 (střední) při vzdálenosti 100–500 m
        - 1 (nízké) jinak.
    - **SC (Stupeň ochrany / Shelter Coefficient):** Vypočítáno na základě SOV, NC a SO.

    Poznámka:
        Pokud neexistují žádné cíle, nastaví se SO na 1 a SC se přepočítá bez penalizace vzdáleností.
    """

    tar = await TargetOutSchema.from_queryset(Targets.all())
    if len(tar) > 0:
        m = np.asmatrix([(i.x_sjtsk, i.y_sjtsk) for i in tar])
        tree = KDTree(m)
        shelters = await get_shelters()

        for shelter in shelters:
            #print(shelter.dict()["x_sjtsk"], shelter.dict()["y_sjtsk"])
            d, _ = tree.query([shelter.dict()["x_sjtsk"], shelter.dict()["y_sjtsk"]])
            #print(d)

            so = None
            if d < 100:
                so = 3
            elif 100 <= d <= 500:
                so = 2
            else:
                so = 1

            sc = None
            if shelter.dict()['SOV'] and shelter.dict()['NC']:
                sc = round(100 * (500 * shelter.dict()['SOV']) / (shelter.dict()['NC'] * so)) / 100
            shelter_dict = {
                'SO': so,
                'SC': sc
            }
            await Shelters.filter(id=shelter.dict()['id']).update(**shelter_dict)
    else:
        shelters = await get_shelters()
        for shelter in shelters:
            sc = None
            if shelter.dict()['SOV'] and shelter.dict()['NC']:
                sc = round(100 * (500 * shelter.dict()['SOV']) / (shelter.dict()['NC'])) / 100
            shelter_dict = {
                'SO': 1,
                'SC': sc,
            }
            await Shelters.filter(id=shelter.dict()['id']).update(**shelter_dict)

async def get_user_targets(current_user):
    """
    Vrátí seznam cílů dostupných pro aktuálního uživatele.

    - **Supervisor:** Vidí všechny cíle v systému.
    - **Běžný uživatel:** Vidí pouze cíle, které sám vytvořil.

    Args:
        current_user (dict): Data přihlášeného uživatele (z JWT).

    Returns:
        List[TargetOutSchema]: Seznam cílů.
    """

    if 'supervisor' in current_user.get("realm_access", {}).get("roles", []):
        return await TargetOutSchema.from_queryset(Targets.all())
    else:
        targets = Targets.filter(user=current_user['preferred_username'])
        return await TargetOutSchema.from_queryset(targets)


async def get_targets():
    """
    Vrátí seznam všech cílů v systému bez ohledu na oprávnění.

    Returns:
        List[TargetOutSchema]: Seznam všech cílů.
    """
    return await TargetOutSchema.from_queryset(Targets.all())


async def create_target(target, current_user) -> TargetOutSchema:
    """
    Vytvoří nový strategický cíl v databázi.

    Součástí procesu je transformace GPS souřadnic (WGS84) na souřadný systém S-JTSK,
    který se používá pro výpočty vzdáleností v ČR.

    Args:
        target (dict): Vstupní data cíle (name, address, x, y, description).
                       'x' a 'y' zde reprezentují GPS Lat/Lon.
        current_user (dict): Přihlášený uživatel.

    Returns:
        TargetOutSchema: Vytvořený cíl.
    """
    crs_wgs84 = pyproj.CRS("EPSG:4326")
    crs_s_jtsk = pyproj.CRS("EPSG:5514")

    transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_s_jtsk, always_xy=True)

    x, y = transformer.transform(target['y'], target['x'])

    target_dict = {
        'user': current_user['preferred_username'],
        'name': target['name'],
        'address': target['address'],
        'description': target['description'],
        'x': target['x'],
        'y': target['y'],
        'x_sjtsk': x,
        'y_sjtsk': y,
    }

    target_obj = await Targets.create(**target_dict)
    ret = await TargetOutSchema.from_tortoise_orm(target_obj)
    #await update_shelters_evaluation()
    return ret

async def delete_target(target_id, current_user) -> Status:
    """
    Smaže cíl z databáze a spustí přepočet hodnocení úkrytů.

    Args:
        target_id (int): ID cíle ke smazání.
        current_user (dict): Přihlášený uživatel.

    Returns:
        Status: Zpráva o úspěchu.

    Raises:
        HTTPException:
            - 404: Pokud cíl neexistuje.
            - 403: Pokud uživatel nemá oprávnění cíl smazat (není vlastník ani supervisor).
    """
    try:
        db_target = await TargetOutSchema.from_queryset_single(Targets.get(id=target_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Target {target_id} not found")

    if db_target.user == current_user['preferred_username'] or 'supervisor' in current_user.get("realm_access", {}).get("roles", []):
        deleted_count = await Targets.filter(id=target_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Target {target_id} not found")
        await update_shelters_evaluation()
        return Status(message=f"Deleted target {target_id}")  #

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


async def update_target(target_id, target, current_user) -> TargetOutSchema:
    """
    Aktualizuje popisné údaje existujícího cíle.

    Poznámka: Neaktualizuje souřadnice. Pokud se změní poloha, měl by se cíl
    pravděpodobně smazat a vytvořit znovu, nebo by se musel provést nový přepočet S-JTSK.

    Args:
        target_id (int): ID cíle.
        target (Schema): Nová data (name, address, description).
        current_user (dict): Přihlášený uživatel.

    Returns:
        TargetOutSchema: Aktualizovaný cíl.

    Raises:
        HTTPException: 404 (nenalezeno) nebo 403 (nedostatečná práva).
    """
    print('Updating target')
    try:
        db_target = await TargetOutSchema.from_queryset_single(Targets.get(id=target_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Target {target_id} not found")

    if db_target.user == current_user['preferred_username'] or 'supervisor' in current_user.get("realm_access", {}).get("roles", []):

        target_dict = {
            #'user': current_user['preferred_username'],
            'name': target.dict()['name'],
            'address': target.dict()['address'],
            'description': target.dict()['description'],
        }
        await Targets.filter(id=target_id).update(**target_dict)
        return await TargetOutSchema.from_queryset_single(Targets.get(id=target_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")
