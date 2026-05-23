<template>
  <v-card>
    <v-toolbar
        color="primary"
    >
      <v-toolbar-title>{{ $t("menu.mainMenu") }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
          :loading="isExporting"
          :disabled="isExporting"
          variant="tonal"
          color="white"
          prepend-icon="mdi-microsoft-excel"
          class="mr-2"
          @click="downloadExport"
      >
        {{ $t("menu.exportExcel") }}
      </v-btn>
    </v-toolbar>
    <v-card-text class="py-3">
      <div class="capacity-summary">
        <div class="capacity-summary__item">
          <div class="capacity-summary__label-row">
            <span class="capacity-summary__abbr">N_K</span>
            <span class="capacity-summary__caption">Kapacita IÚ při krátkodobém ukrytí (max. 2 hod.)</span>
          </div>
          <div class="capacity-summary__value">{{ visibleCapacityTotals.total_n_k }}</div>
        </div>
        <div class="capacity-summary__item">
          <div class="capacity-summary__label-row">
            <span class="capacity-summary__abbr">N_KS</span>
            <span class="capacity-summary__caption">Kapacita IÚ při střední době ukrytí (2 až 6 hod.)</span>
          </div>
          <div class="capacity-summary__value">{{ visibleCapacityTotals.total_n_ks }}</div>
        </div>
        <div class="capacity-summary__item">
          <div class="capacity-summary__label-row">
            <span class="capacity-summary__abbr">N_KD</span>
            <span class="capacity-summary__caption">Kapacita IÚ při dlouhodobém ukrytí (více než 6 hod.)</span>
          </div>
          <div class="capacity-summary__value">{{ visibleCapacityTotals.total_n_kd }}</div>
        </div>
      </div>
    </v-card-text>
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

import api from '@/services/api';
import { useSearchStore } from '@/stores/searchStore';


export default {
  name: 'MainMenu',
  data() {
    return {
      tab: 'option-1',
      isExporting: false,
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
      return useSearchStore().filteredBuildings
    },
        /**
     * Vrací seznam cílů ze store.
     * Pokud data nejsou načtena, vrací pole s prázdným objektem.
     * @type {Array<Object>}
     */
    targetItems() {
      return useSearchStore().filteredTargets
    },
    visibleCapacityTotals() {
      return useSearchStore().visibleCapacityTotals
    }
  },
  methods: {
    async downloadExport() {
      this.isExporting = true
      try {
        const response = await api.exportBuildingsWorkbook({
          building_ids: useSearchStore().filteredBuildingIds,
        })
        const blobUrl = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        const disposition = response.headers?.['content-disposition'] || ''
        const filenameMatch = disposition.match(/filename="?([^"]+)"?/i)

        link.href = blobUrl
        link.download = filenameMatch?.[1] || 'ikryty-export.xlsx'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(blobUrl)
      } catch (error) {
        console.error('Workbook export failed', error)
      } finally {
        this.isExporting = false
      }
    }
  }
}
</script>

<style scoped>
.capacity-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.capacity-summary__item {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 10px;
  min-width: 0;
  padding: 12px 14px;
  border: 1px solid rgba(25, 118, 210, 0.18);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(25, 118, 210, 0.08) 0%, rgba(25, 118, 210, 0.02) 100%);
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

.capacity-summary__label-row {
  display: flex;
  gap: 6px;
  align-items: baseline;
  flex-wrap: wrap;
}

.capacity-summary__abbr {
  font-weight: 700;
  color: rgb(13, 71, 161);
  letter-spacing: 0.04em;
}

.capacity-summary__caption {
  color: rgba(15, 23, 42, 0.72);
  font-size: 0.8rem;
  line-height: 1.25;
}

.capacity-summary__value {
  justify-self: end;
  font-size: 1.15rem;
  line-height: 1;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: rgba(15, 23, 42, 0.82);
}
</style>
