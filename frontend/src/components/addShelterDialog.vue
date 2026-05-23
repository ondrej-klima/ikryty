<template>
  <div class="text-center">
    <v-dialog v-model="show" width="1024" persistent>
		<v-form fast-fail @submit.prevent="submit">
		<v-card>
    <v-toolbar color="primary" :title="$t('shelter.title')">
            <v-btn
				variant="tonal"
                prepend-icon="mdi-close-circle"
                @click="show = false"
			>
            {{ $t("shelter.close") }}
            </v-btn>
    </v-toolbar>

    <div class="d-flex flex-row">
      <v-tabs
        v-model="tab"
        color="primary"
        direction="vertical"
      >
		<v-tab
			:prepend-icon="$t('tabs.step1_icon')"
			:text="$t('tabs.step1_text')"
			value="building-info-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step2_icon')"
			:text="$t('tabs.step2_text')"
			:disabled="!selectedBuildingId"
			value="territory-analysis-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step3_icon')"
			:text="$t('tabs.step3_text')"
			:disabled="!selectedBuildingId"
			value="shelter-identification-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step4_icon')"
			:text="$t('tabs.step4_text')"
			:disabled="!selectedBuildingId"
			value="structural-assessment-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step5_icon')"
			:text="$t('tabs.step5_text')"
			:disabled="!selectedBuildingId"
			value="threat-assessment-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step6_icon')"
			:text="$t('tabs.step6_text')"
			:disabled="!selectedBuildingId"
			value="overall-assessment-form"
			class="tab-wrap"
		></v-tab>
		
		<v-tab
			:prepend-icon="$t('tabs.step7_icon')"
			:text="$t('tabs.step7_text')"
			:disabled="!selectedBuildingId"
			value="review-and-approval-form"
			class="tab-wrap"
		></v-tab>
      </v-tabs>

      <v-tabs-window v-model="tab">
		<A1Form       
            :building-id="selectedBuildingId"
            :gps-lat="newGpsLat"
            :gps-lng="newGpsLng"
            @building-created="handleCreation"
            @building-updated="handleUpdate"
		/>
		<A2Form 
			:building-id="selectedBuildingId"
			@building-updated="handleUpdate"
		/>
		<A3Form 
			:building-id="selectedBuildingId"
			@building-updated="handleUpdate"
		/>
		<A4Form 
			:building-id="selectedBuildingId"
			:is-active="tab === 'structural-assessment-form'"
			@building-updated="handleUpdate"		
		/>
		<A5Form
			:building-id="selectedBuildingId"
			:is-active="tab === 'threat-assessment-form'"
			@building-updated="handleUpdate"	
		/>
		<A6Form 
			:building-id="selectedBuildingId"
			:is-active="tab === 'overall-assessment-form'"
			@building-updated="handleUpdate"
		/>
		<A7Form
			:building-id="selectedBuildingId"
			:is-active="tab === 'review-and-approval-form'"
			@building-updated="handleUpdate"		
		/>
      </v-tabs-window>
    </div>
  </v-card>

	</v-form>
    </v-dialog>
  </div>
</template>

<script>
/**
 * @file addShelterDialog.vue
 * @brief Hlavní dialog pro správu procesu evidence úkrytu (Průvodce).
 * 
 * @description
 * Tato komponenta slouží jako kontejner (wrapper) pro celý 7krokový proces evidence budovy a úkrytů.
 * Obsahuje dialogové okno (`v-dialog`), které zobrazuje jednotlivé kroky (formuláře) pomocí 
 * vertikálních záložek (`v-tabs`).
 * 
 * Hlavní funkce:
 * - **Řízení stavu:** Spravuje aktuálně vybranou budovu (`selectedBuildingId`) a GPS souřadnice.
 * - **Navigace:** Umožňuje přepínání mezi kroky A1 až A7. Záložky A2-A7 jsou zablokované, 
 *   dokud není v kroku A1 vytvořena nebo vybrána budova.
 * - **Koordinace:** Předává `buildingId` a signály o aktualizaci mezi jednotlivými pod-komponentami.
 * - **Inicializace:** Metoda `showDialog` nastaví formulář pro vytvoření nové budovy (z mapy) 
 *   nebo editaci existující (z DB).
 * 
 * Struktura kroků:
 * 1. A1Form: Základní údaje o budově.
 * 2. A2Form: Analýza území.
 * 3. A3Form: Identifikace úkrytů.
 * 4. A4Form: Stavební posouzení.
 * 5. A5Form: Posouzení ohroženosti.
 * 6. A6Form: Celkové hodnocení.
 * 7. A7Form: Revize a schválení.
 * 
 * @component
 * @example
 * <add-shelter-dialog ref="dialog" />
 * // Volání z rodiče:
 * this.$refs.dialog.showDialog({ lat: 49.1, lng: 16.6, id: 123 });
 */

