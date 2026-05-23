from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Targets, Shelters, BuildingType, BuildingSubType, MaterialType, MaterialSubType, ProtectiveSpace
from src.schemas.shelters import ShelterOutSchema, BuildingTypeOutSchema, BuildingSubTypeOutSchema
from src.schemas.shelters import MaterialTypeOutSchema, MaterialSubTypeOutSchema, ProtectiveSpaceOutSchema
from src.schemas.token import Status
from src.schemas.targets import TargetOutSchema
import numpy as np
from scipy.spatial import KDTree

import pyproj

async def get_user_shelters(current_user):
    if 'supervisor' in current_user.get("realm_access", {}).get("roles", []):
        return await ShelterOutSchema.from_queryset(Shelters.all())
    else:
        shelters = Shelters.filter(user=current_user['preferred_username'])
        return await ShelterOutSchema.from_queryset(shelters)


async def get_shelters():
    return await ShelterOutSchema.from_queryset(Shelters.all())


async def create_shelter(shelter, current_user) -> ShelterOutSchema:
    crs_wgs84 = pyproj.CRS("EPSG:4326")
    crs_s_jtsk = pyproj.CRS("EPSG:5514")

    transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_s_jtsk, always_xy=True)

    x, y = transformer.transform(shelter['y'], shelter['x'])

    shelter_dict = {
        'user': current_user['preferred_username'],
        'address': shelter['address'],
        'name': shelter['name'],
        'x': shelter['x'],
        'y': shelter['y'],
        'building_subtype_id': shelter['buildingSubType'],
        'x_sjtsk': x,
        'y_sjtsk': y,
        'TP': shelter['TP'],
        'NC': shelter['NC'],
        'NV': shelter['NV'],
        'SOV': shelter['SOV'],
        'SV': shelter['SV'],
        'SO': shelter['SO'],
        'SC': shelter['SC']
    }

    shelter_obj = await Shelters.create(**shelter_dict)

    protective_space_dict = {
        'shelter_id': shelter_obj.id,
        'type': shelter['type'],
        'width': shelter['width'],
        'height': shelter['height'],
        'depth': shelter['depth'],
        'thickness': shelter['thickness'],
        'material_subtype_id': shelter['materialSubType']
    }

    await ProtectiveSpace.create(**protective_space_dict)
    return await ShelterOutSchema.from_tortoise_orm(shelter_obj)

    # shelter_dict = shelter.dict(exclude_unset=True)
    # shelter_dict['user_id'] = current_user.id
    # shelter_obj = await Shelters.create(**shelter_dict)
    # return await ShelterOutSchema.from_tortoise_orm(shelter_obj)


async def delete_shelter(shelter_id, current_user) -> Status:
    try:
        db_shelter = await ShelterOutSchema.from_queryset_single(Shelters.get(id=shelter_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Shelter {shelter_id} not found")

    if db_shelter.user == current_user['preferred_username'] or 'supervisor' in current_user.get("realm_access", {}).get("roles", []):
        deleted_count = await Shelters.filter(id=shelter_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Shelter {shelter_id} not found")
        return Status(message=f"Deleted shelter {shelter_id}")  #

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


async def update_shelter(shelter_id, shelter, current_user) -> ShelterOutSchema:
    try:
        db_shelter = await ShelterOutSchema.from_queryset_single(Shelters.get(id=shelter_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Shelter {shelter_id} not found")

    if db_shelter.user == current_user['preferred_username'] or 'supervisor' in current_user.get("realm_access", {}).get("roles", []):

        #print(shelter.dict())

        shelter_dict = {
            #'user': current_user['preferred_username'],
            'address': shelter.dict()['address'],
            'name': shelter.dict()['name'],
            'description': shelter.dict()['description'],
            #'x': shelter.dict()['x'],
            #'y': shelter.dict()['y'],
            'building_subtype_id': shelter.dict()['buildingSubType'],
            'TP': shelter.dict()['TP'],
            'NC': shelter.dict()['NC'],
            'NV': shelter.dict()['NV'],
            'SOV': shelter.dict()['SOV'],
            'SV': shelter.dict()['SV'],
            'SO': shelter.dict()['SO'],
            'SC': shelter.dict()['SC']
        }
        await Shelters.filter(id=shelter_id).update(**shelter_dict)
        # await Shelters.filter(id=shelter_id).update(**shelter.dict(exclude_unset=True))

        db_protective_space = await ProtectiveSpaceOutSchema.from_queryset_single(ProtectiveSpace.get(shelter_id=shelter_id))
        protective_space_dict = {
            'shelter_id': shelter_id,
            'type': shelter.dict()['type'],
            'width': shelter.dict()['width'],
            'height': shelter.dict()['height'],
            'depth': shelter.dict()['depth'],
            'thickness': shelter.dict()['thickness'],
            'material_subtype_id': shelter.dict()['materialSubType']
        }
        await ProtectiveSpace.filter(id=db_protective_space.id).update(**protective_space_dict)

        return await ShelterOutSchema.from_queryset_single(Shelters.get(id=shelter_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def update_shelters_evaluation():
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


async def get_building_types():
    return await BuildingTypeOutSchema.from_queryset(BuildingType.all())


async def get_building_sub_types():
    return await BuildingSubTypeOutSchema.from_queryset(BuildingSubType.all())


async def get_material_types():
    return await MaterialTypeOutSchema.from_queryset(MaterialType.all())


async def get_material_sub_types():
    return await MaterialSubTypeOutSchema.from_queryset(MaterialSubType.all())
