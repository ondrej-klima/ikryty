<template>
  <v-tabs-window-item value="shelter-identification-form">
    <v-card flat :loading="isLoading">
      <v-card-text>
        <!-- Informational block -->
        <v-alert
          variant="tonal"
          color="blue-grey"
          class="mb-6"
          border="start"
        >
          <template v-slot:title>
            <div class="font-weight-bold">{{ $t('step3.info.title') }}</div>
          </template>
          <ol class="info-list">
            <li>{{ $t('step3.info.goal1') }}</li>
            <li>{{ $t('step3.info.goal2') }}</li>
            <li>{{ $t('step3.info.goal3') }}</li>
          </ol>
          <v-divider class="my-2"></v-divider>
          <p class="text-caption">
            {{ $t('step3.info.output1') }}<br>
            {{ $t('step3.info.output2') }}<br>
            {{ $t('step3.info.output3') }}
          </p>
        </v-alert>

        <!-- Warning message if no building ID is provided -->
        <v-alert
          v-if="!buildingId"
          type="warning"
          variant="outlined"
          class="mb-6"
          prominent
          border="start"
          icon="mdi-alert-circle-outline"
        >
          {{ $t('step3.no_building_selected') }}
        </v-alert>

        <!-- Dynamic Form 1: Register of Improvised Shelters (RIÚ1) -->
        <div class="d-flex align-center mb-2">
          <p class="font-weight-bold flex-grow-1">{{ $t('step3.form1_title') }}</p>
          <v-btn
            color="primary"
            variant="tonal"
            prepend-icon="mdi-plus-circle-outline"
            @click="addShelterForm"
            :disabled="!buildingId"
          >
            {{ $t('actions.add_shelter') }}
          </v-btn>
        </div>
        
        <v-card
          v-for="(shelter, index) in shelters"
          :key="shelter.id || `new-${index}`"
          class="mb-6"
          variant="outlined"
        >
          <v-card-title class="d-flex align-center bg-grey-lighten-4 py-2">
            <span class="text-subtitle-1">{{ shelter.id ? `${$t('step3.edit_shelter_title')} ${shelter.shelter_code}` : `${$t('step3.new_shelter_title')} #${index + 1}` }}</span>
            <v-spacer></v-spacer>
            <v-btn
              color="error"
              variant="text"
              icon="mdi-delete-outline"
              size="small"
              @click="removeShelter(index)"
            ></v-btn>
          </v-card-title>
          <v-divider></v-divider>
          
          <v-card-text>
            <v-form>
              <v-container class="pa-0">
                <v-row>
                  <!-- All form fields from the A3 shelter form -->
                  <v-col cols="12" md="6"><v-text-field :label="$t('step3.riu4')" :hint="$t('step3.riu4_hint')" persistent-hint v-model="shelter.shelter_code" variant="outlined"></v-text-field></v-col>
                  <v-col cols="12" md="6"><v-select :label="$t('step3.riu5')" :items="['Suterén', 'Vnitřní trakt']" v-model="shelter.location" variant="outlined"></v-select></v-col>
                  <v-col cols="12">
                  
                  <!-- File Management Section -->
                  <v-divider class="my-4"></v-divider>
                  
                  <div v-if="shelter.id">
                    <!-- Schema Management -->
                    <p class="font-weight-medium mb-2">{{ $t('step3.riu6') }}</p>
                    <div v-if="shelter.schema_path && shelter.schema_path.length > 0" class="mb-4">
                      <v-chip v-for="path in shelter.schema_path" :key="path" class="mr-2 mb-2" closable @click:close="handleSchemaDelete(index, path)">
                        <a :href="getFileUrl(path)" target="_blank" class="text-decoration-none text-black">
                          <v-icon start icon="mdi-file-document-outline"></v-icon>
                          {{ getFileName(path) }}
                        </a>
                      </v-chip>
                    </div>
                    <div v-else class="text-caption text-medium-emphasis">Žádná schémata nebyla nahrána.</div>
                    <div class="d-flex align-center">
                      <v-file-input v-model="shelter.schemasToUpload" label="Přidat schémata" multiple dense hide-details variant="outlined" class="mr-4"></v-file-input>
                      <v-btn color="success" icon="mdi-upload" :disabled="!shelter.schemasToUpload || shelter.schemasToUpload.length === 0" :loading="shelter.isUploadingSchema" @click="handleSchemaUpload(index)"></v-btn>
                    </div>

                    <v-divider class="my-4"></v-divider>

                    <!-- Photo Management -->
                    <p class="font-weight-medium mb-2">{{ $t('step3.riu7') }}</p>
                    <div v-if="shelter.photo_paths && shelter.photo_paths.length > 0" class="mb-4">
                      <v-chip v-for="path in shelter.photo_paths" :key="path" class="mr-2 mb-2" closable @click:close="handlePhotoDelete(index, path)">
                        <a :href="getFileUrl(path)" target="_blank" class="text-decoration-none text-black">
                          <v-icon start icon="mdi-camera"></v-icon>
                          {{ getFileName(path) }}
                        </a>
                      </v-chip>
                    </div>
                    <div v-else class="text-caption text-medium-emphasis">Žádné fotografie nebyly nahrány.</div>
                    <div class="d-flex align-center">
                      <v-file-input v-model="shelter.photosToUpload" label="Přidat fotografie" multiple dense hide-details variant="outlined" class="mr-4"></v-file-input>
                      <v-btn color="success" icon="mdi-upload" :disabled="!shelter.photosToUpload || shelter.photosToUpload.length === 0" :loading="shelter.isUploadingPhotos" @click="handlePhotoUpload(index)"></v-btn>
                    </div>
                  </div>

                  <div v-else class="text-caption text-blue-grey">
                    Nejprve uložte úkryt, abyste mohli nahrávat soubory.
                  </div>
                  </v-col>
                        
                  <v-col cols="12" md="4"><v-text-field :label="$t('step3.riu8')" suffix="m²" type="number" v-model.number="shelter.area" variant="outlined"></v-text-field></v-col>
                  <v-col cols="12" md="4"><v-text-field :label="$t('step3.riu9')" suffix="m" type="number" v-model.number="shelter.height" variant="outlined"></v-text-field></v-col>
                  <v-col cols="12" md="4"><v-text-field :label="$t('step3.riu10')" :hint="$t('step3.riu10_hint')" persistent-hint suffix="m³" type="number" v-model.number="shelter.obstacles_volume" variant="outlined"></v-text-field></v-col>
 
                  <v-col cols="12"><v-divider class="my-2"></v-divider></v-col>

                  <!-- ADDED: Calculated fields -->
                  <v-col cols="12" md="3"><v-text-field :label="$t('step3.riu11')" v-model="shelter.usable_volume" readonly variant="outlined" bg-color="grey-lighten-5" suffix="m³" :hint="$t('step3.riu11_hint')" persistent-hint></v-text-field></v-col>
                  <v-col cols="12" md="3"><v-text-field :label="$t('step3.riu12')" v-model="shelter.capacity_short" readonly variant="outlined" bg-color="grey-lighten-5" :hint="$t('step3.riu12_hint')" persistent-hint></v-text-field></v-col>
                  <v-col cols="12" md="3"><v-text-field :label="$t('step3.riu13')" v-model="shelter.capacity_medium" readonly variant="outlined" bg-color="grey-lighten-5" :hint="$t('step3.riu13_hint')" persistent-hint></v-text-field></v-col>
                  <v-col cols="12" md="3"><v-text-field :label="$t('step3.riu14')" v-model="shelter.capacity_long" readonly variant="outlined" bg-color="grey-lighten-5" :hint="$t('step3.riu14_hint')" persistent-hint></v-text-field></v-col>
                  
                  <v-col cols="12"><v-divider class="my-2"></v-divider></v-col>

                  <v-col cols="12" md="6"><v-text-field :label="$t('step3.riu15')" :hint="$t('step3.riu15_hint')" persistent-hint type="number" v-model.number="shelter.expected_persons" variant="outlined"></v-text-field></v-col>
                  <v-col cols="12" md="6"><v-select :label="$t('step3.riu16')" :items="['Přirozené', 'Přetlak', 'Chybí']" v-model="shelter.ventilation" variant="outlined"></v-select></v-col>
                  <v-col cols="12" md="12"><v-textarea :label="$t('step3.riu17')" :hint="$t('step3.riu17_hint')" persistent-hint v-model="shelter.emergency_exits" variant="outlined" rows="2"></v-textarea></v-col>
                  <v-col cols="12" md="6"><v-select :label="$t('step3.riu18')" :items="['V dosahu', 'Chybí']" v-model="shelter.power_supply" variant="outlined"></v-select></v-col>
                  <v-col cols="12" md="6"><v-select :label="$t('step3.riu19')" :items="['V dosahu', 'Chybí']" v-model="shelter.energy_cutoff" variant="outlined"></v-select></v-col>
                  <v-col cols="12">
                    <v-checkbox v-model="shelter.is_chuc" :label="$t('step3.isChuc_label')" hide-details></v-checkbox>
                  </v-col>
                  <template v-if="shelter.is_chuc">
                    <v-col cols="12" md="4"><v-select :label="$t('step3.riu20')" :items="['A', 'B', 'C']" v-model="shelter.chuc_type" variant="outlined"></v-select></v-col>
                    <v-col cols="12" md="4"><v-text-field :label="$t('step3.riu21')" suffix="m" type="number" v-model.number="shelter.chuc_length" variant="outlined"></v-text-field></v-col>
                    <v-col cols="12" md="4"><v-select :label="$t('step3.riu22')" :items="['Přirozené otvory', 'Přetlak']" v-model="shelter.chuc_ventilation" variant="outlined"></v-select></v-col>
                    <v-col cols="12"><v-textarea :label="$t('step3.riu23')" :hint="$t('step3.riu23_hint')" persistent-hint v-model="shelter.chuc_walls" variant="outlined" rows="2"></v-textarea></v-col>
                  </template>
                </v-row>
              </v-container>
            </v-form>

            
             <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" :loading="shelter.isSaving" @click="saveShelter(index)">Uložit tento úkryt</v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>

        <v-alert
          v-if="shelters.length > 0"
          :color="totalCapacityColor"
          :icon="totalCapacityIcon"
          variant="tonal"
          class="mb-8"
          border="start"
        >
          <template v-slot:title>
            <div class="font-weight-bold">Celková krátkodobá kapacita (N_K)</div>
          </template>
          Celkový součet kapacity (RIÚ_12) pro všechny definované úkryty v této budově je <strong>{{ totalShortTermCapacity }}</strong> osob.
          <div v-if="totalShortTermCapacity < 50" class="mt-2 text-caption">
            Upozornění: Celková kapacita je nižší než doporučených 50 osob. Stavba může být v dalším kroku vyřazena.
          </div>
        </v-alert>

        <v-divider class="my-8"></v-divider>

        <!-- Form 2: Building Register (RS3) -->
        <p class="font-weight-bold mb-2">{{ $t('step3.form2_title') }}</p>
        <v-form>
           <v-container class="pa-0">
            <v-row>
              <v-col cols="12"><v-textarea v-model="buildingData.deficiency" :label="$t('step3.rs15')" :hint="$t('step3.rs15_hint')" persistent-hint variant="outlined" rows="2" :disabled="!buildingId"></v-textarea></v-col>
              <v-col cols="12"><v-textarea v-model="buildingData.deficiency_justification" :label="$t('step3.rs16')" :hint="$t('step3.rs16_hint')" persistent-hint variant="outlined" rows="3" :disabled="!buildingId"></v-textarea></v-col>
            </v-row>
          </v-container>
        </v-form>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step3.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step3.procedure.title') }}</p>
          <ol class="procedure-list">
            <li v-for="i in 4" :key="i">{{ $t(`step3.procedure.step${i}`) }}</li>
          </ol>
        </v-sheet>
        
        <!-- Static tables in expansion panels -->
        <div class="static-tables">
          <h3 class="text-h6 mb-4">{{ $t('step3.tables_title') }}</h3>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step3.panel_titles.table1') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step3.table1.title') }}</p>
                <v-table density="compact" class="refined-table" hover>
                  <thead><tr><th>{{ $t('step3.table1.headers.col1') }}</th><th>{{ $t('step3.table1.headers.col2') }}</th></tr></thead>
                  <tbody><tr v-for="(item, i) in table1Data" :key="i"><td>{{ item.space }}</td><td>{{ item.requirements }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step3.panel_titles.table2') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step3.table2.title') }}</p>
                <v-table density="compact" class="refined-table" hover>
                  <thead><tr><th>{{ $t('step3.table2.headers.col1') }}</th><th>{{ $t('step3.table2.headers.col2') }}</th><th>{{ $t('step3.table2.headers.col3') }}</th><th>{{ $t('step3.table2.headers.col4') }}</th><th>{{ $t('step3.table2.headers.col5') }}</th><th>{{ $t('step3.table2.headers.col6') }}</th></tr></thead>
                  <tbody><tr v-for="(item, i) in table2Data" :key="i"><td>{{ item.type }}</td><td>{{ item.length }}</td><td>{{ item.envelope }}</td><td>{{ item.doors }}</td><td>{{ item.ventilation }}</td><td>{{ item.note }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
        
        <v-divider class="my-6"></v-divider>
        <!-- Form Actions for the RS3 part -->
        <v-row>
          <v-col class="d-flex justify-end">
            <v-btn color="primary" :loading="isSavingBuilding" @click="saveBuildingData" :disabled="!buildingId">
              Uložit údaje o stavbě (RS3)
            </v-btn>
          </v-col>
        </v-row>

        <!-- Snackbars -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000" location="top right"> {{ alertMessage }} </v-snackbar>
        <v-snackbar v-model="showErrorAlert" color="error" timeout="5000" location="top right" multi-line> {{ alertMessage }} </v-snackbar>
      </v-card-text>
    </v-card>
  </v-tabs-window-item>
</template>

<script>
/**
 * @file ShelterIdentificationForm.vue
 * @brief Formulář pro identifikaci úkrytů a stavební nedostatky (Krok 3).
 * 
 * @description
 * Tato komponenta slouží jako třetí krok v procesu evidence budovy. Má dvě hlavní části:
 * 
 * 1. **Evidence improvizovaných úkrytů (RIÚ):**
 *    - Umožňuje přidávat, editovat a mazat více úkrytů v rámci jedné budovy.
 *    - Automaticky vypočítává kapacity (krátkodobé, střednědobé, dlouhodobé) na základě rozměrů.
 *    - Zajišťuje nahrávání příloh (schémata a fotografie) ke konkrétním úkrytům.
 *    - Zobrazuje souhrnnou kapacitu a varuje, pokud je pod limitem.
 * 
 * 2. **Údaje o stavbě (RS3):**
 *    - Formulář pro zadání stavebních nedostatků a jejich zdůvodnění.
 * 
 * Komponenta vyžaduje `buildingId` a komunikuje s API pro úkryty i budovu.
 * 
 * @component
 * @example
 * <shelter-identification-form 
 *    :building-id="123" 
 *    @building-updated="handleUpdate"
 * />
 */

/**
 * @event building-updated
 * @brief Vyvoláno po úspěšném uložení údajů o stavbě (část RS3).
 * @param {Number|String} id - ID budovy.
 */


import api from '@/services/api';
import { useShelterStore } from '@/stores/shelterStore';

/**
 * Vytvoří prázdný objekt úkrytu s výchozími hodnotami.
 * @returns {Object} Prázdný objekt úkrytu.
 */
const createEmptyShelter = () => ({
  id: null, isSaving: false,
  isUploadingPhotos: false, photosToUpload: [],
  isUploadingSchema: false, schemaToUpload: [],
  shelter_code: '', location: null, schema_path: [], photo_paths: [],
  area: null, height: null, obstacles_volume: null,
  expected_persons: null, ventilation: null, emergency_exits: '', power_supply: null, energy_cutoff: null,
  is_chuc: false, chuc_type: null, chuc_length: null, chuc_ventilation: null, chuc_walls: '',
});

export default {
  name: 'ShelterIdentificationForm',
  props: {
    /**
     * ID budovy, ke které se úkryty vztahují.
     * Povinný údaj pro fungování formuláře.
     */
    buildingId: { type: [Number, String], required: true, default: null },
  },
  data() {
    return {
      isLoading: false, isSavingBuilding: false, shelters: [],
      buildingData: { deficiency: '', deficiency_justification: '' },
      showSuccessAlert: false, showErrorAlert: false, alertMessage: '',
      apiBaseUrl: process.env.VUE_APP_API_BASE_URL || 'https://api.civildefense.fit.vutbr.cz',
      table1Data: [
        { space: 'Suterénní prostor', requirements: 'Nesmí mít dřevěný strop. Je vybudován únikový výlez nebo jej lze dobudovat.' },
        { space: 'Vnitřní trakt', requirements: 'Nesmí mít dřevěný strop. Vyžaduje se min. tloušťka obvodové zdi 450 mm (zděné) nebo 300 mm (betonové).' },
      ],
      table2Data: [
        { type: 'A', length: '22,5 m', envelope: 'REI 30–45', doors: 'EI 30-C', ventilation: 'přirozené otvory ≥ 2 m²', note: 'pro objekty ≤ 30 m' },
        { type: 'B', length: '30 m', envelope: 'REI 45', doors: 'kouřotěsné Sa/S200', ventilation: 'přirozené otvory ≥ 2 m²', note: 'základní typ' },
        { type: 'C', length: '45 m', envelope: 'REI 60', doors: 'kouřotěsné Sa/S200', ventilation: 'přetlakové VZT ≥ 25 Pa', note: 'výškové budovy' },
      ],
    };
  },
  methods: {
    // ADDED: New method for calculation
        /**
     * Vypočítá využitelný objem a kapacity úkrytu na základě zadaných rozměrů.
     * Automaticky se volá při změně dat ve formuláři (watch).
     * 
     * @param {Object} shelter - Objekt úkrytu k přepočítání.
     * @public
     * @method calculateCapacities
     * @return {void}
     */
    calculateCapacities(shelter) {
      const area = shelter.area || 0;
      const height = shelter.height || 0;
      const obstacles = shelter.obstacles_volume || 0;

      const volume = (area * height) - obstacles;

      if (volume > 0) {
        shelter.usable_volume = parseFloat(volume.toFixed(2));
        shelter.capacity_short = Math.floor(volume / 3);
        shelter.capacity_medium = Math.floor(volume / 5);
        shelter.capacity_long = Math.floor(volume / 8);
      } else {
        shelter.usable_volume = null;
        shelter.capacity_short = null;
        shelter.capacity_medium = null;
        shelter.capacity_long = null;
      }
    },

     /**
     * Načte seznam úkrytů a data o budově (RS3) z API.
     * Pokud není ID budovy, vyresetuje formuláře.
     * 
     * @public
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      if (!this.buildingId) {
        this.shelters = []; this.buildingData = { deficiency: '', deficiency_justification: '' };
        return;
      }
      this.isLoading = true;
      try {
        const response = await api.getBuilding(this.buildingId);
        this.shelters = response.data.shelters.map(s => ({ ...createEmptyShelter(), ...s })) || [];
        this.buildingData.deficiency = response.data.deficiency || '';
        this.buildingData.deficiency_justification = response.data.deficiency_justification || '';
      } catch (error) { this.handleApiError(error); } finally { this.isLoading = false; }
    },

    /**
     * Přidá nový (prázdný) formulář úkrytu do seznamu.
     * 
     * @public
     * @method addShelterForm
     */
    addShelterForm() { this.shelters.push(createEmptyShelter()); },

    /**
     * Odstraní úkryt ze seznamu.
     * Pokud je úkryt již uložen v DB, provede API volání pro smazání.
     * Vyžaduje potvrzení uživatelem.
     * 
     * @param {number} index - Index úkrytu v poli shelters.
     * @public
     * @method removeShelter
     * @return {Promise<void>}
     */
    async removeShelter(index) {
      const shelter = this.shelters[index];
      if (!shelter) return;
      if (!shelter.id) { this.shelters.splice(index, 1); return; }
      if (confirm(`Opravdu si přejete smazat úkryt ${shelter.shelter_code}?`)) {
        shelter.isSaving = true;
        try {
          await api.deleteShelter(shelter.id);
          this.shelters.splice(index, 1);
          this.alertMessage = 'Úkryt byl úspěšně smazán.'; this.showSuccessAlert = true;
        } catch (error) {
          this.handleApiError(error);
          if (this.shelters[index]) this.shelters[index].isSaving = false;
        }
      }
    },

    /**
     * Uloží konkrétní úkryt na server (Vytvoření nebo Aktualizace).
     * Rozlišuje mezi POST a PATCH podle přítomnosti ID.
     * Aktualizuje stav úkrytu v poli po úspěšném uložení.
     * 
     * @param {number} index - Index úkrytu v poli shelters.
     * @public
     * @method saveShelter
     * @return {Promise<void>}
     */
    async saveShelter(index) {
      const shelter = this.shelters[index];
      if (!shelter) return;
      shelter.isSaving = true;

      try {
        const toNullIfEmpty = (value) => (value === '' || value === undefined ? null : value);
        const payload = {
            shelter_code: shelter.shelter_code, building_id: this.buildingId, location: shelter.location,
            area: toNullIfEmpty(shelter.area), height: toNullIfEmpty(shelter.height),
            obstacles_volume: toNullIfEmpty(shelter.obstacles_volume),
            expected_persons: toNullIfEmpty(shelter.expected_persons),
            ventilation: shelter.ventilation, emergency_exits: shelter.emergency_exits,
            power_supply: shelter.power_supply, energy_cutoff: shelter.energy_cutoff,
            is_chuc: shelter.is_chuc, chuc_type: shelter.chuc_type,
            chuc_length: toNullIfEmpty(shelter.chuc_length),
            chuc_ventilation: shelter.chuc_ventilation, chuc_walls: shelter.chuc_walls,
        };

        let response;
        if (shelter.id) {
          response = await api.updateShelterStep3(shelter.id, payload);
          this.alertMessage = `Změny v úkrytu '${shelter.shelter_code}' byly uloženy.`;
        } else {
          response = await api.createShelter(payload);
          this.alertMessage = 'Nový úkryt byl úspěšně vytvořen.';
        }
        
        this.shelters.splice(index, 1, { ...shelter, ...response.data, isSaving: false, filesToUpload: [], schemaToUpload: null });
        this.showSuccessAlert = true;

      } catch (error) { this.handleApiError(error); } finally { if(this.shelters[index]) this.shelters[index].isSaving = false; }
      await useShelterStore().getUserShelters();
    },
    /**
     * Uloží data o stavebních nedostatcích (sekce RS3).
     * Volá API endpoint pro update budovy a emituje událost.
     * 
     * @public
     * @method saveBuildingData
     * @return {Promise<void>}
     */
    async saveBuildingData() {
        if (!this.buildingId) return;
        this.isSavingBuilding = true;
        try {
            await api.updateBuildingStep3(this.buildingId, this.buildingData);
            this.alertMessage = 'Údaje o stavbě (RS3) byly uloženy.'; this.showSuccessAlert = true;
            this.$emit('building-updated', this.buildingId);
        } catch (error) { this.handleApiError(error); } finally { this.isSavingBuilding = false; }
    },

     /**
     * Sestaví absolutní URL pro přístup k souboru.
     * 
     * @param {string} relativePath - Relativní cesta k souboru.
     * @public
     * @method getFileUrl
     * @return {string} Absolutní URL.
     */
    getFileUrl(relativePath) {
      if (!relativePath) return '#';
      return `${this.apiBaseUrl}/uploads/${relativePath.replace(/\\/g, '/')}`;
    },

    /**
     * Získá název souboru z cesty.
     * 
     * @param {string} path - Cesta k souboru.
     * @public
     * @method getFileName
     * @return {string} Název souboru.
     */
    getFileName(path) { if (!path) return ''; return path.split(/[\\/]/).pop(); },

    /**
     * Nahraje vybrané fotografie k úkrytu.
     * 
     * @param {number} index - Index úkrytu.
     * @public
     * @method handlePhotoUpload
     * @return {Promise<void>}
     */
    async handlePhotoUpload(index) {
      const shelter = this.shelters[index];
      if (!shelter.id || !shelter.photosToUpload || shelter.photosToUpload.length === 0) return;
      shelter.isUploadingPhotos = true;
      try {
        const response = await api.uploadShelterPhotos(shelter.id, shelter.photosToUpload);
        shelter.photo_paths = response.data.photo_paths;
        shelter.photosToUpload = [];
        this.alertMessage = 'Fotografie byly úspěšně nahrány.'; this.showSuccessAlert = true;
      } catch (error) { this.handleApiError(error); } finally { shelter.isUploadingPhotos = false; }
    },

     /**
     * Smaže fotografii úkrytu.
     * 
     * @param {number} index - Index úkrytu.
     * @param {string} path - Cesta k fotografii.
     * @public
     * @method handlePhotoDelete
     * @return {Promise<void>}
     */
    async handlePhotoDelete(index, path) {
      const shelter = this.shelters[index];
      const filename = this.getFileName(path);
      if (!shelter.id || !filename) return;
      if (confirm(`Opravdu si přejete smazat fotografii '${filename}'?`)) {
        try {
          await api.deleteShelterPhoto(shelter.id, filename);
          shelter.photo_paths = shelter.photo_paths.filter(p => p !== path);
          this.alertMessage = 'Fotografie byla smazána.'; this.showSuccessAlert = true;
        } catch (error) { this.handleApiError(error); }
      }
    },

    /**
     * Nahraje vybraná schémata/plány k úkrytu.
     * 
     * @param {number} index - Index úkrytu.
     * @public
     * @method handleSchemaUpload
     * @return {Promise<void>}
     */
    async handleSchemaUpload(index) {
      const shelter = this.shelters[index];
      if (!shelter.id || !shelter.schemasToUpload || shelter.schemasToUpload.length === 0) return;
      shelter.isUploadingSchema = true;
      try {
        const response = await api.uploadShelterSchemas(shelter.id, shelter.schemasToUpload);
        shelter.schema_path = response.data.schema_path;
        shelter.schemasToUpload = [];
        this.alertMessage = 'Schémata byla úspěšně nahrána.'; this.showSuccessAlert = true;
      } catch (error) { this.handleApiError(error); } finally { shelter.isUploadingSchema = false; }
    },

    /**
     * Smaže schéma úkrytu.
     * 
     * @param {number} index - Index úkrytu.
     * @param {string} path - Cesta ke schématu.
     * @public
     * @method handleSchemaDelete
     * @return {Promise<void>}
     */
    async handleSchemaDelete(index, path) {
      const shelter = this.shelters[index];
      const filename = this.getFileName(path);
      if (!shelter.id || !filename) return;
      if (confirm(`Opravdu si přejete smazat schéma '${filename}'?`)) {
        try {
          await api.deleteShelterSchema(shelter.id, filename);
          shelter.schema_path = shelter.schema_path.filter(p => p !== path);
          this.alertMessage = 'Schéma bylo smazáno.'; this.showSuccessAlert = true;
        } catch (error) { this.handleApiError(error); }
      }
    },

     /**
     * Zpracuje chyby z API volání.
     * Řeší validační chyby (422) i serverové chyby.
     * 
     * @param {Object} error - Objekt chyby.
     * @public
     * @method handleApiError
     * @return {void}
     */
    handleApiError(error) {
      if (error.response) {
        if (error.response.status === 422 && error.response.data.detail) {
            const firstError = error.response.data.detail[0];
            this.alertMessage = `Chyba validace v poli '${firstError.loc.slice(-1)}': ${firstError.msg}`;
        } else {
            this.alertMessage = `Chyba serveru: ${error.response.data.detail || error.response.statusText}`;
        }
      } else if (error.request) {
        this.alertMessage = 'Chyba sítě: Server neodpovídá.';
      } else {
        this.alertMessage = 'Nastala neočekávaná chyba.';
      }
      this.showErrorAlert = true; console.error("API Error:", error);
    },
  },
  mounted() {
    this.initializeForm();
  },
  computed: {
    /**
     * Vypočítá celkovou krátkodobou kapacitu všech úkrytů.
     * Slouží pro sumární statistiku a validaci.
     * @type {number}
     */
    totalShortTermCapacity() {
      return this.shelters.reduce((total, shelter) => {
        // Add the capacity_short if it's a valid number, otherwise add 0
        return total + (Number(shelter.capacity_short) || 0);
      }, 0);
    },

    /**
     * Určuje barvu upozornění podle celkové kapacity (zelená/červená).
     * @type {string}
     */
    totalCapacityColor() {
      return this.totalShortTermCapacity >= 50 ? 'success' : 'error';
    },

    /**
     * Určuje ikonu upozornění podle celkové kapacity.
     * @type {string}
     */
    totalCapacityIcon() {
      return this.totalShortTermCapacity >= 50 ? '$success' : '$error';
    }
  },
  watch: {
     /**
     * Při změně ID budovy znovu načte celý formulář.
     */
    buildingId: {
      handler() {
        this.initializeForm();
      },
    },
     /**
     * Hluboké sledování změn v poli shelters.
     * Při jakékoliv změně dat v úkrytu přepočítá jeho kapacity.
     */
    shelters: {
      handler(newShelters) {
        newShelters.forEach(shelter => {
          this.calculateCapacities(shelter);
        });
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.info-list { padding-left: 20px; }
.procedure-list { padding-left: 20px; font-size: 0.875rem; }
.procedure-list li { margin-bottom: 8px; padding-left: 4px; }
.procedure-list li:last-child { margin-bottom: 0; }
.static-tables .refined-table { border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)); border-radius: 8px; overflow: hidden; }
.static-tables .refined-table :deep(thead) { background-color: rgb(var(--v-theme-surface-variant)); }
.static-tables .refined-table :deep(thead th) { font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; color: rgb(var(--v-theme-on-surface-variant)); }
.static-tables .refined-table :deep(tbody tr:nth-child(even)) { background-color: rgba(var(--v-theme-surface-variant), 0.3); }
.static-tables .refined-table :deep(tbody tr td) { border-bottom: none !important; }
</style>