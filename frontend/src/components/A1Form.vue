<template>
  <v-tabs-window-item value="building-info-form">
    <v-card flat :loading="isLoading">
      <v-card-text>
        <!-- Informational block at the start of the form -->
        <v-alert
          variant="tonal"
          color="blue-grey"
          class="mb-6"
          border="start"
        >
          <template v-slot:title>
            <div class="font-weight-bold">{{ $t('step1.info.title') }}</div>
          </template>
          <p class="mb-2">{{ $t('step1.info.description') }}</p>
          <p class="text-caption">{{ $t('step1.info.detail') }}</p>
        </v-alert>

        <!-- Form Title -->
        <p class="font-weight-bold mb-2">
          {{ $t('step1.form_title') }}
        </p>

        <!-- Form -->
        <v-form v-model="isFormValid">
          <v-container class="pa-0">
            <v-row>
              <!-- RS_1: Building Code -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.building_code"
                  :label="$t('step1.rs1')"
                  :persistent-hint="true"
                  :hint="$t('step1.rs1_hint')"
                  variant="outlined"
                  :disabled="isEditMode"
                  :rules="[v => !!v || 'Identifikační kód je povinný']"
                  required
                ></v-text-field>
              </v-col>

              <!-- RS_11: Responsible Person -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.responsible_person"
                  :label="$t('step1.rs11')"
                  :persistent-hint="true"
                  :hint="$t('step1.rs11_hint')"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- RS_2: Name / Address -->
              <v-col cols="12">
                <v-textarea
                  v-model="formData.name_address"
                  :label="$t('step1.rs2')"
                  :persistent-hint="true"
                  :hint="$t('step1.rs2_hint')"
                  variant="outlined"
                  rows="2"
                  auto-grow
                  :rules="[v => !!v || 'Název / adresa je povinná']"
                  required
                ></v-textarea>
              </v-col>

              <!-- RS_3: GPS Coordinates -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.gps_lat"
                  :label="$t('step1.rs3_lat')"
                  placeholder="např. 49.1951"
                  variant="outlined"
                  type="number"
                  :rules="[v => !!v || 'GPS souřadnice jsou povinné']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.gps_long"
                  :label="$t('step1.rs3_long')"
                  placeholder="např. 16.6068"
                  variant="outlined"
                  type="number"
                  :rules="[v => !!v || 'GPS souřadnice jsou povinné']"
                  required
                ></v-text-field>
              </v-col>

              <!-- RS_4: Owner / Manager -->
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.owner" :label="$t('step1.rs4')" :persistent-hint="true" :hint="$t('step1.rs4_hint')" variant="outlined"></v-text-field>
              </v-col>

              <!-- RS_4: Owner / Manager -->
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.administrator" :label="$t('step1.rs5a')" :persistent-hint="true" :hint="$t('step1.rs5a_hint')" variant="outlined"></v-text-field>
              </v-col>

              <!-- RS_5: Accessibility / Mode -->
              <v-col cols="12">
                <p class="text-subtitle-1 mb-2">{{ $t('step1.rs5_title') }}</p>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.operation_type"
                  :items="operationTypeItems"
                  :label="$t('step1.rs5_operationType')"
                  :persistent-hint="true"
                  :hint="$t('step1.rs5_hint')"
                  variant="outlined"
                >
                  <template v-slot:item="{ props, item }">
                    <template v-if="item.raw.type === 'subheader'">
                      <v-list-subheader>{{ item.raw.title }}</v-list-subheader>
                    </template>
                    <template v-else>
                      <v-list-item v-bind="props"></v-list-item>
                    </template>
                  </template>
                </v-select>
                 <v-text-field
                  v-if="formData.operation_type === OPERATION_TYPE_CUSTOM"
                  v-model="formData.operation_type_custom"
                  label="Zadejte vlastní způsob provozu"
                  variant="outlined"
                  class="mt-4"
                  required
                  :rules="[v => !!v || 'Vlastní způsob provozu je povinný']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center pt-md-0">
                <v-checkbox v-model="formData.access_restricted" :label="$t('step1.rs5_access')" color="primary" hide-details></v-checkbox>
              </v-col>

              <!-- RS_6: Object Type / Purpose -->
              <v-col cols="12">
                <v-select
                  v-model="formData.object_type"
                  :items="objectTypeItems"
                  :label="$t('step1.rs6')"
                  :persistent-hint="true"
                  :hint="$t('step1.rs6_hint')"
                  variant="outlined"
                >
                  <template v-slot:item="{ props, item }">
                    <template v-if="item.raw.type === 'subheader'">
                      <v-list-subheader>{{ item.raw.title }}</v-list-subheader>
                    </template>
                    <template v-else>
                      <v-list-item v-bind="props"></v-list-item>
                    </template>
                  </template>
                </v-select>

                <v-text-field
                  v-if="formData.object_type === CUSTOM_OBJECT_TYPE"
                  v-model="formData.object_type_custom"
                  label="Zadejte vlastní typ stavby"
                  placeholder="Např. datové centrum, archiv, atd."
                  variant="outlined"
                  class="mt-4"
                  required
                  :rules="[v => !!v || 'Vlastní typ stavby je povinný']"
                ></v-text-field>
              </v-col>

              <!-- RS_7: Available Spaces -->
              <v-col cols="12">
                <p class="text-subtitle-1 mb-2">{{ $t('step1.rs7_title') }}</p>
                <div class="d-flex flex-wrap">
                  <!-- <v-checkbox v-model="formData.has_underground" :label="$t('step1.rs7_underground')" class="mr-4"></v-checkbox> -->
                  <v-checkbox v-model="formData.has_basement" :label="$t('step1.rs7_basement')" class="mr-4"></v-checkbox>
                  <v-checkbox v-model="formData.has_inner_wing" :label="$t('step1.rs7_innerWing')"></v-checkbox>
                </div>
              </v-col>

              <!-- RS_8: Construction Limits -->
              <v-col cols="12"><v-textarea v-model="formData.construction_limits" :label="$t('step1.rs8')" :persistent-hint="true" :hint="$t('step1.rs8_hint')" variant="outlined" rows="3" auto-grow></v-textarea></v-col>

              <!-- RS_9: Data Source -->
              <v-col cols="12"><v-text-field v-model="formData.data_source" :label="$t('step1.rs9')" :persistent-hint="true" :hint="$t('step1.rs9_hint')" variant="outlined"></v-text-field></v-col>

              <!-- RS_10: Datum vytvoření záznamu -->
              <v-col cols="12" md="6">
                <v-menu v-model="dateMenu" :close-on-content-click="false">
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      :label="$t('step1.rs10')"
                      :model-value="formattedDateForDisplay(formData.created_date)"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      variant="outlined"
                      v-bind="props"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="formData.created_date" @update:modelValue="dateMenu = false" hide-header></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-container>
        </v-form>

        <!-- Procedural Guide -->
        <v-sheet border rounded="lg" class="pa-4 my-6">
          <p class="body-2">{{ $t('step1.procedure.intro') }}</p>
          <p class="body-1 font-weight-bold mt-4 mb-2">{{ $t('step1.procedure.title') }}</p>
          <ol class="procedure-list">
            <li v-for="i in 6" :key="i">{{ $t(`step1.procedure.step${i}`) }}</li>
          </ol>
        </v-sheet>

        <!-- Form Actions -->
        <v-row>
          <v-col class="d-flex justify-end">
            <!-- <v-btn color="grey" class="mr-4">{{ $t('actions.cancel') }}</v-btn> -->
            <v-btn
              color="primary"
              :disabled="!isFormValid"
              :loading="isSaving"
              @click="submitForm"
            >
              {{ isEditMode ? $t('actions.save_changes') : $t('actions.create_record') }}
            </v-btn>
          </v-col>
        </v-row>

        <!-- Success Snackbar -->
        <v-snackbar
          v-model="showSuccessAlert"
          color="success"
          timeout="3000"
          location="top right"
        >
          {{ alertMessage }}
        </v-snackbar>

        <!-- Error Snackbar -->
        <v-snackbar
          v-model="showErrorAlert"
          color="error"
          timeout="5000"
          location="top right"
          multi-line
        >
          {{ alertMessage }}
        </v-snackbar>

      </v-card-text>
    </v-card>
  </v-tabs-window-item>
