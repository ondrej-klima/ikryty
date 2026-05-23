<template>
  <v-tabs-window-item value="structural-assessment-form">
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
            <div class="font-weight-bold">{{ $t('step4.info.title') }}</div>
          </template>
          <p class="body-2 my-2">{{ $t('step4.info.description') }}</p>
        </v-alert>

        <!-- Warning message if no building is selected -->
        <v-alert v-if="!buildingId" type="warning" variant="outlined" class="mb-6" prominent border="start" icon="mdi-alert-circle-outline">
          {{ $t('step4.no_building_selected', { default: 'Pro tento krok nejprve vyberte nebo vytvořte stavbu.' }) }}
        </v-alert>

        <!-- Form 1: Building Register (RS4) -->
        <p class="font-weight-bold mb-2">{{ $t('step4.form1_title') }}</p>
        <v-form v-model="isBuildingFormValid">
          <v-container class="pa-0">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  :label="$t('step4.rs17')"
                  v-model="buildingData.wall_material"
                  :items="materialOptions"
                  :disabled="!buildingId"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6"><v-text-field :label="$t('step4.rs18')" v-model.number="buildingData.wall_thickness" type="number" suffix="mm" :disabled="!buildingId" variant="outlined"></v-text-field></v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  :label="$t('step4.rs19')"
                  :hint="$t('step4.rs19_hint')"
                  persistent-hint
                  v-model.number="buildingData.s_ok"
                  type="number"
                  step="0.001"
                  :disabled="!buildingId"
                  variant="outlined"
                  readonly
                  bg-color="grey-lighten-5"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4"><v-select :label="$t('step4.rs20')" :hint="$t('step4.rs20_hint')" persistent-hint :items="[{ title: 'Alespoň jedna podezřelá dělící spára', value: 0}, {value: 1, title: 'Žádná podezřelá dělící spára'}]" v-model.number="buildingData.s_sd" :disabled="!buildingId" variant="outlined"></v-select></v-col>
              <v-col cols="12" md="4"><v-select :label="$t('step4.rs22')" :hint="$t('step4.rs22_hint')" persistent-hint :items="[{ title: 'V nosných stěnách jsou nevyztužené otvory/prostupy', value: 0}, { title: 'Žádné nevyztužené otvory', value: 1}]" v-model.number="buildingData.s_is" :disabled="!buildingId" variant="outlined"></v-select></v-col>
              
