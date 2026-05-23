<template>
  <v-tabs-window-item value="territory-analysis-form">
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
            <div class="font-weight-bold">{{ $t('step2.info.title') }}</div>
          </template>
          <p class="mb-2">{{ $t('step2.info.description') }}</p>
          <p class="text-caption">{{ $t('step2.info.detail') }}</p>
        </v-alert>

        <!-- Alert shown when no building is selected -->
        <v-alert
          v-if="!buildingId"
          type="warning"
          variant="outlined"
          class="mb-6"
          prominent
          border="start"
          icon="mdi-alert-circle-outline"
        >
          {{ $t('step2.no_building_selected') }}
        </v-alert>

        <!-- Form and title -->
        <p class="font-weight-bold mb-2">{{ $t('step2.form_title') }}</p>
        <v-form v-model="isFormValid">
          <v-container class="pa-0">
            <v-row>
              <!-- RS_13: Risk Area -->
              <v-col cols="12">
                <v-textarea
                  v-model="formData.risk_area"
                  :label="$t('step2.rs13')"
                  :persistent-hint="true"
                  :hint="$t('step2.rs13_hint')"
                  variant="outlined"
                  rows="2"
                  auto-grow
                  :disabled="!buildingId"
                ></v-textarea>
              </v-col>
              <!-- RS_14: Risk Justification -->
              <v-col cols="12">
                <v-textarea
                  v-model="formData.risk_justification"
                  :label="$t('step2.rs14')"
                  :persistent-hint="true"
                  :hint="$t('step2.rs14_hint')"
                  variant="outlined"
                  rows="3"
                  auto-grow
                  :disabled="!buildingId"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-form>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step2.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step2.procedure.title') }}</p>
          <ol class="procedure-list">
            <li>{{ $t('step2.procedure.step1') }}</li>
            <li>{{ $t('step2.procedure.step2') }}</li>
          </ol>
        </v-sheet>

        <!-- Static tables in expansion panels -->
        <div class="static-tables">
          <h3 class="text-h6 mb-4">{{ $t('step2.tables_title') }}</h3>
          <v-expansion-panels>
            <!-- Panel 1: Table 3-4 -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step2.panel_titles.table1') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step2.table1.title') }}</p>
                <v-table density="compact" class="refined-table" hover>
                  <thead><tr><th>{{ $t('step2.table1.headers.col1') }}</th><th>{{ $t('step2.table1.headers.col2') }}</th></tr></thead>
                  <tbody><tr v-for="(item, i) in table1Data" :key="i"><td>{{ item.area }}</td><td>{{ item.source }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- Panel 2: Table 3-5 -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step2.panel_titles.table2') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step2.table2.title') }}</p>
                <v-table density="compact" class="refined-table" hover>
                  <thead><tr><th>{{ $t('step2.table2.headers.col1') }}</th><th>{{ $t('step2.table2.headers.col2') }}</th><th>{{ $t('step2.table2.headers.col3') }}</th></tr></thead>
                  <tbody><tr v-for="(item, i) in table2Data" :key="i"><td>{{ item.device }}</td><td>{{ item.zone }}</td><td>{{ item.note }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- Panel 3: Table 3-6 -->
            <v-expansion-panel>
              <v-expansion-panel-title class="font-weight-bold">{{ $t('step2.panel_titles.table3') }}</v-expansion-panel-title>
              <v-expansion-panel-text class="bg-grey-lighten-5">
                <p class="font-weight-bold mb-2 mt-4">{{ $t('step2.table3.title') }}</p>
                <v-table density="compact" class="refined-table" hover>
                  <thead><tr><th>{{ $t('step2.table3.headers.col1') }}</th><th>{{ $t('step2.table3.headers.col2') }}</th><th>{{ $t('step2.table3.headers.col3') }}</th><th>{{ $t('step2.table3.headers.col4') }}</th></tr></thead>
                  <tbody><tr v-for="(item, i) in table3Data" :key="i"><td>{{ item.line }}</td><td>{{ item.zone }}</td><td>{{ item.type }}</td><td>{{ item.source }}</td></tr></tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <v-divider class="my-6"></v-divider>
        <!-- Form actions -->
        <v-row>
          <v-col class="d-flex justify-end">
            <v-btn
              color="primary"
              :disabled="!isFormValid || !buildingId"
              :loading="isSaving"
              @click="saveChanges"
            >
              {{ $t('actions.save_changes') }}
            </v-btn>
          </v-col>
        </v-row>
        
        <!-- Snackbars for success and error feedback -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000" location="top right">
          {{ alertMessage }}
        </v-snackbar>
        <v-snackbar v-model="showErrorAlert" color="error" timeout="5000" location="top right" multi-line>
          {{ alertMessage }}
        </v-snackbar>
        
      </v-card-text>
    </v-card>
  </v-tabs-window-item>
</template>

<script>
/**
 * @file TerritoryAnalysisForm.vue
 * @brief Formulář pro analýzu území a rizikových oblastí (Krok 2).
 * 
 * @description
 * Tato komponenta slouží jako druhý krok v procesu evidence budovy (Analýza území).
 * Obsahuje formulář pro zadání popisu rizikového území (RS_13) a zdůvodnění (RS_14).
 * 
 * Součástí komponenty jsou také informativní rozbalovací tabulky obsahující přehled
 * bezpečnostních a ochranných pásem (např. plynovody, elektrická vedení, záplavová území),
 * které slouží uživateli jako pomůcka při vyplňování.
 * 
 * Komponenta je určena primárně pro **editaci (Edit)** již existujícího záznamu budovy.
 * Vyžaduje předání `buildingId`. Data jsou ukládána pomocí specifického endpointu
 * pro aktualizaci kroku 2.
 * 
 * @component
 * @example
 * <territory-analysis-form 
 *    :building-id="123" 
 *    @building-updated="handleUpdate"
 * />
 */

/**
 * @event building-updated
 * @brief Vyvoláno po úspěšném uložení změn v kroku 2.
 * @param {Number|String} id - ID aktualizované budovy.
 */

import api from '@/services/api';

/**
 * Vrátí prázdný objekt pro inicializaci formuláře.
 * @returns {Object} Výchozí stav dat.
 */
const getInitialFormData = () => ({
  risk_area: '',
  risk_justification: '',
});

export default {
  name: 'TerritoryAnalysisForm',
  props: {
     /**
     * ID budovy pro editaci.
     * Tento formulář funguje pouze v editačním režimu, proto je ID povinné.
     */
    buildingId: {
      type: [Number, String],
      // This component is for editing only, so an ID is required to be useful.
      required: true, 
      default: null,
    },
  },
  data() {
    return {
      isLoading: false,
      isSaving: false,
      isFormValid: false,
      formData: getInitialFormData(),
      showSuccessAlert: false,
      showErrorAlert: false,
      alertMessage: '',
      table1Data: [
        { area: 'Záplavová území stanovená dle § 66 vodního zákona a vyhlášky o návrhu a stanovování záplavových území', source: 'Povodňový plán ČR, databáze DIBAVOD, správci povodí' },
        { area: 'Územní ohrožená zvláštními povodněmi stanovená dle § 69 vodního zákona', source: 'Povodňový plán ČR, správci vodních děl a vodních toků' },
        { area: 'Poddolovaná území', source: 'Česká geologická služba' },
        { area: 'Území ohrožená sesuvem půdy', source: 'Česká geologická služba' },
        { area: 'Bezpečnostní a ochranná pásma plynovodů, produktovodů, ropovodů a vedení vysokého / velmi vysokého napětí (dále také „VN/VVN“) stanovená dle příslušných právních předpisů, zejména energetického zákona a zákona o nouzových zásobách ropy', source: 'Územní plány – stavební úřady, krajské úřady Správce plynovodu, produktovodu, ropovodu nebo vedení VN/VVN' },
        { area: 'Zóna havarijního plánování pro objekt skupiny B dle zákona o prevenci závažných havárií', source: 'Krajské úřady' },
        { area: 'Bezprostřední okolí objektů skupiny A dle zákona o prevenci závažných havárií, případně vybraných objektů s podlimitním množstvím nebezpečných látek (tzv. podlimitních objektů)', source: 'Krajské úřady' }
      ],
      table2Data: [
{ device: 'Podzemní zásobníky plynu (bezsamostatných sond)',
 zone: '250 m',
note: 'od vnějšího okraje'},
{ device: 'Sondy zásobníku – p ≤ 100 bar',
 zone: '80 m',
note: 'od technologií od osy ústí sondy'},
{ device: 'Sondy zásobníku – p > 100 bar',
 zone: '150 m',
note: 'od osy ústí sondy'},
{ device: 'Tlakové zásobníky LPG 5–20 m³',
 zone: '20 m',
note: 'od vnějšího obvodu tech. objektů'},
{ device: 'Tlakové zásobníky LPG 20–100 m³ / 100–250 m³ / 250–500 m³ / 500–1000 m³ / 1 000–3 000 m³ / >3 000m³',
 zone: '40 m / 60 m / 100 m / 150 m/ 200m / 300 m',
note: 'od vnějšího obvodu tech. objektů'},
{ device: 'Plnírny, zkapalňovací a odpařovací stanice plynů',
 zone: '100 m',
note: 'od technologií'},
{ device: 'Kompresorové stanice',
 zone: '200 m'},

{ device: 'Regulační stanice VT 4–40 bar / > 40 bar',
 zone: '10 m / 20 m'},

{ device: 'Vysokotlaké plynovody 4–40 bar – DN ≤ 100 / 100–300 / 300–500 / 500–700 / > 700',
 zone: '10 m / 20 m / 30 m / 45 m / 65 m',
note: 'měřeno od osy, na každou stranu'},
{ device: 'Vysokotlaké plynovody > 40 bar – DN ≤ 100 / 100–500 / > 500',
 zone: '80 m / 120 m / 160 m',
note: 'měřeno od osy, na každou stranu'},
    ],
table3Data: [
        { line: 'VN 1–35 kV (holé vodiče)', zone: '7 m', type: 'nadzemní', source: '§ 46 energetického zákona' },
        { line: 'VN > 35 kV – 110 kV', zone: '12 m', type: 'nadzemní', source: '§ 46 energetického zákona' },
        { line: 'VVN > 110 kV – 220 kV', zone: '15 m', type: 'nadzemní', source: '§ 46 energetického zákona' },
        { line: 'VVN > 220 kV – 400 kV', zone: '20 m', type: 'nadzemní', source: '§ 46 energetického zákona' },
        { line: 'ZVN > 400 kV', zone: '30 m', type: 'nadzemní', source: '§ 46 energetického zákona' },
        { line: 'Kabely ≤ 110 kV', zone: '1 m', type: 'podzemní', source: '§ 46 energetického zákona' },
        { line: 'Kabely > 110 kV', zone: '3 m', type: 'podzemní', source: '§ 46 energetického zákona' },
        { line: 'Ropovod Družba (MERO ČR, a.s.)', zone: '150 m', type: 'ropa', source: '§ 3 zákona o nouzových zásobách ropy' },
        { line: 'Ropovod IKL (MERO ČR, a.s.)', zone: '150 m', type: 'ropa', source: '§ 3 zákona o nouzových zásobách ropy' },
        { line: 'Produktovody ČEPRO (motorová paliva)', zone: '300 m', type: 'benzín, nafta, JET A-1', source: 'Firemní metodika, ÚAP kód 3.5.10224' },
        { line: 'Ethylbenzenový produktovod Litvínov → Kralupy (ORLEN Unipetrol RPA s.r.o.)', zone: '150 m', type: 'ethylbenzen', source: '§ 3 zákona o nouzových zásobách ropy' },
        { line: 'Ethylenový produktovod Litvínov → Neratovice (ORLEN Unipetrol RPA s.r.o.)', zone: '150 m', type: 'ethylen', source: '§ 3 zákona o nouzových zásobách ropy' }
      ],
    };
  },
  methods: {
    /**
     * Inicializuje formulář načtením dat ze serveru.
     * Pokud není zadáno ID budovy, vyresetuje formulář.
     * Mapuje příchozí data na pole `risk_area` a `risk_justification`.
     * 
     * @public
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      if (!this.buildingId) {
        this.formData = getInitialFormData();
        return;
      }
      this.isLoading = true;
      try {
        const response = await api.getBuilding(this.buildingId);
        // Populate only the fields relevant to this form
        this.formData.risk_area = response.data.risk_area || '';
        this.formData.risk_justification = response.data.risk_justification || '';
      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.isLoading = false;
      }
    },
        /**
     * Uloží změny provedené ve formuláři na server.
     * Volá specifický endpoint pro aktualizaci kroku 2 (Analýza území).
     * Při úspěchu zobrazí notifikaci a emituje událost `building-updated`.
     * 
     * @public
     * @method saveChanges
     * @return {Promise<void>}
     */
    async saveChanges() {
      if (!this.isFormValid || !this.buildingId) return;
      this.isSaving = true;
      try {
        // Use the dedicated API function for updating Step 2
        const response = await api.updateBuildingStep2(this.buildingId, this.formData);
        
        this.alertMessage = 'Změny v kroku A2 byly úspěšně uloženy.';
        this.showSuccessAlert = true;
        this.$emit('building-updated', response.data.id);
      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.isSaving = false;
      }
    },

        /**
     * Zpracuje chybu z API volání a nastaví chybovou hlášku.
     * Rozlišuje mezi chybou odpovědi serveru (4xx, 5xx), chybou sítě a neznámou chybou.
     * 
     * @param {Object} error - Objekt chyby (např. Axios error).
     * @public
     * @method handleApiError
     * @return {void}
     */
    handleApiError(error) {
      if (error.response) {
        this.alertMessage = `Chyba serveru: ${error.response.data.detail || error.response.statusText}`;
      } else if (error.request) {
        this.alertMessage = 'Chyba sítě: Server neodpovídá.';
      } else {
        this.alertMessage = 'Nastala neočekávaná chyba.';
      }
      this.showErrorAlert = true;
      console.error("API Error:", error);
    },
  },
  mounted() {
    this.initializeForm();
  },
  watch: {
    // If the parent component changes the ID, reload the data
        /**
     * Sleduje změnu prop `buildingId`.
     * Při změně ID znovu načte data formuláře.
     */
    buildingId: {
      handler() {
        this.initializeForm();
      },
    },
  },
};
</script>

<style scoped>
/* Styles remain the same for consistency */
.procedure-list { padding-left: 20px; font-size: 0.875rem; }
.procedure-list li { margin-bottom: 8px; padding-left: 4px; }
.procedure-list li:last-child { margin-bottom: 0; }
.static-tables .refined-table { border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)); border-radius: 8px; overflow: hidden; }
.static-tables .refined-table :deep(thead) { background-color: rgb(var(--v-theme-surface-variant)); }
.static-tables .refined-table :deep(thead th) { font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; color: rgb(var(--v-theme-on-surface-variant)); }
.static-tables .refined-table :deep(tbody tr:nth-child(even)) { background-color: rgba(var(--v-theme-surface-variant), 0.3); }
.static-tables .refined-table :deep(tbody tr td) { border-bottom: none !important; }
</style>