import {useShelterStore} from "@/stores/shelterStore";
import {useTargetStore } from "@/stores/targetStore";
// import {nextTick} from "vue";
import A1Form from "./A1Form.vue";
import A2Form from "./A2Form.vue";
import A3Form from "./A3Form.vue";
import A4Form from "./A4Form.vue";
import A5Form from "./A5Form.vue";
import A6Form from "./A6Form.vue";
import A7Form from "./A7Form.vue";

export default {
  name: "addShelterDialog",
  components: {
    A1Form, 
	A2Form,
	A3Form,
	A4Form,
	A5Form,
	A6Form,
	A7Form
  },
  data () {
    return {
      selectedBuildingId: null,
      newGpsLat: null,
      newGpsLng: null,
      show: false,
      tab: 'option-1',
      shelter_id: null,
      user: null,
      form: {
        name: null,
        x: null,
        y: null,
				buildingType: null,
				buildingSubType: null,
				materialType: null,
				materialSubType: null,
				width: null,
				height: null,
				depth: null,
				thickness: null,
				type: null,
				TP: null,
				NV: null,
				SV: null,
				NC: null,
				mind: null,
				SO: null,
				SOV: null, 
				SC: null,
			},
			buildingTypesItems: null,
			materialTypesItems: null,
			tpItems: [
				{id: null, caption: null},
				{id: 1, caption: "TP-1 - Podzemní prostor (viz oddíl 3.3.2)."}, 
				{id: 2, caption: "TP-2 - Suterénní prostor (viz oddíl 3.3.1) zapuštěných nejméně do dvou třetin výšky místnosti pod úroveň terénu."},
				{id: 3, caption: "TP-3 - Prostor ve vnitřním traktu (viz oddíl 3.3.3)."}
			],
			nvItems: [
				{id: null, caption: null},
				{id: 1, caption: "NV-1 - Nouzový východ z improvizovaného úkrytu je již vybudován nebo jej lze snadno vybudovat..."}, // bez nutnosti zásahů do nosných konstrukcí stavby (viz oddíl 3.5.5)."},
				{id: 0, caption: "NV-0 - Nouzový východ není vybudován a nelze jej snadno vybudovat..."} //" bez nutnosti zásahů do nosných konstrukcí stavby (viz oddíl 3.5.5)."}
			],
			svItems: [
				{id: null, caption: null},
				{id: 1, caption: "SV-1 - Systém ventilace vzduchu je již vybudován nebo jej lze snadno vybudovat..."}, // bez nutnosti zásahů do nosných konstrukcí stavby (viz příloha 1)."},
				{id: 0, caption: "SV-0 - Systém ventilace vzduchu není vybudován a nelze jej snadno vybudovat..."} // bez nutnosti zásahů do nosných konstrukcí stavby (viz příloha 1)."}
			],
      rules: [
        value => {
          if (value) return true
          return false
        }
      ],
	headers: [
        { title: 'Typ prostoru (TP)', key: 'tp', align: 'start', sortable: false },
        { title: 'Nouzový východ (NV)', key: 'nv', align: 'start', sortable: false },
        { title: 'Systém ventilace (SV)', key: 'sv', align: 'start', sortable: false },
        { title: 'Skóre (SOV)', key: 'sov', align: 'center', sortable: true },
      ],

      // The data from your table, structured as an array of objects
      sovRules: [
        { tp: 'TP-1', nv: 'NV-1', sv: 'SV-1', sov: 1.00 },
        { tp: 'TP-2', nv: 'NV-1', sv: 'SV-1', sov: 0.95 },
        { tp: 'TP-1', nv: 'NV-0', sv: 'SV-1', sov: 0.90 },
        { tp: 'TP-2', nv: 'NV-0', sv: 'SV-1', sov: 0.85 },
        { tp: 'TP-1', nv: 'NV-1', sv: 'SV-0', sov: 0.75 },
        { tp: 'TP-2', nv: 'NV-1', sv: 'SV-0', sov: 0.70 },
        { tp: 'TP-1', nv: 'NV-0', sv: 'SV-0', sov: 0.65 },
        { tp: 'TP-2', nv: 'NV-0', sv: 'SV-0', sov: 0.60 },
        { tp: 'TP-3', nv: 'nehodnotí se', sv: 'nehodnotí se', sov: 0.10 },
      ],
		soHeaders: [
        { 
          title: 'Vzdálenost od nebližšího možného terče útoku', 
          key: 'distance', 
          align: 'start',
          sortable: false 
        },
        { 
          title: 'Skóre ohroženosti (SO)', 
          key: 'score', 
          align: 'center',
          sortable: false
        },
      ],

      // 2. The data for the table, structured as an array of objects.
      soThreatScores: [
        { distance: 'Méně než 100 m', score: 3 },
        { distance: '100 m až 500 m', score: 2 },
        { distance: 'Více než 500 m', score: 1 },
      ],
		equation: 'S_C = \\frac{500 \\cdot S_{OV}}{N_C \\cdot S_O}',
    }
  },
	watch: {
		'form.buildingType': function() {
			this.$data.form.buildingSubType = null
		},
		'form.materialType': function() {
			this.$data.form.materialSubType = null
		},
		'sc': function() {
			this.$data.form.SC = this.sc
		},
		'so': function() {
			this.$data.form.SO = this.so
		},
		'sov': function() {
			this.$data.form.SOV = this.sov
		}
	},
  methods: {
    /**
     * Nastaví dialog do režimu editace existující budovy (pro testovací účely).
     * @public
     * @method selectExistingBuilding
     */
	selectExistingBuilding() {
      this.selectedBuildingId = 123; // ID z databáze
      this.newGpsLat = null; // V edit módu se GPS načte z DB, ne z props
      this.newGpsLng = null;
    },

    /**
     * Nastaví dialog do režimu vytváření nové budovy (pro testovací účely).
     * @public
     * @method selectNewLocation
     */
    selectNewLocation() {
      this.selectedBuildingId = null; // Klíčové pro "Create" mód
      this.newGpsLat = 49.1951; // Souřadnice z kliknutí na mapu
      this.newGpsLng = 16.6068;
    },

    /**
     * Callback funkce volaná z A1Form po úspěšném vytvoření nové budovy.
     * Uloží ID nové budovy, čímž odemkne ostatní záložky.
     * 
     * @param {number|string} newId - ID nově vytvořené budovy.
     * @public
     * @method handleCreation
     * @return {Promise<void>}
     */
    async handleCreation(newId) {
      //alert(`Vytvořena nová budova s ID: ${newId}. Můžete přesměrovat na editaci.`);
      this.selectedBuildingId = newId; // Přepne formulář do edit módu
      await useShelterStore().getUserShelters();
    },

    /**
     * Callback funkce volaná z pod-formulářů po úspěšné aktualizaci dat.
     * Slouží primárně pro logování nebo zobrazení globální notifikace.
     * 
     * @param {number|string} updatedId - ID aktualizované budovy.
     * @public
     * @method handleUpdate
     */
    handleUpdate(updatedId) {
      //alert(`Budova s ID: ${updatedId} byla aktualizována.`);
      console.log(`Budova s ID: ${updatedId} byla aktualizována.`)
    },

    /**
     * Hlavní metoda pro otevření dialogu.
     * Nastaví stav dialogu podle předaných parametrů (Create vs Edit).
     * Pokud je předáno `coords.id`, načte data pro editaci.
     * Pokud není ID, připraví formulář pro nový záznam na daných souřadnicích.
     * 
     * @param {Object} coords - Objekt s parametry {lat, lng, id, label}.
     * @public
     * @method showDialog
     * @return {Promise<void>}
     */
    async showDialog(coords) {
			this.$data.tab = "building-info-form";
			if(coords.id) {
				this.$data.selectedBuildingId = coords.id
				this.$data.shelter_id = coords.id
				/*
				let info = useShelterStore().$state.shelters.find(t => t.id == coords.id)
				this.$data.user = info.user
				this.$data.form.address = info.address
				this.$data.form.name = info.name
				this.$data.form.description = info.description
				this.$data.form.x = info.x
				this.$data.form.y = info.y
				this.$data.form.buildingType = info.building_subtype?.building_type.id || null
				nextTick(() => {
					this.$data.form.buildingSubType = info.building_subtype?.id || null
				})
				this.$data.form.width = info.protectivespaces[0].width
				this.$data.form.height = info.protectivespaces[0].height
				this.$data.form.depth = info.protectivespaces[0].depth
				this.$data.form.type = info.protectivespaces[0].type
				this.$data.form.thickness = info.protectivespaces[0].thickness
				this.$data.form.materialType = info.protectivespaces[0].material_subtype?.material_type.id || null
				nextTick(() => {
					this.$data.form.materialSubType = info.protectivespaces[0].material_subtype?.id || null 
				})
				*/

				await useTargetStore().getMinDistance(coords.lat, coords.lng)
				if(useTargetStore().$state.minDistance['d']) {
					this.$data.form.mind = Math.round(useTargetStore().$state.minDistance['d'])
				}
				else {
					this.$data.form.mind = null
				}
				/*
				this.$data.form.NC = info.NC
				this.$data.form.NV = info.NV
				this.$data.form.TP = info.TP
				this.$data.form.SV = info.SV
				*/
			}
			else {
				this.$data.selectedBuildingId = null
				this.$data.newGpsLat = coords.lat
				this.$data.newGpsLng = coords.lng

				/*
				this.$data.shelter_id = null
				this.$data.form.name = null
				this.$data.form.address = null
				this.$data.form.description = null
				this.$data.shelter_id = null
				this.$data.form.y = coords.lng
				this.$data.form.x = coords.lat
				*/
				await useTargetStore().getMinDistance(coords.lat, coords.lng)
				this.$data.form.mind = Math.round(useTargetStore().$state.minDistance['d'])
				/*
				this.$data.user = this.$keycloak.tokenParsed.preferred_username
				this.$data.form.NC = null
				this.$data.form.NV = null
				this.$data.form.TP = null
				this.$data.form.SV = null
				this.$data.form.buildingType = null
				this.$data.form.buildingSubType = null
				this.$data.form.width = null
				this.$data.form.height = null
				this.$data.form.depth = null
				this.$data.form.type = null
				this.$data.form.thickness = null
				this.$data.form.materialType = null
				this.$data.form.materialSubType = null 	
				*/
			}
			if(coords.label) {
				this.$data.form.address = coords.label.toString()
			}
      this.$data.show = true
    },

    /**
     * Metoda pro odeslání starého formuláře (submit).
     * V novém designu je tato logika přesunuta do jednotlivých pod-komponent (A1-A7),
     * ale zde zůstává pro případné uložení celkového kontextu.
     * 
     * @public
     * @method submit
     * @return {Promise<void>}
     */
    async submit() {
      //if(this.$data.form.name) {
				this.$data.show = false
				if(!this.$data.shelter_id) {
					await useShelterStore().createShelter(this.$data.form)
				}
				else {
					await useShelterStore().updateShelter(this.$data.form, this.$data.shelter_id)
				}
      //}
      //this.$data.form.name = null
    },
    /**
     * A master function that returns a CSS class based on the cell's value.
     * @param {*} value The value of the cell (can be string or number).
     * @returns {string} The CSS class(es) to apply.
     */

    /**
     * Pomocná funkce pro styling buněk v tabulkách nápovědy.
     * Vrací CSS třídu na základě hodnoty buňky (např. barva podle skóre).
     * 
     * @param {*} value - Hodnota buňky.
     * @returns {string} Název CSS třídy.
     * @public
     * @method getCellClass
     */
	getCellClass(value) {
      // Handle the string-based values first
      switch (value) {
        case 'TP-1': return 'bg-tp1';
        case 'TP-2': return 'bg-tp2';
        case 'TP-3': return 'bg-tp3';
        case 'NV-1': return 'bg-nv1';
        case 'NV-0': return 'bg-nv0';
        case 'SV-1': return 'bg-sv1';
        case 'SV-0': return 'bg-sv0';
        case 'nehodnotí se': return 'bg-not-rated';
      }

      // If it's a number, handle the SOV scores
      if (typeof value === 'number') {
        if (value >= 0.9) return 'bg-high-score';
        if (value >= 0.7) return 'bg-medium-score';
        if (value >= 0.6) return 'bg-low-score';
        return 'bg-very-low-score';
      }
      
      // Return a default class if no match
      return 'bg-default';
    },

    /**
     * Formátuje číselnou hodnotu skóre SOV (2 desetinná místa, čárka).
     * @param {number} value - Hodnota skóre.
     * @returns {string} Formátovaný řetězec.
     * @public
     * @method formatSov
     */
    formatSov(value) {
      return value.toFixed(2).replace('.', ',');
    }
  }//,
  /*
	computed: {
		buildingSubTypesItems() {
			if(this.$data.form.buildingType) {
				return [{id:null, caption:null}].concat(this.$data.buildingTypesItems.find(t => t.id == this.$data.form.buildingType).buildingsubtypes)
			}
			else return [{id:null, caption:null}]
		},
		materialSubTypesItems() {
			if(this.$data.form.materialType) {
				return [{id:null, caption:null}].concat(this.$data.materialTypesItems.find(t => t.id == this.$data.form.materialType).materialsubtypes)
			}
			else return [{id:null, caption:null}]
		},
		sov() {
			if(this.form.TP == null || this.form.NV == null || this.form.SV == null)
				return null

			// Speciální případ pro TP-3, který má vždy SOV 0.1
			if (this.form.tp == 3) {
				return 0.1;
			}

			// Definuje pravidla z tabulky jako datovou strukturu (mapu)
			const scoreMap = {
				'1_1_1': 1,
				'2_1_1': 0.95,
				'1_0_1': 0.9,
				'2_0_1': 0.85,
				'1_1_0': 0.75,
				'2_1_0': 0.7,
				'1_0_0': 0.65,
				'2_0_0': 0.6,
			};

			// Vytvoří unikátní klíč z aktuálních hodnot
			const key = `${this.form.TP}_${this.form.NV}_${this.form.SV}`;

			// Vrátí hodnotu z mapy. Pokud klíč neexistuje (neplatná kombinace),
			// vrátí null nebo jinou výchozí hodnotu (např. 0 nebo 'Chyba').
			return scoreMap[key] || null;
		},
		so() {
			if(this.form.mind == null)
				return null
			else if(this.form.mind < 100)
				return 3
			else if(this.form.mind >= 100 && this.form.mind <= 500)
				return 2
			else 
				return 1
		},
		sc() {
			if(this.so == null || this.sov == null || this.form.NC == null)
				return null
			return Math.round(100*(500 * this.sov) / (this.form.NC * this.so))/100
		}
	},
	async mounted() {
		await useShelterStore().initBuildingProperties()
		this.$data.buildingTypesItems = useShelterStore().$state.buildingTypes
		this.$data.materialTypesItems = useShelterStore().$state.materialTypes

		this.$watch('form.buildingType', function() {
			this.$data.buildingSubTypesItems = this.$data.buildingTypesItems.find(t => t.id == this.$data.form.buildingType).buildingsubtypes
		}, {
			deep: true
		})
	}
		*/
}
</script>