<!-- Attachment for S_SD (RS_21) - MULTIPLE FILES -->
              <v-col cols="12" v-if="buildingData.s_sd === 0">
                <p class="font-weight-medium mb-1 text-body-2">Přílohy k S_SD (RS_21)</p>
                <div v-if="buildingData.s_sd_attachment && buildingData.s_sd_attachment.length > 0" class="mb-2">
                  <v-chip v-for="path in buildingData.s_sd_attachment" :key="path" class="mr-2 mb-2" closable @click:close="handleAttachmentDelete('s_sd', path)">
                    <a :href="getFileUrl(path)" target="_blank" class="text-decoration-none text-black">
                      <v-icon start icon="mdi-paperclip"></v-icon>
                      {{ getFileName(path) }}
                    </a>
                  </v-chip>
                </div>
                <div class="d-flex align-center">
                  <v-file-input v-model="filesToUpload.s_sd" label="Přidat přílohy" multiple dense hide-details variant="outlined" class="mr-4" :disabled="!buildingId"></v-file-input>
                  <v-btn color="success" icon="mdi-upload" :disabled="!filesToUpload.s_sd || filesToUpload.s_sd.length === 0" :loading="isUploading.s_sd" @click="handleAttachmentUpload('s_sd')"></v-btn>
                </div>
              </v-col>

              <!-- Attachment for S_IS (RS_23) - MULTIPLE FILES -->
              <v-col cols="12" v-if="buildingData.s_is === 0">
                <p class="font-weight-medium mb-1 text-body-2">Přílohy k S_IS (RS_23)</p>
                <div v-if="buildingData.s_is_attachment && buildingData.s_is_attachment.length > 0" class="mb-2">
                   <v-chip v-for="path in buildingData.s_is_attachment" :key="path" class="mr-2 mb-2" closable @click:close="handleAttachmentDelete('s_is', path)">
                    <a :href="getFileUrl(path)" target="_blank" class="text-decoration-none text-black">
                      <v-icon start icon="mdi-paperclip"></v-icon>
                      {{ getFileName(path) }}
                    </a>
                  </v-chip>
                </div>
                 <div class="d-flex align-center">
                  <v-file-input v-model="filesToUpload.s_is" label="Přidat přílohy" multiple dense hide-details variant="outlined" class="mr-4" :disabled="!buildingId"></v-file-input>
                  <v-btn color="success" icon="mdi-upload" :disabled="!filesToUpload.s_is || filesToUpload.s_is.length === 0" :loading="isUploading.s_is" @click="handleAttachmentUpload('s_is')"></v-btn>
                </div>
              </v-col>

              <v-col cols="12"><v-textarea :label="$t('step4.rs24')" :hint="$t('step4.rs24_hint')" persistent-hint v-model="buildingData.possible_t_upravy_building" :disabled="!buildingId" variant="outlined" rows="3"></v-textarea></v-col>
            </v-row>
            <v-row>
              <v-col class="d-flex justify-end">
                <v-btn color="primary" :loading="isSavingBuilding" @click="saveBuildingData" :disabled="!buildingId || !isBuildingFormValid">
                  Uložit údaje o stavbě (RS4)
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        
        <v-divider class="my-8"></v-divider>

        <!-- Dynamic Form 2: Shelter Register (RIÚ2) -->
        <p class="font-weight-bold mb-2">{{ $t('step4.form2_title') }}</p>
        <div v-if="shelters.length === 0 && buildingId" class="text-medium-emphasis">Tato budova zatím nemá žádné úkryty definované v kroku A3.</div>
        
        <v-card v-for="shelter in shelters" :key="shelter.id" class="mb-6" variant="outlined">
          <v-card-title class="bg-grey-lighten-4 py-2">
            <span class="text-subtitle-1">{{ `Hodnocení úkrytu: ${shelter.shelter_code}` }}</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-container class="pa-0">
              <v-row>
                <v-col cols="12" md="6"><v-select :label="$t('step4.riu29')" :hint="$t('step4.riu29_hint')" persistent-hint readonly :items="[{value: 0, title: '0: Prostor ve vnitřním traktu'}, {value: 1, title: '1: Suterénní prostor'}]" v-model.number="shelter.s_pu" variant="outlined"></v-select></v-col>
                <v-col cols="12" md="6"><v-select :label="$t('step4.riu30')" :hint="$t('step4.riu30_hint')" persistent-hint readonly :items="[{value: 0, title: '0: Prostor mimo CHÚC'}, {value: 1, title: '1: Prostor je umístěn uvnitř CHÚC'}]" v-model.number="shelter.s_chuc" variant="outlined"></v-select></v-col>
                <v-col cols="12"><v-text-field :label="$t('step4.riu31')" :hint="$t('step4.riu31_hint')" persistent-hint readonly v-model="shelter.s_ov" variant="outlined" bg-color="grey-lighten-5"></v-text-field></v-col>
              </v-row>
            </v-container>
            <!--
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" :loading="shelter.isSaving" @click="saveShelterAssessment(index)">
                Uložit hodnocení úkrytu
              </v-btn>
            </v-card-actions>
            -->
          </v-card-text>
        </v-card>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step4.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step4.procedure.title') }}</p>
          <ol class="procedure-list">
             <li v-for="i in 6" :key="i">{{ $t(`step4.procedure.step${i}`) }}</li>
          </ol>
        </v-sheet>
        
        <!-- Static tables in expansion panels -->
        <div class="static-tables">
          <h3 class="text-h6 mb-4">{{ $t('step4.tables_title') }}</h3>
          <v-expansion-panels>
            <!-- Panel 1: Resistance Tables -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step4.panel_titles.resistance') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <div v-for="table in resistanceTables" :key="table.titleKey">
                  <p class="font-weight-bold mb-2 mt-4">{{ $t(table.titleKey) }}</p>
                  <v-table density="compact" class="mb-2 refined-table" hover>
                    <thead><tr><th>{{ $t('step4.tables_common.scenario') }}</th><th v-for="header in table.headers" :key="header">{{ header }}</th></tr></thead>
                    <tbody><tr v-for="row in table.rows" :key="row.scenario"><td>{{ row.scenario }}</td><td v-for="(value, i) in row.values" :key="i">{{ value }}</td></tr></tbody>
                  </v-table>
                  <p class="text-caption mb-6" v-html="$t(table.noteKey)"></p>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- Panel 2: Table 3-18 + Manual -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step4.panel_titles.integrity') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step4.table18.title') }}</p>
                <v-table density="compact" class="mb-4 refined-table" hover>
                  <thead><tr><th>{{ $t('step4.table18.headers.h1') }}</th><th>{{ $t('step4.table18.headers.h2') }}</th><th>{{ $t('step4.table18.headers.h3') }}</th></tr></thead>
                  <tbody><tr v-for="(row, i) in $tm('step4.table18.rows')" :key="i"><td>{{ row.score }}</td><td v-html="row.s_sd"></td><td v-html="row.s_is"></td></tr></tbody>
                </v-table>
                <div class="text-body-2">
                  <p v-html="$t('step4.manual18.p1')"></p>
                  <ul class="ml-5 my-2"><li v-for="i in 6" :key="i" v-html="$t(`step4.manual18.l1_${i}`)"></li></ul>
                  <p v-html="$t('step4.manual18.p2')"></p>
                  <ul class="ml-5 my-2"><li v-for="i in 2" :key="i" v-html="$t(`step4.manual18.l2_${i}`)"></li></ul>
                  <p v-html="$t('step4.manual18.p3')"></p>
                  <p class="font-weight-bold mt-2">{{ $t('step4.manual18.sub1') }}</p>
                  <ul class="ml-5 my-2"><li v-for="i in 3" :key="i" v-html="$t(`step4.manual18.l3_${i}`)"></li></ul>
                  <p class="font-weight-bold mt-2">{{ $t('step4.manual18.sub2') }}</p>
                  <ul class="ml-5 my-2"><li v-for="i in 2" :key="i" v-html="$t(`step4.manual18.l4_${i}`)"></li></ul>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
            
            <!-- Panel 3: Table 3-19 -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step4.panel_titles.location') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step4.table19.title') }}</p>
                <v-table density="compact" class="mb-6 refined-table" hover>
                  <thead><tr><th>{{ $t('step4.table19.headers.h1') }}</th><th>{{ $t('step4.table19.headers.h2') }}</th><th>{{ $t('step4.table19.headers.h3') }}</th></tr></thead>
                  <tbody><tr v-for="(row, i) in $tm('step4.table19.rows')" :key="i"><td>{{ row.score }}</td><td>{{ row.s_pu }}</td><td>{{ row.s_chuc }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
        
        <!-- Snackbars -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000" location="top right"> {{ alertMessage }} </v-snackbar>
        <v-snackbar v-model="showErrorAlert" color="error" timeout="5000" location="top right" multi-line> {{ alertMessage }} </v-snackbar>
      </v-card-text>
    </v-card>
  </v-tabs-window-item>
</template>

<script>
/**
 * @file StructuralAssessmentForm.vue
 * @brief Formulář pro stavební posouzení budovy a úkrytů (Krok 4).
 * 
 * @description
 * Tato komponenta slouží jako čtvrtý krok v procesu evidence. Její hlavní funkcí je vyhodnocení
 * odolnosti budovy proti účinkům zbraní (přetlak, radiace, úlomky).
 * 
 * Skládá se ze dvou hlavních částí:
 * 1. **Stavební údaje budovy (RS4):**
 *    - Zadání materiálu a tloušťky obvodového zdiva -> automatický výpočet koeficientu `s_ok`.
 *    - Posouzení dělících spár (`s_sd`) a otvorů v nosných stěnách (`s_is`).
 *    - Správa příloh (fotografie, dokumenty) pro zdůvodnění koeficientů `s_sd` a `s_is`.
 * 
 * 2. **Hodnocení úkrytů (RIÚ2):**
 *    - Zobrazuje seznam úkrytů (načtených z kroku 3).
 *    - Pro každý úkryt vypočítává celkový ochranný koeficient `s_ov` na základě parametrů
 *      budovy a parametrů úkrytu (`s_pu`, `s_chuc`).
 * 
 * Obsahuje také rozsáhlou nápovědu ve formě statických tabulek odolnosti materiálů.
 * 
 * @component
 * @example
 * <structural-assessment-form 
 *    :building-id="123" 
 *    :is-active="true"
 *    @building-updated="handleUpdate"
 * />
 */

/**
 * @event building-updated
 * @brief Vyvoláno po úspěšném uložení údajů o stavebním posouzení.
 * @param {Number|String} id - ID budovy.
 */
import api from '@/services/api';
import { useShelterStore } from '@/stores/shelterStore';

/**
 * Vrací prázdný objekt pro inicializaci dat budovy.
 * @returns {Object} Výchozí hodnoty pro stavební posouzení.
 */
const getInitialBuildingData = () => ({
  wall_material: '', wall_thickness: null, s_ok: null, s_sd: null, s_is: null,
  s_sd_attachment: null, s_is_attachment: null,
  possible_t_upravy_building: '',
});

// Data structure for S_OK calculation
/**
 * Tabulková data pro výpočet koeficientu S_OK (Ochranný koeficient obvodového pláště).
 * Klíče odpovídají hodnotám ve výběrovém poli materiálu.
 * @const {Object}
 */
const materialResistanceData = {
  zelezobeton: { thicknesses: [120, 200, 280, 400], s_ok_scores: [0.125, 0.375, 0.625, 0.875] },
  cpp: { thicknesses: [150, 300, 450, 600], s_ok_scores: [0.0625, 0.25, 0.5, 0.625] },
  vpc: { thicknesses: [175, 240, 300, 365], s_ok_scores: [0.1875, 0.375, 0.5, 0.625] },
  porobeton: { thicknesses: [200, 250, 300, 375], s_ok_scores: [0, 0, 0, 0] },
  dutinova_tvarnice: { thicknesses: [250, 300, 380, 440], s_ok_scores: [0, 0, 0, 0] },
  clt: { thicknesses: [120, 200, 280, 400], s_ok_scores: [0.125, 0.375, 0.5625, 0.75] },
};

export default {
  name: 'StructuralAssessmentForm',
  props: {
     /**
     * ID budovy, ke které se posouzení vztahuje.
     */
    buildingId: { type: [Number, String], required: true, default: null },
     /**
     * Příznak, zda je tento tab aktivní.
     * Slouží k optimalizaci načítání dat (lazy loading).
     */
    isActive: { type: Boolean, default: false },
  },
  data() {
    return {
      isLoading: false, isSavingBuilding: false, isBuildingFormValid: false,
      buildingData: getInitialBuildingData(),
      shelters: [],
      filesToUpload: { s_sd: null, s_is: null },
      isUploading: { s_sd: false, s_is: false },
      showSuccessAlert: false, showErrorAlert: false, alertMessage: '',
      //apiBaseUrl: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000',
      apiBaseUrl: process.env.VUE_APP_API_BASE_URL || 'https://api.civildefense.fit.vutbr.cz',
      materialOptions: [
        { title: 'Železobeton C30/37', value: 'zelezobeton' },
        { title: 'Cihla plná pálená (CPP)', value: 'cpp' },
        { title: 'Vápenopísková cihla (VPC)', value: 'vpc' },
        { title: 'Pórobetonová tvárnice (YTONG/HEBEL)', value: 'porobeton' },
        { title: 'Dutinová tvárnice (POROTHERM)', value: 'dutinova_tvarnice' },
        { title: 'CLT panely (křížem lepené dřevo)', value: 'clt' },
      ],
      resistanceTables: [
        { titleKey: 'step4.table12.title', noteKey: 'step4.tables_common.note1', headers: ['120 mm', '200 mm', '280 mm', '400 mm'], rows: [ { scenario: 'E1', values: [0.5, 1, 1, 1] }, { scenario: 'E2', values: [0, 0.5, 1, 1] }, { scenario: 'E3', values: [0, 0, 0.5, 1] }, { scenario: 'E4', values: [0, 0, 0, 0.5] }, { scenario: 'B1', values: [0.5, 1, 1, 1] }, { scenario: 'B2', values: [0, 0.5, 1, 1] }, { scenario: 'B3', values: [0, 0, 0.5, 1] }, { scenario: 'B4', values: [0, 0, 0, 0.5] }, { scenario: 'S_OK', values: [0.125, 0.375, 0.625, 0.875] } ] },
        { titleKey: 'step4.table13.title', noteKey: 'step4.tables_common.note1', headers: ['150 mm', '300 mm', '450 mm', '600 mm'], rows: [ { scenario: 'E1', values: [0, 0.5, 1, 1] }, { scenario: 'E2', values: [0, 0, 0.5, 0.5] }, { scenario: 'E3', values: [0, 0, 0, 0] }, { scenario: 'E4', values: [0, 0, 0, 0] }, { scenario: 'B1', values: [0.5, 1, 1, 1] }, { scenario: 'B2', values: [0, 0.5, 1, 1] }, { scenario: 'B3', values: [0, 0, 0.5, 1] }, { scenario: 'B4', values: [0, 0, 0, 0.5] }, { scenario: 'S_OK', values: [0.0625, 0.25, 0.5, 0.625] } ] },
        { titleKey: 'step4.table14.title', noteKey: 'step4.tables_common.note1', headers: ['175 mm', '240 mm', '300 mm', '365 mm'], rows: [ { scenario: 'E1', values: [0, 0.5, 1, 1] }, { scenario: 'E2', values: [0, 0, 0.5, 0.5] }, { scenario: 'E3', values: [0, 0, 0, 0] }, { scenario: 'E4', values: [0, 0, 0, 0] }, { scenario: 'B1', values: [1, 1, 1, 1] }, { scenario: 'B2', values: [0.5, 1, 1, 1] }, { scenario: 'B3', values: [0, 0.5, 0.5, 1] }, { scenario: 'B4', values: [0, 0, 0, 0.5] }, { scenario: 'S_OK', values: [0.1875, 0.375, 0.5, 0.625] } ] },
        { titleKey: 'step4.table15.title', noteKey: 'step4.tables_common.note2', headers: ['200 mm', '250 mm', '300 mm', '375 mm'], rows: [ { scenario: 'E1-E4', values: [0, 0, 0, 0] }, { scenario: 'B1-B4', values: [0, 0, 0, 0] }, { scenario: 'S_OK', values: [0, 0, 0, 0] } ] },
        { titleKey: 'step4.table16.title', noteKey: 'step4.tables_common.note2', headers: ['250 mm', '300 mm', '380 mm', '440 mm'], rows: [ { scenario: 'E1-E4', values: [0, 0, 0, 0] }, { scenario: 'B1-B4', values: [0, 0, 0, 0] }, { scenario: 'S_OK', values: [0, 0, 0, 0] } ] },
        { titleKey: 'step4.table17.title', noteKey: 'step4.tables_common.note1', headers: ['120 mm', '200 mm', '280 mm', '400 mm'], rows: [ { scenario: 'E1', values: [0.5, 1, 1, 1] }, { scenario: 'E2', values: [0, 0.5, 1, 1] }, { scenario: 'E3', values: [0, 0, 0, 0.5] }, { scenario: 'E4', values: [0, 0, 0, 0] }, { scenario: 'B1', values: [0.5, 1, 1, 1] }, { scenario: 'B2', values: [0, 0.5, 1, 1] }, { scenario: 'B3', values: [0, 0, 0.5, 1] }, { scenario: 'B4', values: [0, 0, 0, 0.5] }, { scenario: 'S_OK', values: [0.125, 0.375, 0.5625, 0.75] } ] },
      ],
    };
  },
  watch: {
   /**
     * Při změně ID budovy (pokud je tab aktivní) znovu načte data.
     */
    buildingId: {
      handler() { if (this.isActive) this.initializeForm(); },
    },
     /**
     * Při aktivaci tabu načte data, pokud ještě nejsou načtena nebo se změnilo ID.
     */
    isActive: {
      handler(newVal) { if (newVal && this.buildingId) this.initializeForm(); },
      immediate: true,
    },
        // Watchers for reactive calculation of S_OK
    'buildingData.wall_material'() { this.calculateSOK(); },
    'buildingData.wall_thickness'() { this.calculateSOK(); },
    buildingData: { handler() { this.recalculateAllSov(); }, deep: true },
    shelters: { 
      handler() { 
        this.recalculateAllSov(); 
      }, deep: true },
  },
  methods: {
        /**
     * Načte data o budově a jejích úkrytech z API.
     * Kombinuje data z GET /buildings/{id} s výchozími hodnotami.
     * 
     * @public
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      if (!this.buildingId) {
        this.buildingData = getInitialBuildingData(); this.shelters = [];
        return;
      }
      this.isLoading = true;
      try {
        const response = await api.getBuilding(this.buildingId);
        this.buildingData = { ...getInitialBuildingData(), ...response.data };
        this.shelters = response.data.shelters.map(s => ({ ...s, isSaving: false })) || [];
      } catch (error) { this.handleApiError(error); } finally { this.isLoading = false; }
    },

        /**
     * Automaticky vypočítá koeficient S_OK (Ochranný koeficient) na základě materiálu a tloušťky zdi.
     * Používá předdefinovaná data v `materialResistanceData`.
     * Hledá nejbližší nižší tloušťku v tabulce pro daný materiál.
     * 
     * @public
     * @method calculateSOK
     * @return {void}
     */
    calculateSOK() {
      const material = this.buildingData.wall_material;
      const thickness = this.buildingData.wall_thickness;

      if (!material || thickness === null || thickness < 0) {
        this.buildingData.s_ok = null;
        return;
      }

      const tableData = materialResistanceData[material];
      if (!tableData) {
        this.buildingData.s_ok = null;
        return;
      }

      let bestIndex = -1;
      // Find the highest threshold that is less than or equal to the input thickness
      for (let i = 0; i < tableData.thicknesses.length; i++) {
        if (thickness >= tableData.thicknesses[i]) {
          bestIndex = i;
        } else {
          break; // Stop once we exceed the thickness
        }
      }

      if (bestIndex !== -1) {
        this.buildingData.s_ok = tableData.s_ok_scores[bestIndex];
      } else {
        // If thickness is smaller than the lowest threshold, assign the lowest possible score (often 0)
        // For safety, we can take the score of the lowest threshold if that's the desired logic, or null.
        // Let's assign null if below range.
        this.buildingData.s_ok = null;
      }
    },

        /**
     * Přepočítá celkový ochranný koeficient (S_OV) pro všechny úkryty.
     * Vzorec: S_OV = 0.4*S_OK + 0.2*S_SD + 0.1*S_IS + 0.2*S_PU + 0.1*S_CHUC
     * Volá se automaticky při změně jakékoliv vstupní hodnoty (watcher).
     * 
     * @public
     * @method recalculateAllSov
     * @return {void}
     */
    recalculateAllSov() {
      this.shelters.forEach(shelter => {
        const { s_ok, s_sd, s_is } = this.buildingData;
        const { s_pu, s_chuc } = shelter;
        if (s_ok !== null && s_sd !== null && s_is !== null && s_pu !== null && s_chuc !== null) {
          const s_ov = 0.4 * s_ok + 0.2 * s_sd + 0.1 * s_is + 0.2 * s_pu + 0.1 * s_chuc;
          shelter.s_ov = parseFloat(s_ov.toFixed(3));
        } else {
          shelter.s_ov = null;
        }
      });
    },

        /**
     * Uloží data o stavebním posouzení budovy (RS4).
     * Volá endpoint `updateBuildingStep4`.
     * 
     * @public
     * @method saveBuildingData
     * @return {Promise<void>}
     */
    async saveBuildingData() {
      if (!this.isBuildingFormValid || !this.buildingId) return;
      this.isSavingBuilding = true;
      try {
        const toNullIfEmpty = (value) => (value === '' ? null : value);
        const payload = {
          wall_material: this.buildingData.wall_material,
          wall_thickness: toNullIfEmpty(this.buildingData.wall_thickness),
          s_ok: toNullIfEmpty(this.buildingData.s_ok),
          s_sd: this.buildingData.s_sd,
          s_is: this.buildingData.s_is,
          possible_t_upravy_building: this.buildingData.possible_t_upravy_building,
        };
        await api.updateBuildingStep4(this.buildingId, payload);
        this.alertMessage = 'Údaje o stavbě (RS4) byly úspěšně uloženy.';
        this.showSuccessAlert = true;
        this.$emit('building-updated', this.buildingId);
      } catch (error) { this.handleApiError(error); } finally { this.isSavingBuilding = false; }
    },

        /**
     * Uloží hodnocení konkrétního úkrytu.
     * Poznámka: Tato metoda je v šabloně aktuálně zakomentovaná, 
     * protože S_OV se počítá dynamicky a S_PU/S_CHUC jsou readonly.
     * 
     * @param {number} index - Index úkrytu v poli.
     * @public
     * @method saveShelterAssessment
     * @return {Promise<void>}
     */
    async saveShelterAssessment(index) {
      const shelter = this.shelters[index];
      if (!shelter || !shelter.id) return;
      shelter.isSaving = true;
      try {
        const payload = {
          s_pu: shelter.s_pu,
          s_chuc: shelter.s_chuc,
        };
        const response = await api.updateShelterStep4(shelter.id, payload);
        this.shelters.splice(index, 1, { ...shelter, ...response.data, isSaving: false });
        this.alertMessage = `Hodnocení pro úkryt '${shelter.shelter_code}' bylo uloženo.`;
        this.showSuccessAlert = true;
      } catch (error) { this.handleApiError(error); } finally { shelter.isSaving = false; }
      await useShelterStore().getUserShelters();
    },

        /**
     * Sestaví absolutní URL pro soubor.
     * 
     * @param {string} relativePath - Relativní cesta k souboru.
     * @public
     * @method getFileUrl
     * @return {string} URL souboru.
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
     * Nahraje přílohy k parametrům S_SD nebo S_IS.
     * 
     * @param {string} type - Typ přílohy ('s_sd' nebo 's_is').
     * @public
     * @method handleAttachmentUpload
     * @return {Promise<void>}
     */
    async handleAttachmentUpload(type) { // type is 's_sd' or 's_is'
      const files = this.filesToUpload[type];
      if (!this.buildingId || !files || files.length === 0) return;

      this.isUploading[type] = true;
      try {
        let response;
        if (type === 's_sd') {
          response = await api.uploadBuildingSsdAttachments(this.buildingId, files);
        } else { // 's_is'
          response = await api.uploadBuildingSisAttachments(this.buildingId, files);
        }
        
        this.buildingData.s_sd_attachment = response.data.s_sd_attachment;
        this.buildingData.s_is_attachment = response.data.s_is_attachment;
        this.filesToUpload[type] = [];
        
        this.alertMessage = `Přílohy byly úspěšně nahrány.`;
        this.showSuccessAlert = true;
      } catch (error) { this.handleApiError(error); } finally { this.isUploading[type] = false; }
    },

    /**
     * Smaže přílohu od parametru S_SD nebo S_IS.
     * 
     * @param {string} type - Typ přílohy ('s_sd' nebo 's_is').
     * @param {string} path - Cesta k souboru ke smazání.
     * @public
     * @method handleAttachmentDelete
     * @return {Promise<void>}
     */
    async handleAttachmentDelete(type, path) { // type is 's_sd' or 's_is'
      if (!this.buildingId) return;
      const filename = this.getFileName(path);
      
      if (confirm(`Opravdu si přejete smazat přílohu '${filename}'?`)) {
        try {
          if (type === 's_sd') {
            await api.deleteBuildingSsdAttachment(this.buildingId, filename);
            this.buildingData.s_sd_attachment = this.buildingData.s_sd_attachment.filter(p => p !== path);
          } else { // 's_is'
            await api.deleteBuildingSisAttachment(this.buildingId, filename);
            this.buildingData.s_is_attachment = this.buildingData.s_is_attachment.filter(p => p !== path);
          }
          this.alertMessage = 'Příloha byla smazána.';
          this.showSuccessAlert = true;
        } catch (error) { this.handleApiError(error); }
      }
    },

    /**
     * Zpracuje chyby z API volání.
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
      } else if (error.request) { this.alertMessage = 'Chyba sítě: Server neodpovídá.'; }
      else { this.alertMessage = 'Nastala neočekávaná chyba.'; }
      this.showErrorAlert = true; console.error("API Error:", error);
    },
  },
};
</script>

<style scoped>
/* Styles remain the same for consistency */
.procedure-list { padding-left: 20px; font-size: 0.875rem; }
.procedure-list li { margin-bottom: 8px; padding-left: 4px; }
.static-tables .refined-table { border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)); border-radius: 8px; overflow: hidden; }
.static-tables .refined-table :deep(thead) { background-color: rgb(var(--v-theme-surface-variant)); }
.static-tables .refined-table :deep(thead th) { font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; color: rgb(var(--v-theme-on-surface-variant)); }
.static-tables .refined-table :deep(tbody tr:nth-child(even)) { background-color: rgba(var(--v-theme-surface-variant), 0.3); }
.static-tables .refined-table :deep(tbody tr td) { border-bottom: none !important; }
</style>