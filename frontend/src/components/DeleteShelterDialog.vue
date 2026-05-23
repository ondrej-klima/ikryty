<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="auto"
    >
      <v-card>
        <v-toolbar color="primary" :title="$t('shelter.removeShelter')">
        </v-toolbar>
        <v-card-text>
          {{ $t("shelter.removeQuestion", { name: name }) }}
        </v-card-text>
        <v-card-actions>
          <v-btn variant="tonal" prepend-icon="mdi-trash-can" color="primary" @click="deleteShelter">{{ $t("shelter.delete") }}</v-btn>
          <v-btn color="primary" prepend-icon="mdi-close-circle" @click="dialog = false">{{ $t("shelter.cancel") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  /**
 * @file deleteShelterDialog.vue
 * @brief Dialogové okno pro potvrzení smazání záznamu.
 * 
 * @description
 * Tato komponenta zobrazuje jednoduché modální okno (v-dialog), které vyžaduje
 * potvrzení uživatele před smazáním záznamu.
 * 
 * **Důležitá poznámka k implementaci:**
 * Ačkoliv název komponenty a lokalizační klíče odkazují na "Shelter" (úkryt),
 * metoda `deleteShelter` volá `api.deleteBuilding`. To znamená, že tato komponenta
 * v aktuálním kontextu slouží k odstranění celé budovy (která je v systému
 * vedena jako nadřazený prvek úkrytů).
 * 
 * @component
 * @example
 * <delete-shelter-dialog ref="deleteDialog" />
 * // Volání z rodiče:
 * this.$refs.deleteDialog.showDialog(123, "Budova A");
 */

import {defineComponent} from "vue";
import {useShelterStore} from "@/stores/shelterStore";
import api from "@/services/api"
export default defineComponent({
  data() {
    return {
      dialog: false,
      id: null,
      name: null
    }
  },
  methods: {
     /**
     * Otevře dialogové okno a nastaví kontext pro mazání.
     * 
     * @param {number|string} id - ID záznamu, který se má smazat.
     * @param {string} name - Název záznamu (zobrazí se v potvrzovací otázce).
     * @public
     * @method showDialog
     * @return {void}
     */
    showDialog(id, name) {
      this.$data.id = id
      this.$data.name = name
      this.$data.dialog = true
    },

     /**
     * Provede smazání záznamu.
     * Volá API endpoint pro smazání budovy (`api.deleteBuilding`) na základě uloženého ID.
     * Po úspěšném smazání aktualizuje seznam úkrytů v `ShelterStore` a zavře dialog.
     * 
     * @public
     * @method deleteShelter
     * @return {void}
     */
    deleteShelter() {
      if (this.$data.id) {
        //useShelterStore().deleteShelter(this.$data.id)
        api.deleteBuilding(this.$data.id)
        useShelterStore().getUserShelters();
      }
      this.$data.dialog = false
    }
  }
})
</script>
