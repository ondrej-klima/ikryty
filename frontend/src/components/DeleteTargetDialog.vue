<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="auto"
    >
      <v-card>
        <v-toolbar color="primary" :title="$t('target.removeTarget')">
        </v-toolbar>
        <v-card-text>
          {{ $t("target.removeQuestion", { name: name }) }}
        </v-card-text>
        <v-card-actions>
          <v-btn variant="tonal" color="primary" prepend-icon="mdi-trash-can" @click="deleteTarget">{{ $t("target.delete") }}</v-btn>
          <v-btn variant="tonal" color="primary" prepend-icon="mdi-close-circle" @click="dialog = false">{{ $t("target.cancel") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
/**
 * @file deleteTargetDialog.vue
 * @brief Dialogové okno pro potvrzení smazání Cíle (Target).
 * 
 * @description
 * Tato komponenta zobrazuje modální okno pro bezpečné odstranění cíle útoku.
 * Cíle jsou využívány pro výpočet ohroženosti úkrytů, proto je jejich smazání
 * operace s dopadem na ostatní data.
 * 
 * Hlavní kroky při mazání:
 * 1. Zavolá akci `deleteTarget` v `TargetStore` (smazání z DB).
 * 2. Zavolá akci `getUserShelters` v `ShelterStore`. Toto je kritické, protože
 *    změna seznamu cílů může ovlivnit "vzdálenost k nejbližšímu cíli" u existujících úkrytů.
 * 
 * @component
 * @example
 * <delete-target-dialog ref="delTargetDialog" />
 * // Volání z rodiče:
 * this.$refs.delTargetDialog.showDialog(1, "Hlavní nádraží");
 */

import {defineComponent} from "vue";
import {useTargetStore} from "@/stores/targetStore";
import { useShelterStore } from "@/stores/shelterStore";
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
     * Otevře dialogové okno a nastaví údaje o mazaném cíli.
     * 
     * @param {number|string} id - ID cíle.
     * @param {string} name - Název cíle (pro zobrazení v dotazu).
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
     * Provede smazání cíle a aktualizaci souvisejících dat.
     * Po smazání cíle vynutí přenačtení seznamu úkrytů, aby se aktualizovaly
     * výpočty ohroženosti (vzdálenosti).
     * 
     * @public
     * @method deleteTarget
     * @return {Promise<void>}
     */
    async deleteTarget() {
      if (this.$data.id) {
        await useTargetStore().deleteTarget(this.$data.id)
        await useShelterStore().getUserShelters()
      }
      this.$data.dialog = false
    }
  }
})
</script>
