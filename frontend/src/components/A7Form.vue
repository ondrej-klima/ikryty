<template>
  <v-tabs-window-item value="review-and-approval-form">
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
            <div class="font-weight-bold">{{ $t('step7.info.title') }}</div>
          </template>
          <p class="body-2 my-2">{{ $t('step7.info.description') }}</p>
          <v-divider class="my-2"></v-divider>
          <p class="text-caption">{{ $t('step7.info.output1') }}</p>
        </v-alert>

        <!-- Warning message if no building is selected -->
        <v-alert v-if="!buildingId" type="warning" variant="outlined" class="mb-6" prominent border="start" icon="mdi-alert-circle-outline">
          {{ $t('step7.no_building_selected') }}
        </v-alert>

        <!-- Form: Review and Approval -->
        <p class="font-weight-bold mb-2">{{ $t('step7.form_title') }}</p>
        <v-form v-model="isFormValid">
          <v-container class="pa-0">
            <v-row>
              <!-- RS_25: Datum poslední kontroly -->
              <v-col cols="12" md="6">
                <v-menu v-model="dateMenuControl" :close-on-content-click="false" :disabled="!buildingId">
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      :label="$t('step7.rs25_riu38')"
                      :model-value="formattedDateForDisplay(formData.last_control_date)"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      variant="outlined"
                      v-bind="props"
                      :disabled="!buildingId"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="formData.last_control_date" @update:modelValue="dateMenuControl = false" hide-header></v-date-picker>
                </v-menu>
              </v-col>

              <!-- RS_27: Schvalovatel -->
              <v-col cols="12" md="6">
                <v-text-field
                  :label="$t('step7.rs27_riu40')"
                  v-model="formData.approver"
                  variant="outlined"
                  :disabled="!buildingId"
                ></v-text-field>
              </v-col>

              <!-- RS_26: Nedostatky -->
              <v-col cols="12">
                <v-textarea
                  :label="$t('step7.rs26_riu39')"
                  :hint="$t('step7.rs26_riu39_hint')"
                  persistent-hint
                  v-model="formData.control_deficiencies"
                  variant="outlined"
                  rows="3"
                  :disabled="!buildingId"
                ></v-textarea>
              </v-col>
              
              <!-- RS_28: Provedení odborného posouzení -->
              <v-col cols="12" md="6">
                <v-select
                  :label="$t('step7.rs28_riu41')"
                  v-model="formData.assessment_status"
                  :items="['Provedeno', 'Plánování', 'Ne']"
                  variant="outlined"
                  :disabled="!buildingId"
                ></v-select>
              </v-col>

              <!-- RS_29: Datum odborného posouzení (conditional) -->
              <v-col cols="12" md="6" v-if="formData.assessment_status === 'Provedeno' || formData.assessment_status === 'Plánování'">
                 <v-menu v-model="dateMenuAssessment" :close-on-content-click="false" :disabled="!buildingId">
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      :label="$t('step7.rs29_riu42')"
                      :model-value="formattedDateForDisplay(formData.assessment_date)"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      variant="outlined"
                      v-bind="props"
                      :disabled="!buildingId"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="formData.assessment_date" @update:modelValue="dateMenuAssessment = false" hide-header></v-date-picker>
                </v-menu>
              </v-col>

              <!-- RS_28b: Interval revize -->
              <v-col cols="12" md="6">
                <v-text-field
                  :label="$t('step7.rs28_riu43')"
                  :hint="$t('step7.rs28_riu43_hint')"
                  persistent-hint
                  v-model="formData.review_interval"
                  variant="outlined"
                  :disabled="!buildingId"
                ></v-text-field>
              </v-col>

              <!-- RS_29b: Datum příští revize -->
              <v-col cols="12" md="6">
                 <v-menu v-model="dateMenuNextReview" :close-on-content-click="false" :disabled="!buildingId">
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      :label="$t('step7.rs29_riu44')"
                      :model-value="formattedDateForDisplay(formData.next_review_date)"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      variant="outlined"
                      v-bind="props"
                      :disabled="!buildingId"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="formData.next_review_date" @update:modelValue="dateMenuNextReview = false" hide-header></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-container>
        </v-form>

        <!-- Procedural guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step7.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step7.procedure.title') }}</p>
          <ol class="procedure-list">
            <li v-for="i in 3" :key="i" v-html="$t(`step7.procedure.step${i}`)"></li>
          </ol>
        </v-sheet>
        
        <!-- Form Actions -->
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

        <!-- Snackbars for user feedback -->
        <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000" location="top right"> {{ alertMessage }} </v-snackbar>
        <v-snackbar v-model="showErrorAlert" color="error" timeout="5000" location="top right" multi-line> {{ alertMessage }} </v-snackbar>
      </v-card-text>
    </v-card>
  </v-tabs-window-item>
</template>