</template>

<script>
/**
 * @file BuildingInfoForm.vue
 * @brief Formulář pro správu základních identifikačních údajů budovy (Krok 1).
 * 
 * @description
 * Tato komponenta slouží jako první krok v procesu evidence budovy. 
 * Obsahuje formulář pro zadání identifikačního kódu (RS_1), adresy (RS_2), 
 * GPS souřadnic (RS_3), vlastníka (RS_4), typu provozu (RS_5) a typu objektu (RS_6).
 * 
 * Komponenta podporuje dva režimy:
 * 1. **Vytvoření (Create):** Pokud není předáno `buildingId`.
 * 2. **Editace (Edit):** Pokud je předáno `buildingId`, data se načtou z API.
 * 
 * Zahrnuje také logiku pro zpracování "vlastních voleb" (custom input) 
 * u výběrových polí (Select) pro typ provozu a typ stavby.
 * 
 * @component
 * @example
 * <building-info-form 
 *    :building-id="123" 
 *    :gps-lat="49.195" 
 *    :gps-lng="16.606"
 *    @building-updated="handleUpdate"
 * />
 */

 /**
 * @event building-created
 * @brief Vyvoláno po úspěšném vytvoření nového záznamu.
 * @param {Number|String} id - ID nově vytvořené budovy.
 */

