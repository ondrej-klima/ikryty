// src/services/api.js

/**
 * @file api.js
 * @brief Služba pro komunikaci s REST API.
 * 
 * @description
 * Tento modul zapouzdřuje veškerá volání na backend (Axios).
 * Konfigurace `baseURL` a interceptorů (např. pro autentizaci) se řeší globálně mimo tento soubor.
 * 
 * Modul je rozdělen do několika sekcí:
 * 1. **Buildings:** CRUD operace pro budovy a specifické updaty pro jednotlivé kroky průvodce (Step 2 - 7).
 * 2. **Shelter Spaces:** CRUD operace pro úkryty a jejich specifické updaty.
 * 3. **Files:** Upload a mazání příloh (fotky, schémata) pro úkryty i budovy.
 * 4. **Utils:** Pomocné funkce (minDistance) a přehledy (summary).
 */

import axios from 'axios';

// The configuration (baseURL, interceptors) is now handled globally,
// so we can directly define the API methods.

const api = {

  // ============================
  // Building Endpoints (Stavby)
  // ============================

  /**
   * Fetches a list of all buildings.
   * @returns {Promise<AxiosResponse<Array>>}
   */
  /**
   * Získá seznam všech budov.
   * @public
   * @method getAllBuildings
   * @returns {Promise<AxiosResponse<Array>>} Pole objektů budov.
   */
  getAllBuildings() {
    return axios.get('/buildings/');
  },

  /**
   * Fetches a single building by its database ID.
   * @param {number} buildingId
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Získá detail jedné budovy podle ID.
   * Obsahuje vnořená data (úkryty, parametry kroků).
   * @public
   * @method getBuilding
   * @param {number|string} buildingId - ID budovy.
   * @returns {Promise<AxiosResponse<Object>>} Objekt budovy.
   */
  getBuilding(buildingId) {
    return axios.get(`/buildings/${buildingId}`);
  },

  /**
   * Creates a new building (corresponds to Step A1).
   * @param {Object} buildingData - (BuildingInSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Vytvoří novou budovu (Krok 1 - Základní údaje).
   * @public
   * @method createBuilding
   * @param {Object} buildingData - Data pro vytvoření (BuildingInSchema).
   * @returns {Promise<AxiosResponse<Object>>} Vytvořená budova.
   */
  createBuilding(buildingData) {
    return axios.post('/buildings/', buildingData);
  },

  /**
   * Updates a building with a generic payload.
   * Ideal for updating Step A1 data or general edits.
   * @param {number} buildingId - The ID of the building to update.
   * @param {Object} buildingData - The data to update.
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje obecná data budovy.
   * Vhodné pro úpravu dat z kroku 1 nebo generické změny.
   * @public
   * @method updateBuilding
   * @param {number|string} buildingId - ID budovy.
   * @param {Object} buildingData - Data k aktualizaci.
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  updateBuilding(buildingId, buildingData) {
    return axios.patch(`/buildings/${buildingId}/`, buildingData); // Předpokládáme obecný PATCH endpoint
  },

  /**
   * Deletes a building by its ID.
   * @param {number} buildingId
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Smaže budovu podle ID.
   * Smazání budovy kaskádově smaže i všechny její úkryty.
   * @public
   * @method deleteBuilding
   * @param {number|string} buildingId - ID budovy.
   * @returns {Promise<AxiosResponse<Object>>} Potvrzení smazání.
   */
  deleteBuilding(buildingId) {
    return axios.delete(`/buildings/${buildingId}`);
  },

  // --- Step-specific Building Updates ---

  /**
   * Updates a building's Step 2 data (Risk Analysis).
   * @param {number} buildingId
   * @param {Object} data - (BuildingStep2UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data budovy pro Krok 2 (Analýza rizik).
   * @public
   * @method updateBuildingStep2
   * @param {number|string} buildingId - ID budovy.
   * @param {Object} data - Data (BuildingStep2UpdateSchema: risk_area, risk_justification).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  updateBuildingStep2(buildingId, data) {
    return axios.patch(`/buildings/${buildingId}/step2`, data);
  },

  /**
   * Updates a building's Step 3 data (Minimum Standards).
   * @param {number} buildingId
   * @param {Object} data - (BuildingStep3UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data budovy pro Krok 3 (Minimální standardy / RS3).
   * @public
   * @method updateBuildingStep3
   * @param {number|string} buildingId - ID budovy.
   * @param {Object} data - Data (BuildingStep3UpdateSchema: deficiency, deficiency_justification).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  updateBuildingStep3(buildingId, data) {
    return axios.patch(`/buildings/${buildingId}/step3`, data);
  },

  /**
   * Updates a building's Step 4 data (Structural Assessment).
   * @param {number} buildingId
   * @param {Object} data - (BuildingStep4UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data budovy pro Krok 4 (Stavební posouzení / RS4).
   * @public
   * @method updateBuildingStep4
   * @param {number|string} buildingId - ID budovy.
   * @param {Object} data - Data (BuildingStep4UpdateSchema: wall_material, wall_thickness, s_ok, s_sd, s_is...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  updateBuildingStep4(buildingId, data) {
    return axios.patch(`/buildings/${buildingId}/step4`, data);
  },

  /**
   * Updates a building's Step 7 data (Review and Approval).
   * @param {number} buildingId
   * @param {Object} data - (BuildingStep7UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data budovy pro Krok 7 (Revize a schválení).
   * @public
   * @method updateBuildingStep7
   * @param {number|string} buildingId - ID budovy.
   * @param {Object} data - Data (BuildingStep7UpdateSchema: last_control_date, approver...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  updateBuildingStep7(buildingId, data) {
    return axios.patch(`/buildings/${buildingId}/step7`, data);
  },

  // ===================================
  // Shelter Space Endpoints (Úkryty)
  // ===================================

  /**
   * Creates a new shelter space within a building (corresponds to Step A3).
   * @param {Object} shelterData - (ShelterInSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Vytvoří nový úkryt v rámci budovy (Krok 3 - Identifikace).
   * @public
   * @method createShelter
   * @param {Object} shelterData - Data úkrytu (ShelterInSchema). Musí obsahovat building_id.
   * @returns {Promise<AxiosResponse<Object>>} Vytvořený úkryt.
   */
  createShelter(shelterData) {
    return axios.post('/shelter_spaces/', shelterData);
  },
  
  /**
   * Deletes a shelter space by its ID.
   * @param {number} shelterId
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Smaže úkryt podle ID.
   * @public
   * @method deleteShelter
   * @param {number|string} shelterId - ID úkrytu.
   * @returns {Promise<AxiosResponse<Object>>} Potvrzení smazání.
   */
  deleteShelter(shelterId) {
    return axios.delete(`/shelter_spaces/${shelterId}`);
  },
  
  // --- Step-specific Shelter Updates ---
  
  /**
   * Updates a shelter's Step 3 data (Identification).
   * @param {number} shelterId
   * @param {Object} data - (ShelterInSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data úkrytu pro Krok 3 (Identifikace / RIÚ1).
   * @public
   * @method updateShelterStep3
   * @param {number|string} shelterId - ID úkrytu.
   * @param {Object} data - Data (ShelterInSchema: code, area, height...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt.
   */
  updateShelterStep3(shelterId, data) {
    return axios.patch(`/shelter_spaces/${shelterId}/step3`, data);
  },

  /**
   * Updates a shelter's Step 4 data (Structural Score).
   * @param {number} shelterId
   * @param {Object} data - (ShelterStep4UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data úkrytu pro Krok 4 (Stavební skóre / RIÚ2).
   * @public
   * @method updateShelterStep4
   * @param {number|string} shelterId - ID úkrytu.
   * @param {Object} data - Data (ShelterStep4UpdateSchema: s_pu, s_chuc...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt.
   */
  updateShelterStep4(shelterId, data) {
    return axios.patch(`/shelter_spaces/${shelterId}/step4`, data);
  },

  /**
   * Updates a shelter's Step 5 data (Threat Assessment).
   * @param {number} shelterId
   * @param {Object} data - (ShelterStep5UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data úkrytu pro Krok 5 (Posouzení ohroženosti / RIÚ3).
   * @public
   * @method updateShelterStep5
   * @param {number|string} shelterId - ID úkrytu.
   * @param {Object} data - Data (ShelterStep5UpdateSchema: distance_to_target...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt.
   */
  updateShelterStep5(shelterId, data) {
    return axios.patch(`/shelter_spaces/${shelterId}/step5`, data);
  },

  /**
   * Updates a shelter's Step 6 data (Overall Assessment).
   * @param {number} shelterId
   * @param {Object} data - (ShelterStep6UpdateSchema)
   * @returns {Promise<AxiosResponse<Object>>}
   */
    /**
   * Aktualizuje data úkrytu pro Krok 6 (Celkové hodnocení / RIÚ4).
   * @public
   * @method updateShelterStep6
   * @param {number|string} shelterId - ID úkrytu.
   * @param {Object} data - Data (ShelterStep6UpdateSchema: s_c, iu_class...).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt.
   */
  updateShelterStep6(shelterId, data) {
    return axios.patch(`/shelter_spaces/${shelterId}/step6`, data);
  },

  // --- Photo Upload/Delete Functions ---
  /**
   * Uploads one or more photos for a specific shelter.
   * @param {number} shelterId The ID of the shelter.
   * @param {File[]} files An array of File objects from the input.
   * @returns {Promise<AxiosResponse<Object>>} The updated shelter object.
   */
    /**
   * Nahraje jednu nebo více fotografií k úkrytu.
   * @public
   * @method uploadShelterPhotos
   * @param {number|string} shelterId - ID úkrytu.
   * @param {File[]} files - Pole souborů (fotografií) z inputu.
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt (s cestami k fotkám).
   */
  uploadShelterPhotos(shelterId, files) {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    return axios.post(`/shelter_spaces/${shelterId}/photos`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * Deletes a specific photo from a shelter.
   * @param {number} shelterId The ID of the shelter.
   * @param {string} filename The name of the file to delete.
   * @returns {Promise<AxiosResponse<Object>>} A status message.
   */
    /**
   * Smaže konkrétní fotografii úkrytu.
   * @public
   * @method deleteShelterPhoto
   * @param {number|string} shelterId - ID úkrytu.
   * @param {string} filename - Název souboru ke smazání.
   * @returns {Promise<AxiosResponse<Object>>} Status.
   */
  deleteShelterPhoto(shelterId, filename) {
    return axios.delete(`/shelter_spaces/${shelterId}/photos/${encodeURIComponent(filename)}`);
  },

    /**
   * Uploads one or more schema files for a specific shelter.
   * @param {number} shelterId The ID of the shelter.
   * @param {File[]} files The File objects from the input.
   * @returns {Promise<AxiosResponse<Object>>} The updated shelter object.
   */
   /**
   * Nahraje schémata/plány k úkrytu.
   * @public
   * @method uploadShelterSchemas
   * @param {number|string} shelterId - ID úkrytu.
   * @param {File[]} files - Pole souborů (schémat).
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaný úkryt.
   */
  uploadShelterSchemas(shelterId, files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return axios.post(`/shelter_spaces/${shelterId}/schemas`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * Deletes a specific schema file from a shelter.
   * @param {number} shelterId The ID of the shelter.
   * @param {string} filename The name of the file to delete.
   * @returns {Promise<AxiosResponse<Object>>} A status message.
   */
    /**
   * Smaže konkrétní schéma úkrytu.
   * @public
   * @method deleteShelterSchema
   * @param {number|string} shelterId - ID úkrytu.
   * @param {string} filename - Název souboru.
   * @returns {Promise<AxiosResponse<Object>>} Status.
   */
  deleteShelterSchema(shelterId, filename) {
    return axios.delete(`/shelter_spaces/${shelterId}/schemas/${encodeURIComponent(filename)}`);
  },

    /**
   * Nahraje přílohy k parametru S_SD (Stavební spáry) budovy.
   * @public
   * @method uploadBuildingSsdAttachments
   * @param {number|string} buildingId - ID budovy.
   * @param {File[]} files - Pole souborů.
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
   uploadBuildingSsdAttachments(buildingId, files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return axios.post(`/buildings/${buildingId}/ssd_attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
    /**
   * Smaže přílohu S_SD budovy.
   * @public
   * @method deleteBuildingSsdAttachment
   * @param {number|string} buildingId - ID budovy.
   * @param {string} filename - Název souboru.
   * @returns {Promise<AxiosResponse<Object>>} Status.
   */
  deleteBuildingSsdAttachment(buildingId, filename) {
    return axios.delete(`/buildings/${buildingId}/ssd_attachments/${encodeURIComponent(filename)}`);
  },
  
    /**
   * Nahraje přílohy k parametru S_IS (Instalační šachty) budovy.
   * @public
   * @method uploadBuildingSisAttachments
   * @param {number|string} buildingId - ID budovy.
   * @param {File[]} files - Pole souborů.
   * @returns {Promise<AxiosResponse<Object>>} Aktualizovaná budova.
   */
  uploadBuildingSisAttachments(buildingId, files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return axios.post(`/buildings/${buildingId}/sis_attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  /**
   * Smaže přílohu S_IS budovy.
   * @public
   * @method deleteBuildingSisAttachment
   * @param {number|string} buildingId - ID budovy.
   * @param {string} filename - Název souboru.
   * @returns {Promise<AxiosResponse<Object>>} Status.
   */
  deleteBuildingSisAttachment(buildingId, filename) {
    return axios.delete(`/buildings/${buildingId}/sis_attachments/${encodeURIComponent(filename)}`);
  },

  /**
   * Zjistí minimální vzdálenost zadaného bodu (budovy) k nejbližšímu definovanému cíli útoku.
   * Používá se pro výpočet koeficientu ohroženosti ($S_O$).
   * @public
   * @method minDistance
   * @param {number} lat - Zeměpisná šířka.
   * @param {number} lon - Zeměpisná délka.
   * @returns {Promise<AxiosResponse<Object>>} Objekt { d: number }.
   */
  minDistance(lat, lon) {
    return axios.get(`/min_distance/${lat}/${lon}`);
  },

  /**
   * Fetches a summary list of all buildings, each including the highest
   * s_c score from its associated shelters.
   * @returns {Promise<AxiosResponse<Array>>}
   */
    /**
   * Získá souhrnný seznam všech budov (Summary).
   * Každá budova obsahuje agregované informace (např. nejvyšší $S_C$ skóre ze svých úkrytů).
   * Vhodné pro zobrazení v tabulce/dashboardu.
   * @public
   * @method getBuildingsSummary
   * @returns {Promise<AxiosResponse<Array>>} Pole sumarizovaných objektů budov.
   */
  getBuildingsSummary() {
    return axios.get('/buildings/summary');
  },

  /**
   * Stáhne Excel export viditelných budov a úkrytů.
   * @public
   * @method exportBuildingsWorkbook
   * @param {{ building_ids: number[] }} filterPayload - Filtrované ID budov k exportu.
   * @returns {Promise<AxiosResponse<Blob>>} Excel soubor jako blob.
   */
  exportBuildingsWorkbook(filterPayload) {
    return axios.post('/buildings/export/xlsx', filterPayload, {
      responseType: 'blob',
    });
  },
};

export default api;