<script>
  /**
 * @file ReviewAndApprovalForm.vue
 * @brief Formulář pro revizi, kontrolu a schválení záznamu (Krok 7).
 * 
 * @description
 * Tato komponenta představuje administrativní závěr procesu evidence (část RS5 a RS6).
 * Slouží k zaznamenání:
 * - Data poslední kontroly a zjištěných nedostatků (RS_25, RS_26).
 * - Jména schvalovatele záznamu (RS_27).
 * - Stavu odborného posouzení (RS_28) a jeho data (RS_29).
 * - Intervalů a termínů příštích revizí.
 * 
 * Komponenta řeší specifickou logiku převodu dat, protože UI komponenty (DatePicker)
 * pracují s objekty `Date`, zatímco API vyžaduje řetězce `YYYY-MM-DD`.
 * 
 * @component
 * @example
 * <review-and-approval-form 
 *    :building-id="123" 
 *    :is-active="true"
 *    @building-updated="handleUpdate"
 * />
 */

/**
 * @event building-updated
 * @brief Vyvoláno po úspěšném uložení revizních údajů.
 * @param {Number|String} id - ID budovy.
 */

import api from '@/services/api';

/**
 * Vrací výchozí objekt dat formuláře.
 * @returns {Object} Prázdný stav formuláře.
 */
const getInitialFormData = () => ({
  last_control_date: null,
  control_deficiencies: '',
  approver: '',
  assessment_status: null,
  assessment_date: null,
  review_interval: '2 roky',
  next_review_date: null,
});

/**
 * Formátuje objekt data na řetězec 'YYYY-MM-DD' vyžadovaný API.
 * @param {Date | string | null} date - Vstupní datum (Date objekt nebo string).
 * @returns {string | null} Datum ve formátu YYYY-MM-DD nebo null.
 */
const formatDateForApi = (date) => {
  if (!date) return null;
  const d = new Date(date);
  const year = d.getFullYear();
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const day = d.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
};


export default {
  name: 'ReviewAndApprovalForm',
  props: {
        /**
     * ID budovy.
     */
    buildingId: { type: [Number, String], required: true, default: null },
        /**
     * Příznak, zda je tab aktivní (pro lazy loading).
     */
    isActive: { type: Boolean, default: false },
  },
  data() {
    return {
      isLoading: false, isSaving: false, isFormValid: false,
      formData: getInitialFormData(),
      showSuccessAlert: false, showErrorAlert: false, alertMessage: '',
      dateMenuControl: false, dateMenuAssessment: false, dateMenuNextReview: false,
    };
  },
  watch: {
        /**
     * Reload dat při změně ID budovy (pokud je tab aktivní).
     */
    buildingId: { handler() { if (this.isActive) this.initializeForm(); } },
        /**
     * Reload dat při aktivaci tabu.
     */
    isActive: {
      handler(newVal) { if (newVal && this.buildingId) this.initializeForm(); },
      immediate: true,
    },
  },
  methods: {
        /**
     * Načte data budovy z API a naplní formulář.
     * Provádí konverzi datových řetězců z API na objekty `Date` pro správné fungování `v-date-picker`.
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
        const data = response.data;
        // When fetching, convert date strings from API to Date objects for the v-date-picker
        this.formData.last_control_date = data.last_control_date ? new Date(data.last_control_date) : null;
        this.formData.control_deficiencies = data.control_deficiencies || '';
        this.formData.approver = data.approver || '';
        this.formData.assessment_status = data.assessment_status;
        this.formData.assessment_date = data.assessment_date ? new Date(data.assessment_date) : null;
        this.formData.review_interval = data.review_interval || '2 roky';
        this.formData.next_review_date = data.next_review_date ? new Date(data.next_review_date) : null;
      } catch (error) { this.handleApiError(error); } finally { this.isLoading = false; }
    },

    /**
     * Uloží data formuláře na server.
     * Před odesláním převede objekty `Date` zpět na řetězce `YYYY-MM-DD` pomocí `formatDateForApi`.
     * Volá endpoint `updateBuildingStep7`.
     * 
     * @public
     * @method saveChanges
     * @return {Promise<void>}
     */
    async saveChanges() {
      if (!this.isFormValid || !this.buildingId) return;
      this.isSaving = true;
      try {
        // --- KEY FIX: Format dates before sending ---
        const payload = {
          last_control_date: formatDateForApi(this.formData.last_control_date),
          control_deficiencies: this.formData.control_deficiencies,
          approver: this.formData.approver,
          assessment_status: this.formData.assessment_status,
          assessment_date: formatDateForApi(this.formData.assessment_date),
          review_interval: this.formData.review_interval,
          next_review_date: formatDateForApi(this.formData.next_review_date),
        };

        const response = await api.updateBuildingStep7(this.buildingId, payload);
        this.alertMessage = 'Revize a schválení bylo úspěšně uloženo.';
        this.showSuccessAlert = true;
        this.$emit('building-updated', response.data.id);
      } catch (error) { this.handleApiError(error); } finally { this.isSaving = false; }
    },

    // Helper for displaying dates in the text fields
     /**
     * Pomocná metoda pro formátování data v textovém poli (český formát).
     * @param {Date|string} date - Vstupní datum.
     * @public
     * @method formattedDateForDisplay
     * @return {string|null} Datum ve formátu 'd. M. yyyy' nebo null.
     */
    formattedDateForDisplay(date) {
      if (!date) return null;
      const d = date instanceof Date ? date : new Date(date);
      return d.toLocaleDateString('cs-CZ'); // Format as DD. MM. YYYY
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
</style>