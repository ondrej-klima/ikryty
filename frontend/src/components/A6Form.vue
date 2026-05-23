<template>
  <v-tabs-window-item value="overall-assessment-form">
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
            <div class="font-weight-bold">{{ $t('step6.info.title') }}</div>
          </template>
          <p class="body-2 my-2">{{ $t('step6.info.description') }}</p>
          <v-divider class="my-2"></v-divider>
          <p class="text-caption">{{ $t('step6.info.output1') }}</p>
        </v-alert>

        <!-- Warning message if no building is selected -->
        <v-alert v-if="!buildingId" type="warning" variant="outlined" class="mb-6" prominent border="start" icon="mdi-alert-circle-outline">
          {{ $t('step6.no_building_selected') }}
        </v-alert>

        <!-- Dynamic Form: Shelter Register (RIÚ4) -->
        <p class="font-weight-bold mb-2">{{ $t('step6.form_title') }}</p>
        <div v-if="shelters.length === 0 && buildingId" class="text-medium-emphasis">Tato budova zatím nemá žádné úkryty definované v kroku A3.</div>
        
        <v-card v-for="shelter in shelters" :key="shelter.id" class="mb-6" variant="outlined">
          <v-card-title class="bg-grey-lighten-4 py-2">
            <span class="text-subtitle-1">{{ `Celkové hodnocení úkrytu: ${shelter.shelter_code}` }}</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-container class="pa-0">
              <v-row>
                <!-- Input fields for calculation -->
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.s_ov_input')" readonly v-model.number="shelter.s_ov" type="number" step="0.001" variant="outlined" persistent-hint hint="Skóre z kroku A4"></v-text-field></v-col>
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.n_c_input')" readonly v-model.number="shelter.capacity_short" type="number" variant="outlined" persistent-hint hint="Kapacita z kroku A3"></v-text-field></v-col>
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.s_o_input')" readonly v-model.number="shelter.s_o" type="number" variant="outlined" persistent-hint hint="Skóre z kroku A5"></v-text-field></v-col>
                
                <v-col cols="12" md="6"><v-select :label="$t('step6.s_sd_input')" :items="[{ title: 'Alespoň jedna podezřelá dělící spára', value: 0}, {value: 1, title: 'Žádná podezřelá dělící spára'}]" readonly v-model.number="buildingData.s_sd" variant="outlined" persistent-hint hint="Údaj ze stavby (krok A4)"></v-select></v-col>
                <v-col cols="12" md="6"><v-select :label="$t('step6.s_is_input')" :items="[{ title: 'V nosných stěnách jsou nevyztužené otvory/prostupy', value: 0}, { title: 'Žádné nevyztužené otvory', value: 1}]" readonly v-model.number="buildingData.s_is" variant="outlined" persistent-hint hint="Údaj ze stavby (krok A4)"></v-select></v-col>
                
                <v-col cols="12"><v-divider></v-divider></v-col>

                <!-- Output (calculated) fields -->
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.riu35')" v-model="shelter.s_c" readonly variant="outlined" bg-color="grey-lighten-5"></v-text-field></v-col>
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.riu36')" v-model="shelter.iu_class" readonly variant="outlined" bg-color="grey-lighten-5"></v-text-field></v-col>
                <v-col cols="12" md="4"><v-text-field :label="$t('step6.riu37')" v-model="shelter.assessment_needed" readonly variant="outlined" bg-color="grey-lighten-5"></v-text-field></v-col>
              </v-row>
            </v-container>

            <!-- START: Added Result Alert -->
            <v-alert
              v-if="getShelterResult(shelter)"
              :color="getAlertColor(shelter.iu_class)"
              :icon="getAlertIcon(shelter.iu_class)"
              variant="tonal"
              border="start"
              class="mt-4"
            >
              <template v-slot:title>
                <div class="font-weight-bold text-uppercase">{{ getShelterResult(shelter).priority }}</div>
              </template>
              {{ getShelterResult(shelter).action }}
            </v-alert>
            <!-- END: Added Result Alert -->

            <v-card-actions>
              <v-spacer></v-spacer>
              <!--
              <v-btn color="primary" :loading="shelter.isSaving" @click="saveShelterAssessment(index)">
                Uložit celkové hodnocení
              </v-btn>
              -->
            </v-card-actions>
          </v-card-text>
        </v-card>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step6.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step6.procedure.title') }}</p>
          <ol class="procedure-list">
            <li v-for="i in 3" :key="i" v-html="$t(`step6.procedure.step${i}`)"></li>
          </ol>
        </v-sheet>
        
        <!-- Static table in expansion panel -->
        <div class="static-tables">
          <h3 class="text-h6 mb-4">{{ $t('step6.tables_title') }}</h3>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step6.table.title') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <v-table density="compact" class="mt-4 refined-table" hover>
                  <thead><tr><th>{{ $t('step6.table.headers.col1') }}</th><th>{{ $t('step6.table.headers.col2') }}</th><th>{{ $t('step6.table.headers.col3') }}</th></tr></thead>
                  <tbody>
                    <tr v-for="(row, i) in tableData" :key="i">
                      <td v-html="row.conditions"></td><td>{{ row.priority }}</td><td>{{ row.action }}</td>
                    </tr>
                  </tbody>
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
 * @file OverallAssessmentForm.vue
 * @brief Formulář pro celkové vyhodnocení úkrytů (Krok 6).
 * 
 * @description
 * Tato komponenta představuje finální krok (RIÚ4) v procesu evidence.
 * Agreguje data z předchozích kroků a provádí finální výpočet a kategorizaci úkrytů.
 * 
 * Hlavní funkce:
 * 1. **Výpočet Celkového koeficientu ($S_C$):**
 *    - Vstupují do něj: $S_{OV}$ (odolnost), $N_C$ (kapacita), $S_O$ (ohroženost).
 *    - Používá vzorec: $S_C = \frac{10 \cdot S_{OV}}{\sqrt[3]{0.02 \cdot N_C} \cdot S_O}$.
 * 
 * 2. **Kategorizace úkrytu (Třída IÚ):**
 *    - Na základě hodnoty $S_C$ a stavebních vad ($S_{SD}$, $S_{IS}$) řadí úkryt do kategorií:
 *      - **IÚ-I / IÚ-II**: Vhodné improvizované úkryty.
 *      - **KIÚ-I / KIÚ-II / KIÚ-III**: Konzultované úkryty (vyžadují posouzení).
 *      - **KIÚ-N**: Nevhodné.
 * 
 * 3. **Doporučení:** Automaticky určuje, zda je potřeba odborné posouzení (ANO/NE).
 * 
 * Data se automaticky přepočítávají při změně vstupů (reactive watch).
 * 
 * @component
 * @example
 * <overall-assessment-form 
 *    :building-id="123" 
 *    :is-active="true"
 * />
 */