/**
 * @event building-updated
 * @brief Vyvoláno po úspěšné aktualizaci existujícího záznamu.
 * @param {Number|String} id - ID aktualizované budovy.
 */

import api from '@/services/api';

const formatDateForApi = (date) => {
  if (!date) return null;
  const d = new Date(date);
  const year = d.getFullYear();
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const day = d.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// --- START: Constants for RS_5 Select Field ---
const OPERATION_TYPE_CUSTOM = '12.1 Uživatelská volba';
const OPERATION_TYPE_ITEMS = [
  { type: 'subheader', title: 'Administrativní provozy' },
  { title: '1.1 Úřady a státní správa', value: '1.1 Úřady a státní správa' },
  { title: '1.2 Kancelářské provozy', value: '1.2 Kancelářské provozy' },
  { title: '1.3 Bankovní a finanční služby', value: '1.3 Bankovní a finanční služby' },
  { type: 'subheader', title: 'Obchodní provozy' },
  { title: '2.1 Maloobchod (obchody, supermarkety)', value: '2.1 Maloobchod (obchody, supermarkety)' },
  { title: '2.2 Velkoobchod', value: '2.2 Velkoobchod' },
  { title: '2.3 E-commerce a distribuční centra', value: '2.3 E-commerce a distribuční centra' },
  { type: 'subheader', title: 'Výrobní provozy' },
  { title: '3.1 Lehké výroby (textil, potraviny)', value: '3.1 Lehké výroby (textil, potraviny)' },
  { title: '3.2 Těžké výroby (strojírenství, hutnictví)', value: '3.2 Těžké výroby (strojírenství, hutnictví)' },
  { title: '3.3 Chemické a farmaceutické provozy', value: '3.3 Chemické a farmaceutické provozy' },
  { type: 'subheader', title: 'Skladovací a logistické provozy' },
  { title: '4.1 Sklady', value: '4.1 Sklady' },
  { title: '4.2 Logistická centra', value: '4.2 Logistická centra' },
  { title: '4.3 Chladírenské provozy', value: '4.3 Chladírenské provozy' },
  { type: 'subheader', title: 'Zdravotnické provozy' },
  { title: '5.1 Nemocniční provozy', value: '5.1 Nemocniční provozy' },
  { title: '5.2 Ambulantní provozy', value: '5.2 Ambulantní provozy' },
  { title: '5.3 Lékárenské provozy', value: '5.3 Lékárenské provozy' },
  { type: 'subheader', title: 'Školské a vzdělávací provozy' },
  { title: '6.1 Mateřské školy', value: '6.1 Mateřské školy' },
  { title: '6.2 Základní a střední školy', value: '6.2 Základní a střední školy' },
  { title: '6.3 Vysoké školy a univerzity', value: '6.3 Vysoké školy a univerzity' },
  { type: 'subheader', title: 'Stravovací a ubytovací provozy' },
  { title: '7.1 Restaurace a jídelny', value: '7.1 Restaurace a jídelny' },
  { title: '7.2 Hotely a penziony', value: '7.2 Hotely a penziony' },
  { title: '7.3 Cateringové služby', value: '7.3 Cateringové služby' },
  { type: 'subheader', title: 'Sportovní a rekreační provozy' },
  { title: '8.1 Fitness centra', value: '8.1 Fitness centra' },
  { title: '8.2 Sportovní haly', value: '8.2 Sportovní haly' },
  { title: '8.3 Aquaparky a wellness', value: '8.3 Aquaparky a wellness' },
  { type: 'subheader', title: 'Kulturní a společenské provozy' },
  { title: '9.1 Divadla, kina', value: '9.1 Divadla, kina' },
  { title: '9.2 Muzea, galerie', value: '9.2 Muzea, galerie' },
  { title: '9.3 Kulturní domy', value: '9.3 Kulturní domy' },
  { type: 'subheader', title: 'Dopravní provozy' },
  { title: '10.1 Silniční doprava (autobusová nádraží)', value: '10.1 Silniční doprava (autobusová nádraží)' },
  { title: '10.2 Železniční doprava (železniční nádraží)', value: '10.2 Železniční doprava (železniční nádraží)' },
  { title: '10.3 Letecká doprava', value: '10.3 Letecká doprava' },
  { type: 'subheader', title: 'Sociální provozy' },
  { title: '11.1 Domovy pro seniory', value: '11.1 Domovy pro seniory' },
  { title: '11.2 Azylové domy', value: '11.2 Azylové domy' },
  { title: '11.3 Zařízení sociálních služeb (denní stacionáře, chráněné bydlení)', value: '11.3 Zařízení sociálních služeb (denní stacionáře, chráněné bydlení)' },
  { type: 'subheader', title: 'Další typ provozu' },
  { title: '12.1 Uživatelská volba', value: OPERATION_TYPE_CUSTOM },
];
// --- END: Constants for RS_5 Select Field ---


// --- START: Constants for RS_6 Select Field ---
const CUSTOM_OBJECT_TYPE = '6.1 Uživatelská volba';
const OBJECT_TYPE_ITEMS = [
  { type: 'subheader', title: 'Veřejné stavby' },
  { title: '1.1 Obecní (radnice, obecní úřady, kulturní domy)', value: '1.1 Obecní (radnice, obecní úřady, kulturní domy)' },
  { title: '1.2 Školské (mateřské školy, základní školy, univerzity)', value: '1.2 Školské (mateřské školy, základní školy, univerzity)' },
  { title: '1.3 Zdravotnické (nemocnice, polikliniky, lékárny)', value: '1.3 Zdravotnické (nemocnice, polikliniky, lékárny)' },
  { title: '1.4 Sportovní (stadiony, tělocvičny, bazény)', value: '1.4 Sportovní (stadiony, tělocvičny, bazény)' },
  { type: 'subheader', title: 'Bytové stavby' },
  { title: '2.1 Rodinné domy (samostatné, řadové)', value: '2.1 Rodinné domy (samostatné, řadové)' },
  { title: '2.2 Bytové domy (panelové, činžovní)', value: '2.2 Bytové domy (panelové, činžovní)' },
  { title: '2.3 Sociální bydlení (domovy pro seniory, azylové domy)', value: '2.3 Sociální bydlení (domovy pro seniory, azylové domy)' },
  { type: 'subheader', title: 'Průmyslové stavby' },
  { title: '3.1 Výrobní (továrny, montážní haly)', value: '3.1 Výrobní (továrny, montážní haly)' },
  { title: '3.2 Skladové (logistická centra, sklady)', value: '3.2 Skladové (logistická centra, sklady)' },
  { title: '3.3 Energetické (elektrárny, rozvodny)', value: '3.3 Energetické (elektrárny, rozvodny)' },
  { type: 'subheader', title: 'Komerční stavby' },
  { title: '4.1 Obchodní (nákupní centra, supermarkety)', value: '4.1 Obchodní (nákupní centra, supermarkety)' },
  { title: '4.2 Administrativní (kancelářské budovy)', value: '4.2 Administrativní (kancelářské budovy)' },
  { title: '4.3 Ubytovací (hotely, penziony)', value: '4.3 Ubytovací (hotely, penziony)' },
  { type: 'subheader', title: 'Dopravní stavby' },
  { title: '5.1 Silniční (mosty, tunely, dálnice)', value: '5.1 Silniční (mosty, tunely, dálnice)' },
  { title: '5.2 Železniční (nádraží, tratě)', value: '5.2 Železniční (nádraží, tratě)' },
  { title: '5.3 Letecké (letiště, hangáry)', value: '5.3 Letecké (letiště, hangáry)' },
  { type: 'subheader', title: 'Další typ stavby' },
  { title: '6.1 Uživatelská volba', value: CUSTOM_OBJECT_TYPE },
];
// --- END: Constants for RS_6 Select Field ---

const getInitialFormData = () => ({
  building_code: '',
  name_address: '',
  gps_lat: null,
  gps_long: null,
  owner: '',
  administrator: '',
  access_restricted: false,
  operation_type: '',
  operation_type_custom: '', // For custom RS_5 input
  object_type: '',
  object_type_custom: '', // For custom RS_6 input
  has_underground: false,
  has_basement: false,
  has_inner_wing: false,
  construction_limits: '',
  data_source: '',
  created_date: new Date(),
  responsible_person: ''
});

export default {
  name: 'BuildingInfoForm',
  props: {
    /**
     * @brief ID budovy pro editaci.
     * @details Pokud je hodnota null nebo undefined, formulář se přepne do režimu vytváření nového záznamu.
     * @type {Number|String|null}
     */
    buildingId: { type: [Number, String], default: null },
    /**
     * @brief Počáteční zeměpisná šířka.
     * @details Použito pro předvyplnění formuláře v režimu vytváření (např. z kliknutí do mapy).
     * @type {Number|null}
     */
    gpsLat: { type: Number, default: null },
    /**
     * @brief Počáteční zeměpisná délka.
     * @details Použito pro předvyplnění formuláře v režimu vytváření.
     * @type {Number|null}
     */
    gpsLng: { type: Number, default: null },
  },
  data() {
    return {
      internalBuildingId: null,
      isLoading: false,
      isSaving: false,
      isFormValid: false,
      formData: getInitialFormData(),
      dateMenu: false,
      showSuccessAlert: false,
      showErrorAlert: false,
      alertMessage: '',
      // Make constants available to the template
      operationTypeItems: OPERATION_TYPE_ITEMS,
      OPERATION_TYPE_CUSTOM: OPERATION_TYPE_CUSTOM,
      objectTypeItems: OBJECT_TYPE_ITEMS,
      CUSTOM_OBJECT_TYPE: CUSTOM_OBJECT_TYPE,
    };
  },
  computed: {
    /**
     * Určuje, zda je formulář v editačním režimu. Vrací true, pokud `internalBuildingId` není null.
     * @method isEditMode
     * @type {boolean}
     */
    isEditMode() {
      return this.internalBuildingId !== null;
    },
  },
  methods: {
    /**
     * Inicializuje formulář. Rozhoduje, zda se data mají načíst z API (editace) nebo resetovat na výchozí hodnoty (vytváření).
     * Nastavuje stav `isLoading`.
     * @method initializeForm
     * @return {Promise<void>}
     */
    async initializeForm() {
      this.isLoading = true;
      if (this.isEditMode) {
        await this.fetchBuildingData();
      } else {
        this.resetForm();
      }
      this.isLoading = false;
    },

    /**
     * Resetuje formulář do výchozího stavu.
     * Vymaže všechna pole, nastaví aktuálního uživatele jako zodpovědnou osobu 
     * a předvyplní GPS souřadnice, pokud jsou k dispozici v props.
     * @method resetForm
     * @public
     */
    resetForm() {
      this.formData = getInitialFormData();
      this.formData.responsible_person = this.$keycloak?.tokenParsed?.name || 'Guest';
      if (!this.isEditMode) {
        this.formData.gps_lat = this.gpsLat;
        this.formData.gps_long = this.gpsLng;
      }
    },

    /**
     * Načte data o budově z API.
     * Provádí GET požadavek. Zároveň mapuje příchozí data na formát formuláře.
     * Speciálně řeší situaci, kdy `operation_type` nebo `object_type` neodpovídá
     * předdefinovaným položkám v seznamu -> přepne select na "Uživatelská volba" 
     * a vyplní textové pole pro vlastní hodnotu.
     * @method fetchBuildingData
     * @return {Promise<void>}
     */
    async fetchBuildingData() {
      if (!this.internalBuildingId) return;
      try {
        const response = await api.getBuilding(this.internalBuildingId);
        this.formData = { ...getInitialFormData(), ...response.data };

        // Handle custom operation_type values from the API
        const predefinedOperationValues = this.operationTypeItems.filter(item => item.value).map(item => item.value);
        if (response.data.operation_type && !predefinedOperationValues.includes(response.data.operation_type)) {
          this.formData.operation_type = OPERATION_TYPE_CUSTOM;
          this.formData.operation_type_custom = response.data.operation_type;
        }

        // Handle custom object_type values from the API
        const predefinedObjectValues = this.objectTypeItems.filter(item => item.value).map(item => item.value);
        if (response.data.object_type && !predefinedObjectValues.includes(response.data.object_type)) {
          this.formData.object_type = CUSTOM_OBJECT_TYPE;
          this.formData.object_type_custom = response.data.object_type;
        }

        if (response.data.created_date) {
          this.formData.created_date = new Date(response.data.created_date);
        }
      } catch (error) {
        this.handleApiError(error);
      }
    },

    /**
     * Hlavní metoda pro odeslání formuláře.
     * Validuje formulář a rozhoduje, zda volat `createBuilding` nebo `updateBuilding`.
     * @method submitForm
     */
    submitForm() {
      if (!this.isFormValid) return;
      if (this.isEditMode) {
        this.updateBuilding();
      } else {
        this.createBuilding();
      }
    },

    /**
     * Připraví datový payload pro API.
     * 1. Kopíruje data z formuláře.
     * 2. Řeší logiku "Vlastní volby": pokud je vybrána možnost "Uživatelská volba",
     *    přepíše hodnotu selectu hodnotou z doplňkového textového pole.
     * 3. Formátuje datum vytvoření do formátu `YYYY-MM-DD`.
     * 4. Odstraňuje pomocné proměnné (`_custom` pole) z objektu.
     * @method preparePayload
     * @return {Object} Objekt připravený k odeslání na server.
     */
    preparePayload() {
      const payload = { ...this.formData };

      // Handle custom operation type
      if (payload.operation_type === OPERATION_TYPE_CUSTOM) {
        payload.operation_type = payload.operation_type_custom;
      }
      delete payload.operation_type_custom;

      // Handle custom object type
      if (payload.object_type === CUSTOM_OBJECT_TYPE) {
        payload.object_type = payload.object_type_custom;
      }
      delete payload.object_type_custom;

      payload.created_date = formatDateForApi(payload.created_date);
      return payload;
    },

    /**
     * Vytvoří nový záznam budovy (POST).
     * Při úspěchu emituje událost `building-created` a zobrazí success notifikaci.
     * @method createBuilding
     * @return {Promise<void>}
     */
    async createBuilding() {
      this.isSaving = true;
      try {
        const payload = this.preparePayload();
        const response = await api.createBuilding(payload);
        this.internalBuildingId = response.data.id;
        this.alertMessage = 'Záznam o stavbě byl úspěšně vytvořen.';
        this.showSuccessAlert = true;
        this.$emit('building-created', response.data.id);
        await this.fetchBuildingData();
      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.isSaving = false;
      }
    },

   /**
     * Aktualizuje existující záznam budovy (PUT).
     * Při úspěchu emituje událost `building-updated` a zobrazí success notifikaci.
     * @method updateBuilding
     * @return {Promise<void>}
     */
    async updateBuilding() {
      this.isSaving = true;
      try {
        const payload = this.preparePayload();
        const response = await api.updateBuilding(this.internalBuildingId, payload);
        this.alertMessage = 'Změny byly úspěšně uloženy.';
        this.showSuccessAlert = true;
        this.$emit('building-updated', response.data.id);
      } catch (error) {
        this.handleApiError(error);
      } finally {
        this.isSaving = false;
      }
    },

    /**
     * Formátuje datum pro zobrazení v UI (český formát).
     * @param {Date|string} date - Vstupní datum.
     * @method formattedDateForDisplay
     * @return {string|null} Datum ve formátu 'dd.mm.yyyy' nebo null.
     */
    formattedDateForDisplay(date) {
      if (!date) return null;
      const d = date instanceof Date ? date : new Date(date);
      return d.toLocaleDateString('cs-CZ');
    },
    /**
     * Zpracovává chyby z API volání.
     * Rozlišuje typy chyb (409 Konflikt, síťové chyby) a nastavuje chybovou hlášku pro Snackbar.
     * @method handleApiError
     * @param {Error} error - Objekt chyby (Axios error).
     */
    handleApiError(error) {
      if (error.response) {
        if (error.response.status === 409) {
          this.alertMessage = 'Záznam s tímto identifikátorem již existuje.';
        } else {
          this.alertMessage = `Chyba serveru: ${error.response.statusText} (kód: ${error.response.status})`;
        }
      } else if (error.request) {
        this.alertMessage = 'Chyba sítě: Server neodpovídá.';
      } else {
        this.alertMessage = 'Nastala neočekávaná chyba.';
      }
      this.showErrorAlert = true;
      console.error("API Error:", error);
    }
  },
  mounted() {
    this.internalBuildingId = this.buildingId;
    this.initializeForm();
  },
  watch: {
    buildingId: {
      handler(newId) {
        if (newId !== this.internalBuildingId) {
          this.internalBuildingId = newId;
          this.initializeForm();
        }
      },
    }
  }
};
</script>

<style scoped>
.procedure-list {
  padding-left: 20px;
  font-size: 0.875rem;
}
.procedure-list li {
  margin-bottom: 8px;
  padding-left: 4px;
}
.procedure-list li:last-child {
  margin-bottom: 0;
}
</style>