<style scoped>
.tab-wrap {
  /* 1. Nastavíme maximální šířku celé záložky */
  max-width: 275px;
  
  /* 2. Necháme výšku, ať se přizpůsobí obsahu */
  height: auto !important;
  min-height: 56px; /* Mírně vyšší pro lepší vzhled */
}

/* Můžeme také ovlivnit vnitřní div, který drží text */
.tab-wrap :deep(.v-tab__content) {
  /* Povolíme zalamování */
  white-space: normal;
  
  /* Upravíme zarovnání a řádkování pro lepší čitelnost */
  text-align: left;
  line-height: 1.3;
  padding: 12px 0; /* Přidáme vertikální padding pro vícerádkový text */
}

/* 
  Use :deep() to apply styles to the <td> elements inside the v-data-table.
  The !important flag helps override Vuetify's default styling.
*/

/* --- Default and Generic --- */
.v-data-table :deep(td) {
  font-weight: 500;
  text-align: center;
}
.v-data-table :deep(td.bg-not-rated) {
  background-color: #F5F5F5 !important; /* Grey lighten-4 */
  color: #616161;
  font-style: italic;
}

/* --- TP Column Colors --- */
.v-data-table :deep(td.bg-tp1) { background-color: #E8F5E9 !important; color: #1565C0; } /* Light Blue */
.v-data-table :deep(td.bg-tp2) { background-color: #fffcbd !important; color: #00695C; } /* Light Teal */
.v-data-table :deep(td.bg-tp3) { background-color: #ffdec8 !important; color: #6A1B9A; } /* Light Purple */

/* --- NV Column Colors --- */
.v-data-table :deep(td.bg-nv1) { background-color: #E8F5E9 !important; color: #2E7D32; } /* Light Green */
.v-data-table :deep(td.bg-nv0) { background-color: #ffdec8 !important; color: #C62828; } /* Light Red */

/* --- SV Column Colors --- */
.v-data-table :deep(td.bg-sv1) { background-color: #E8F5E9 !important; color: #2E7D32; } /* Same as NV-1 */
.v-data-table :deep(td.bg-sv0) { background-color: #ffdec8 !important; color: #C62828; } /* Same as NV-0 */

/* --- SOV Column Colors (using a gradient idea) --- */
/*.v-data-table :deep(td.bg-high-score) { background-color: #A5D6A7 !important; color: #1B5E20; } /* Green */
/*.v-data-table :deep(td.bg-medium-score) { background-color: #FFF59D !important; color: #F9A825; } /* Yellow */
/*.v-data-table :deep(td.bg-low-score) { background-color: #FFAB91 !important; color: #D84315; } /* Orange */
/*.v-data-table :deep(td.bg-very-low-score) { background-color: #EF9A9A !important; color: #B71C1C; } /* Red */
</style>