import api from '@/services/api';

/**
 * Vytvoří výchozí objekt stavu úkrytu pro formulář (rozšíření dat ze serveru).
 * @param {Object} shelterData - Data úkrytu z API.
 * @returns {Object} Objekt úkrytu.
 */
const getInitialShelterState = (shelterData) => ({
  id: null, shelter_code: '', isSaving: false,
  s_ov: null, capacity_short: null, s_o: null,
  s_c: null, iu_class: null, assessment_needed: null,
  ...shelterData,
});

/**
 * Vytvoří výchozí objekt pro data budovy.
 * @returns {Object} Výchozí stav.
 */
const getInitialBuildingData = () => ({
  s_sd: null, s_is: null,
});

export default {
  name: 'OverallAssessmentForm',
  props: {
        /**
     * ID budovy.
     */
    buildingId: { type: [Number, String], required: true, default: null },
        /**
     * Příznak, zda je tab aktivní (pro lazy loading dat).
     */
    isActive: { type: Boolean, default: false },
  },
  data() {
    return {
      isLoading: false,
      shelters: [],
      buildingData: getInitialBuildingData(),
      showSuccessAlert: false, showErrorAlert: false, alertMessage: '',
      tableData: [
        { conditions: "S_C ≥ 5<br>S_SD = 1<br>S_IS = 1", priority: "IÚ-I", action: "Doporučuje se provedení odborného posouzení IÚ dle části B metodiky. V odůvodněných případech (např. nedostatek času pro provedení odborného posouzení) lze přímo využít pro plánování IÚ s prioritou IÚ-I." },
        { conditions: "S_C ≥ 5<br>S_SD = 0 nebo S_IS = 0", priority: "KIÚ-I", action: "Využití k plánování IÚ je možné až po odborném posouzení KIÚ dle části B metodiky." },
        { conditions: "3 ≤ S_C < 5<br>S_SD = 1<br>S_IS = 1", priority: "IÚ-II", action: "Doporučuje se provedení odborného posouzení IÚ dle části B metodiky. V odůvodněných případech (např. nedostatek času pro provedení odborného posouzení) lze přímo využít pro plánování IÚ s prioritou IÚ-II." },
        { conditions: "3 ≤ S_C < 5<br>S_SD = 0 nebo S_IS = 0", priority: "KIÚ-II", action: "Využití k plánování IÚ je možné až po odborném posouzení KIÚ dle části B metodiky." },
        { conditions: "1 ≤ S_C < 3", priority: "KIÚ-III", action: "Využití k plánování IÚ je možné až po odborném posouzení KIÚ dle části B metodiky." },
        { conditions: "S_C < 1", priority: "KIÚ-N – nevhodné pro ukrytí", action: "Nedoporučuje využít k plánování IÚ. Údaje o KIÚ-N se doporučuje archivovat k případnému využití v budoucnu." }
      ],
    };
  },
  watch: {
    /**
     * Reload dat při změně ID budovy (pokud je tab aktivní).
     */
    buildingId: {
      handler() { if (this.isActive) this.initializeForm(); },
    },
    /**
     * Reload dat při aktivaci tabu.
     */
    isActive: {
      handler(newVal) { if (newVal && this.buildingId) this.initializeForm(); },
      immediate: true,
    },
     /**
     * Automatický přepočet skóre při změně dat úkrytů.
     */
    shelters: { handler(newShelters) { newShelters.forEach(this.calculateOverallScore); }, deep: true },
     /**
     * Automatický přepočet skóre při změně dat budovy (S_SD, S_IS).
     */
    buildingData: { handler() { this.shelters.forEach(this.calculateOverallScore); }, deep: true },
  },
  methods: {
    /**
     * Načte data budovy a úkrytů.
     * Mapuje parametry budovy ($S_{SD}$, $S_{IS}$) do lokálního stavu pro výpočty.
     * 
     * @public
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      if (!this.buildingId) {
        this.shelters = []; this.buildingData = getInitialBuildingData();
        return;
      }
      this.isLoading = true;
      try {
        const response = await api.getBuilding(this.buildingId);
        const data = response.data;
        this.shelters = data.shelters.map(s => getInitialShelterState(s)) || [];
        this.buildingData.s_sd = data.s_sd;
        this.buildingData.s_is = data.s_is;
      } catch (error) { this.handleApiError(error); } finally { this.isLoading = false; }
    },

    /**
     * Vypočítá celkové skóre ($S_C$) a určí třídu úkrytu.
     * 
     * Vzorec:
     * $S_C = \frac{10 \cdot S_{OV}}{\sqrt[3]{0.02 \cdot N_C} \cdot S_O}$
     * 
     * Klasifikace:
     * - $S_C \ge 5$: IÚ-I (pokud bez vad) jinak KIÚ-I
     * - $3 \le S_C < 5$: IÚ-II (pokud bez vad) jinak KIÚ-II
     * - $1 \le S_C < 3$: KIÚ-III
     * - $S_C < 1$: KIÚ-N
     * 
     * @param {Object} shelter - Objekt úkrytu.
     * @public
     * @method calculateOverallScore
     * @return {void}
     */
    calculateOverallScore(shelter) {
      const { s_ov, capacity_short, s_o } = shelter;
      const { s_sd, s_is } = this.buildingData;

      if (s_ov !== null && capacity_short > 0 && s_o > 0) {
        const s_c = (10*s_ov)/ ((2*capacity_short/100)**(1/3)*s_o) 
        //(1000 * s_ov) / (2 * capacity_short * s_o);
        shelter.s_c = parseFloat(s_c.toFixed(3));
      } else {
        shelter.s_c = null;
      }

      const s_c = shelter.s_c;
      if (s_c === null || s_sd === null || s_is === null) {
        shelter.iu_class = null;
        shelter.assessment_needed = null;
        return;
      }
      
      if (s_c >= 5) {
        shelter.iu_class = (s_sd === 1 && s_is === 1) ? 'IÚ-I' : 'KIÚ-I';
      } else if (s_c >= 3) {
        shelter.iu_class = (s_sd === 1 && s_is === 1) ? 'IÚ-II' : 'KIÚ-II';
      } else if (s_c >= 1) {
        shelter.iu_class = 'KIÚ-III';
      } else {
        // MODIFIED: Match exact text from tableData
        shelter.iu_class = 'KIÚ-N – nevhodné pro ukrytí';
      }
      // MODIFIED: Match exact text for comparison
      shelter.assessment_needed = (shelter.iu_class.startsWith('KIÚ') && shelter.iu_class !== 'KIÚ-N – nevhodné pro ukrytí') ? 'ANO' : 'NE';
    },
    // START: Added helper methods
    /**
     * Určí barvu alertu na základě třídy úkrytu.
     * @param {string} iu_class - Třída úkrytu (např. 'IÚ-I').
     * @public
     * @method getAlertColor
     * @return {string} Název barvy (success, error, warning, grey).
     */
    getAlertColor(iu_class) {
      if (!iu_class) return 'grey';
      if (iu_class.startsWith('IÚ-')) return 'success'; // Green
      if (iu_class.startsWith('KIÚ-N')) return 'error'; // Red
      if (iu_class.startsWith('KIÚ-')) return 'warning'; // Yellow
      return 'grey';
    },
    /**
     * Určí ikonu alertu na základě třídy úkrytu.
     * @param {string} iu_class - Třída úkrytu.
     * @public
     * @method getAlertIcon
     * @return {string|undefined} Název MDI ikony.
     */
    getAlertIcon(iu_class) {
      if (!iu_class) return undefined;
      if (iu_class.startsWith('IÚ-')) return 'mdi-check-circle-outline';
      if (iu_class.startsWith('KIÚ-N')) return 'mdi-close-circle-outline';
      if (iu_class.startsWith('KIÚ-')) return 'mdi-alert-outline';
      return undefined;
    },

     /**
     * Najde odpovídající řádek v `tableData` pro zobrazení doporučení uživateli.
     * @param {Object} shelter - Objekt úkrytu.
     * @public
     * @method getShelterResult
     * @return {Object|null} Řádek z tabulky pravidel.
     */
    getShelterResult(shelter) {
      if (!shelter?.iu_class) return null;
      return this.tableData.find(row => row.priority === shelter.iu_class);
    },
    // END: Added helper methods

    /**
     * Uloží vypočítané celkové hodnocení na server.
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
          s_c: shelter.s_c,
          iu_class: shelter.iu_class,
          assessment_needed: shelter.assessment_needed,
        };
        const response = await api.updateShelterStep6(shelter.id, payload);
        this.shelters.splice(index, 1, getInitialShelterState(response.data));
        this.alertMessage = `Celkové hodnocení pro úkryt '${shelter.shelter_code}' bylo uloženo.`;
        this.showSuccessAlert = true;
      } catch (error) { this.handleApiError(error); } finally { shelter.isSaving = false; }
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