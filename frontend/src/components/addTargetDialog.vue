<template>
  <div class="text-center">
    <v-dialog v-model="show" width="1024" persistent>
      <v-form fast-fail @submit.prevent="submit">
      <v-card>
        <v-toolbar color="primary" :title="$t('target.title')">
          <v-chip prepend-icon="mdi-account">{{ user }}</v-chip>&nbsp;
          <v-btn
                type="submit"
                variant="tonal"
				prepend-icon="mdi-content-save"
            >
              {{ $t("shelter.save") }}
            </v-btn>&nbsp;
            <v-btn
				variant="tonal"
                prepend-icon="mdi-close-circle"
                @click="show = false"
            >{{ $t("shelter.cancel") }}
            </v-btn>
        </v-toolbar>
          <v-card-title v-if="false">
            <span class="text-h5" v-if="!target_id">{{ $t("target.addTarget") }}</span>
						<span class="text-h5" v-else>{{ $t("target.editTarget") }} {{target_id}}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field :label="$t('target.targetName')" v-model="form.name"></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('target.targetAddress')" v-model="form.address"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                    <v-text-field :label="$t('target.longitude')" suffix="°" v-model="form.x" readonly></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field :label="$t('target.latitude')" suffix="°" v-model="form.y" readonly></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea :label="$t('target.targetDescription')" v-model="form.description"></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-form>
    </v-dialog>
  </div>
</template>

<script>
  /**
 * @file addTargetDialog.vue
 * @brief Dialogové okno pro správu Cílů (Targets).
 * 
 * @description
 * Tato komponenta slouží k vytváření nových nebo editaci existujících Cílů útoku.
 * Cíle jsou body na mapě (definované GPS souřadnicemi), ke kterým se vztahuje 
 * výpočet ohroženosti úkrytů (Krok 5 v evidenci úkrytu).
 * 
 * Hlavní funkce:
 * - **Vytvoření (Create):** Otevře se kliknutím do mapy. Předvyplní GPS souřadnice a adresu (pokud je dostupná z geocodingu).
 * - **Editace (Edit):** Otevře se kliknutím na existující cíl. Načte data ze store.
 * - **Ukládání:** Komunikuje s `TargetStore` pro persistenci dat.
 * 
 * @component
 * @example
 * <add-target-dialog ref="targetDialog" />
 * // Volání z rodiče (mapy):
 * this.$refs.targetDialog.showDialog({ lat: 49.1, lng: 16.6, label: "Brno" });
 */

import {useTargetStore} from "@/stores/targetStore";
import {useShelterStore} from "@/stores/shelterStore"

export default {
  name: "addTargetDialog",
  data () {
    return {
      show: false,
      target_id: null,
      user: null,
      form: {
        name: null,
        x: null,
        y: null,
        address: null,
        description: null
      },
      rules: [
        value => {
          if (value) return true
          return false
        }
      ]
    }
  },
  methods: {
        /**
     * Otevře dialog a inicializuje formulář.
     * Rozlišuje mezi režimem vytváření a editace na základě přítomnosti `coords.id`.
     * 
     * @param {Object} coords - Vstupní data.
     * @param {number|string} [coords.id] - ID cíle (pokud jde o editaci).
     * @param {number} [coords.lat] - Zeměpisná šířka (pokud jde o nový bod).
     * @param {number} [coords.lng] - Zeměpisná délka (pokud jde o nový bod).
     * @param {string} [coords.label] - Adresa nebo popisek místa (z geocodingu).
     * 
     * @public
     * @method showDialog
     * @return {Promise<void>}
     */
    async showDialog(coords) {
			if(coords.id) {
				this.$data.target_id = coords.id
				let info = useTargetStore().$state.targets.find(t => t.id == coords.id)
				this.$data.user = info.user
				this.$data.form.address = info.address
				this.$data.form.x = info.x
				this.$data.form.y = info.y
        this.$data.form.name = info.name
        this.$data.form.description = info.description
			}
			else {
        this.$data.user = this.$keycloak.tokenParsed.preferred_username
				this.$data.target_id = null
				this.$data.form.name = null
				this.$data.form.y = coords.lng
				this.$data.form.x = coords.lat
        this.$data.form.address = null
        this.$data.form.description = null
			}
			if(coords.label) {
				this.$data.form.address = coords.label.toString()
			}
      this.$data.show = true
    },
     /**
     * Odešle formulář na server.
     * Volá `createTarget` nebo `updateTarget` akci v `TargetStore`.
     * Pokud se vytváří nový cíl, aktualizuje také seznam úkrytů (`getUserShelters`), 
     * aby se přepočítaly vzdálenosti k novému cíli.
     * 
     * @public
     * @method submit
     * @return {Promise<void>}
     */
    async submit() {
      //if(this.$data.form.name) {
				this.$data.show = false
				if(!this.$data.target_id) {
					await useTargetStore().createTarget(this.$data.form)
          await useShelterStore().getUserShelters()
				}
				else {
					await useTargetStore().updateTarget(this.$data.form, this.$data.target_id)
				}
      //}
      //this.$data.form.name = null
    }
  },
}
</script>
