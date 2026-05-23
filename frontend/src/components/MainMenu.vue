<template>
  <v-card>
    <v-toolbar
        color="primary"
    >
      <v-toolbar-title>{{ $t("menu.mainMenu") }}</v-toolbar-title>
    </v-toolbar>
    <div class="d-flex flex-row">
      <v-tabs
          v-model="tab"
          direction="vertical"
          color="primary"
      >
        <v-tab value="option-1">
          <v-icon start>
            mdi-home
          </v-icon>
          {{ $t("menu.shelters") }}
        </v-tab>
        <v-tab value="option-2">
          <v-icon start>
            mdi-star
          </v-icon>
          {{ $t("menu.targets") }}
        </v-tab>
      </v-tabs>
      <v-window v-model="tab">
        <v-window-item value="option-1">
          <v-card flat>
            <v-card-text>
              <v-data-table :items="items" :headers="shelterHeaders"></v-data-table>
            </v-card-text>
          </v-card>
        </v-window-item>
        <v-window-item value="option-2">
          <v-card flat>
            <v-card-text>
              <v-data-table :items="targetItems" :headers="targetHeaders"></v-data-table>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </div>
  </v-card>

</template>

<script>
  /**
 * @file MainMenu.vue
 * @brief Hlavní menu (Sidebar) aplikace.
 * 
 * @description
 * Tato komponenta zobrazuje obsah postranního panelu (Sidebar).
 * Obsahuje dvě záložky (Tabs):
 * 1. **Úkryty (Shelters):** Tabulka se seznamem všech načtených úkrytů.
 * 2. **Cíle (Targets):** Tabulka se seznamem všech definovaných cílů.
 * 
 * Data jsou čerpána reaktivně přímo ze store (`useShelterStore`, `useTargetStore`).
 * Pro zobrazení dat je použita komponenta `v-data-table`.
 * 
 * @component
 * @example
 * <main-menu />
 */

import { useShelterStore } from '@/stores/shelterStore';
import { useTargetStore } from '@/stores/targetStore';


export default {
  name: 'MainMenu',
  data() {
    return {
      tab: 'option-1',
      shelterHeaders: [
        {key:'id',title:'ID'},
        {key:'user_id',title:'Uživatel'},
        {key:'name_address',title:'Název/adresa'},
        {key:'max_s_c',title:'S_C'}
      ],
      targetHeaders: [
        {key:'id',title:'ID'},
        {key:'user',title:'Uživatel'},
        {key:'name',title:'Název'},
        {key:'address',title:'Adresa'},
      ]
    }
  }, 
  computed: {
    /**
     * Vrací seznam úkrytů ze store.
     * Pokud data nejsou načtena, vrací pole s prázdným objektem (aby tabulka nespadla).
     * @type {Array<Object>}
     */
    items() {
      //return useShelterStore()?.stateShelters | [{a: 1}, {b: 2}]
      //console.log(useShelterStore()?.stateShelters)
      //console.log(useShelterStore().$state.buildingTypes)
      //console.log(useShelterStore()?.$state?.shelters | [{}])
      if(useShelterStore().$state.shelters !== null)
        return useShelterStore()?.$state?.shelters
      return [{}]
    },
        /**
     * Vrací seznam cílů ze store.
     * Pokud data nejsou načtena, vrací pole s prázdným objektem.
     * @type {Array<Object>}
     */
    targetItems() {
      if(useTargetStore().$state.targets !== null)
        return useTargetStore()?.$state?.targets
      return [{}]
    }
  }
}
</script>
