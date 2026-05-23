<template>
  <v-tabs-window-item value="threat-assessment-form">
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
            <div class="font-weight-bold">{{ $t('step5.info.title') }}</div>
          </template>
          <p class="body-2 my-2">{{ $t('step5.info.description') }}</p>
          <v-divider class="my-2"></v-divider>
          <p class="text-caption">
            {{ $t('step5.info.output1') }}<br>
            {{ $t('step5.info.output2') }}
          </p>
        </v-alert>
        
        <!-- Warning message if no building is selected -->
        <v-alert v-if="!buildingId" type="warning" variant="outlined" class="mb-6" prominent border="start" icon="mdi-alert-circle-outline">
          {{ $t('step5.no_building_selected') }}
        </v-alert>

        <!-- Dynamic Form: Shelter Register (RIÚ3) -->
        <p class="font-weight-bold mb-2">{{ $t('step5.form_title') }}</p>
        <div v-if="shelters.length === 0 && buildingId" class="text-medium-emphasis">Tato budova zatím nemá žádné úkryty definované v kroku A3.</div>
        
        <v-card v-for="(shelter, index) in shelters" :key="shelter.id" class="mb-6" variant="outlined">
          <v-card-title class="bg-grey-lighten-4 py-2">
            <span class="text-subtitle-1">{{ `Posouzení ohroženosti úkrytu: ${shelter.shelter_code}` }}</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-container class="pa-0">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    :label="$t('step5.riu33')"
                    v-model.number="shelter.distance_to_target"
                    :hint="$t('step5.riu33_hint')"
                    persistent-hint
                    type="number"
                    suffix="m"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    :label="$t('step5.riu34')"
                    v-model="shelter.s_o"
                    :hint="$t('step5.riu34_hint')"
                    persistent-hint
                    readonly
                    variant="outlined"
                    bg-color="grey-lighten-5"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
             <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" :loading="shelter.isSaving" @click="saveShelterAssessment(index)">
                Uložit posouzení ohroženosti
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step5.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step5.procedure.title') }}</p>
          <ol class="procedure-list">
            <li v-for="i in 4" :key="i">{{ $t(`step5.procedure.step${i}`) }}</li>
          </ol>
        </v-sheet>
        
        <!-- Static table in expansion panel -->
        <div class="static-tables">
          <h3 class="text-h6 mb-4">{{ $t('step5.tables_title') }}</h3>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step5.table.title') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <v-table density="compact" class="mt-4 refined-table" hover>
                  <thead>
                    <tr>
                      <th>{{ $t('step5.table.headers.col1') }}</th>
                      <th>{{ $t('step5.table.headers.col2') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, i) in tableData" :key="i">
                      <td>{{ row.distance }}</td>
                      <td>{{ row.score }}</td>
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
 * @file ThreatAssessmentForm.vue
 * @brief Formulář pro posouzení ohroženosti úkrytů (Krok 5).
 * 
 * @description
 * Tato komponenta slouží jako pátý krok v procesu evidence (RIÚ3).
 * Hlavním účelem je stanovení koeficientu ohroženosti ($S_O$) pro každý úkryt
 * na základě jeho vzdálenosti od předpokládaného cíle útoku.
 * 
 * Klíčové vlastnosti:
 * - **Automatický výpočet vzdálenosti:** Při načtení formuláře se komponenta pokusí
 *   automaticky zjistit vzdálenost k nejbližšímu cíli pomocí GPS souřadnic budovy
 *   (volání `api.minDistance`), pokud tato vzdálenost ještě není vyplněna.
 * - **Výpočet skóre ($S_O$):** Automaticky přepočítává skóre (1-3) na základě vzdálenosti:
 *   - < 100 m: Skóre 3 (Vysoké ohrožení)
 *   - 100 - 500 m: Skóre 2 (Střední ohrožení)
 *   - > 500 m: Skóre 1 (Nízké ohrožení)
 * 
 * @component
 * @example
 * <threat-assessment-form 
 *    :building-id="123" 
 *    :is-active="true"
 * />
 */

import api from '@/services/api';
import { useShelterStore } from '@/stores/shelterStore';

/**
 * Vytvoří výchozí objekt stavu úkrytu rozšiřující data ze serveru o UI příznaky.
 * @param {Object} shelterData - Data úkrytu z API.
 * @returns {Object} Objekt úkrytu pro formulář.
 */
const getInitialShelterState = (shelterData) => ({
  id: null,
  shelter_code: '',
  distance_to_target: null,
  s_o: null,
  isSaving: false,
  ...shelterData,
});

export default {
  name: 'ThreatAssessmentForm',
  props: {
     /**
     * ID budovy, ke které se úkryty vztahují.
     */
    buildingId: { type: [Number, String], required: true, default: null },
        /**
     * Příznak, zda je tento tab aktivní.
     * Slouží k optimalizaci načítání dat (lazy loading) a automatického dopočtu vzdáleností.
     */
    isActive: { type: Boolean, default: false },
  },
  data() {
    return {
      isLoading: false,
      shelters: [],
      showSuccessAlert: false,
      showErrorAlert: false,
      alertMessage: '',
      tableData: [
        { distance: 'Méně než 100 m', score: 3 },
        { distance: '100 m až 500 m', score: 2 },
        { distance: 'Více než 500 m', score: 1 },
      ],
    };
  },
  watch: {
     /**
     * Při změně ID budovy (pokud je tab aktivní) znovu načte data.
     */
    buildingId: {
      handler() {
        if (this.isActive) {
          this.initializeForm();
        }
      },
    },
     /**
     * Při aktivaci tabu načte data.
     * Toto je kritické pro spuštění automatického zjišťování vzdálenosti přes API.
     */
    isActive: {
      handler(newVal) {
        if (newVal && this.buildingId) {
          console.log('ThreatAssessmentForm became active, reloading data...');
          this.initializeForm();
        }
      },
      immediate: true,
    },
    // Watch for changes in any shelter's distance to recalculate its score
     /**
     * Hluboké sledování změn v úkrytech.
     * Jakmile se změní `distance_to_target` (ručně nebo z API), přepočítá se skóre `s_o`.
     */
    shelters: {
      handler(newShelters) {
        newShelters.forEach(shelter => {
          this.calculateThreatScore(shelter);
        });
      },
      deep: true,
    },
  },
  methods: {
        /**
     * Načte úkryty budovy a pokusí se automaticky doplnit chybějící vzdálenosti.
     * 
     * Postup:
     * 1. Načte data budovy (včetně GPS a seznamu úkrytů).
     * 2. Pro každý úkryt, který nemá vyplněnou vzdálenost (`distance_to_target`),
     *    zavolá `api.minDistance` s GPS souřadnicemi budovy.
     * 3. Doplní získanou vzdálenost do formuláře.
     * 
     * @public
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      if (!this.buildingId) {
        this.shelters = [];
        return;
      }
      this.isLoading = true;
      try {
        const response = await api.getBuilding(this.buildingId);
        const building = response.data;
        
        // Use Promise.all to fetch missing distances concurrently
        const shelterPromises = (building.shelters || []).map(async (shelterData) => {
          const shelter = getInitialShelterState(shelterData);
          
          // If distance is missing and building has GPS, fetch it
          if ((shelter.distance_to_target === null || shelter.distance_to_target === undefined) && building.gps_lat && building.gps_long) {
            try {
              console.log(`Fetching distance for shelter ${shelter.shelter_code}...`);
              const distanceResponse = await api.minDistance(building.gps_lat, building.gps_long);
              // Assuming the API returns { "d": 1234.5 }
              shelter.distance_to_target = Math.round(distanceResponse.data.d);
            } catch (distError) {
              console.error(`Failed to fetch min distance for shelter ${shelter.shelter_code}:`, distError);
              // Keep distance as null, don't block the UI
            }
          }
          return shelter;
        });

        this.shelters = await Promise.all(shelterPromises);

      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.isLoading = false;
      }
    },

    /*
    handleApiError(error) {
      if (error.response) {
        if (error.response.status === 422) {
          const firstError = error.response.data.detail[0];
          this.alertMessage = `Chyba validace v poli '${firstError.loc.slice(-1)}': ${firstError.msg}`;
        } else {
          this.alertMessage = `Chyba serveru: ${error.response.data.detail || error.response.statusText}`;
        }
      } else if (error.request) { this.alertMessage = 'Chyba sítě: Server neodpovídá.'; }
      else { this.alertMessage = 'Nastala neočekávaná chyba.'; }
      this.showErrorAlert = true; console.error("API Error:", error);
    },*/

    /**
     * Vypočítá koeficient ohroženosti ($S_O$) na základě vzdálenosti.
     * Logika:
     * - < 100m -> 3
     * - 100-500m -> 2
     * - > 500m -> 1
     * 
     * @param {Object} shelter - Objekt úkrytu.
     * @public
     * @method calculateThreatScore
     * @return {void}
     */
    calculateThreatScore(shelter) {
      const distance = shelter.distance_to_target;
      if (distance === null || distance < 0 || distance === '') {
        shelter.s_o = null;
      } else if (distance < 100) {
        shelter.s_o = 3;
      } else if (distance >= 100 && distance <= 500) {
        shelter.s_o = 2;
      } else { // distance > 500
        shelter.s_o = 1;
      }
    },

    /**
     * Uloží posouzení ohroženosti pro konkrétní úkryt.
     * Odesílá pouze pole `distance_to_target` na endpoint kroku 5.
     * Hodnota `s_o` se počítá na serveru (nebo je odvozena), zde ji posílat nemusíme,
     * pokud to API nevyžaduje explicitně (zde předpokládáme uložení distance).
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
          distance_to_target: shelter.distance_to_target === '' ? null : shelter.distance_to_target,
        };
        const response = await api.updateShelterStep5(shelter.id, payload);
        
        // Update local data with the fresh response from the server
        this.shelters.splice(index, 1, getInitialShelterState(response.data));

        this.alertMessage = `Hodnocení ohroženosti pro úkryt '${shelter.shelter_code}' bylo uloženo.`;
        this.showSuccessAlert = true;
      } catch (error) {
        this.handleApiError(error);
      } finally {
        shelter.isSaving = false;
      }
      await useShelterStore().getUserShelters();
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
        if (error.response.status === 422) {
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