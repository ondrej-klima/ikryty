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
        <v-tab value="option-3">
          <v-icon start>
            mdi-information-outline
          </v-icon>
          {{ $t("menu.buildingDetails") }}
        </v-tab>
        <v-tab value="option-4">
          <v-icon start>
            mdi-crosshairs-gps
          </v-icon>
          {{ $t("menu.targetDetails") }}
        </v-tab>
      </v-tabs>
      <v-window v-model="tab">
        <v-window-item value="option-1">
          <v-card flat>
            <v-card-text>
              <v-data-table
                :items="items"
                :headers="shelterHeaders"
                :row-props="getShelterRowProps"
              ></v-data-table>
            </v-card-text>
          </v-card>
        </v-window-item>
        <v-window-item value="option-2">
          <v-card flat>
            <v-card-text>
              <v-data-table
                :items="targetItems"
                :headers="targetHeaders"
                :row-props="getTargetRowProps"
              ></v-data-table>
            </v-card-text>
          </v-card>
        </v-window-item>
        <v-window-item value="option-3">
          <v-card flat>
            <v-card-text>
              <div v-if="selectedBuilding" class="building-details">
                <div class="building-details__title">{{ $t("menu.selectedBuilding") }}</div>
                <table class="building-details__table">
                  <tbody>
                    <tr v-for="entry in selectedBuildingEntries" :key="entry.key">
                      <th scope="row">{{ entry.label }}</th>
                      <td>{{ entry.value }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="building-details__empty">
                {{ $t("menu.noBuildingSelected") }}
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>
        <v-window-item value="option-4">
          <v-card flat>
            <v-card-text>
              <div v-if="selectedTarget" class="building-details">
                <div class="building-details__title">{{ $t("menu.selectedTarget") }}</div>
                <table class="building-details__table">
                  <tbody>
                    <tr v-for="entry in selectedTargetEntries" :key="entry.key">
                      <th scope="row">{{ entry.label }}</th>
                      <td>{{ entry.value }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="building-details__empty">
                {{ $t("menu.noTargetSelected") }}
              </div>
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
    selectedBuildingId() {
      return useSearchStore().selectedBuildingId
    },
    selectedTargetId() {
      return useSearchStore().selectedTargetId
    },
    selectedBuilding() {
      return useSearchStore().selectedBuilding
    },
    selectedTarget() {
      return useSearchStore().selectedTarget
    },
    selectedBuildingEntries() {
      if (!this.selectedBuilding) {
        return []
      }

      const fieldLabels = {
        id: 'ID',
        building_code: this.$t('step1.rs1'),
        user_id: this.$t('menu.user'),
        name_address: this.$t('step1.rs2'),
        max_s_c: this.$t('menu.score'),
        total_n_k: this.$t('menu.capacityShort'),
        total_n_ks: this.$t('menu.capacityMedium'),
        total_n_kd: this.$t('menu.capacityLong'),
        gps_lat: this.$t('step1.rs3_lat'),
        gps_long: this.$t('step1.rs3_long')
      }

      return Object.entries(this.selectedBuilding)
        .filter(([, value]) => value !== null && value !== undefined && value !== '')
        .map(([key, value]) => ({
          key,
          label: fieldLabels[key] || key,
          value: this.formatBuildingEntryValue(key, value)
        }))
    },
    selectedTargetEntries() {
      if (!this.selectedTarget) {
        return []
      }

      const fieldLabels = {
        id: 'ID',
        user: this.$t('menu.user'),
        name: this.$t('target.targetName'),
        address: this.$t('target.targetAddress'),
        x: this.$t('target.latitude'),
        y: this.$t('target.longitude'),
        description: this.$t('target.targetDescription')
      }

      return Object.entries(this.selectedTarget)
        .filter(([, value]) => value !== null && value !== undefined && value !== '')
        .map(([key, value]) => ({
          key,
          label: fieldLabels[key] || key,
          value: this.formatTargetEntryValue(key, value)
        }))
    },
    visibleCapacityTotals() {
      return useSearchStore().visibleCapacityTotals
    }
  },
  watch: {
    selectedBuilding(value) {
      if (value) {
        this.tab = 'option-3'
      }
    },
    selectedTarget(value) {
      if (value) {
        this.tab = 'option-4'
      }
    }
  },
  methods: {
    getShelterRowProps({ item }) {
      const building = item?.raw || item
      const isSelected = building?.id === this.selectedBuildingId

      return {
        class: isSelected ? 'main-menu__row--selected' : '',
        onClick: () => {
          if (building?.id != null) {
            useSearchStore().setSelectedBuildingId(building.id)
            this.tab = 'option-3'
          }
        }
      }
    },
    getTargetRowProps({ item }) {
      const target = item?.raw || item
      const isSelected = target?.id === this.selectedTargetId

      return {
        class: isSelected ? 'main-menu__row--selected' : '',
        onClick: () => {
          if (target?.id != null) {
            useSearchStore().setSelectedTargetId(target.id)
            this.tab = 'option-4'
          }
        }
      }
    },
    formatBuildingEntryValue(key, value) {
      if (['gps_lat', 'gps_long'].includes(key)) {
        return Number(value).toFixed(6)
      }

      if (key === 'max_s_c') {
        return Number(value).toFixed(2)
      }

      return value
    },
    formatTargetEntryValue(key, value) {
      if (['x', 'y'].includes(key)) {
        return Number(value).toFixed(6)
      }

      return value
    },
    async downloadExport() {
      this.isExporting = true
      try {
        const response = await api.exportBuildingsWorkbook({
          building_ids: useSearchStore().filteredBuildingIds,
          target_ids: useSearchStore().filteredTargetIds,
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

.building-details {
  display: grid;
  gap: 10px;
}

.building-details__title {
  font-size: 0.95rem;
  font-weight: 600;
}

.building-details__empty {
  padding: 20px;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.04);
  color: rgba(15, 23, 42, 0.72);
}

.building-details__table {
  width: 100%;
  border-collapse: collapse;
}

.building-details__table th,
.building-details__table td {
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
}

.building-details__table th {
  width: 36%;
  font-weight: 600;
  color: rgba(15, 23, 42, 0.76);
}

.building-details__table td {
  color: rgba(15, 23, 42, 0.88);
  word-break: break-word;
}

.v-data-table :deep(.main-menu__row--selected) {
  background: rgba(245, 124, 0, 0.12);
}

.v-data-table :deep(.main-menu__row--selected:hover) {
  background: rgba(245, 124, 0, 0.18);
}

@media (max-width: 960px) {
  .capacity-summary {
    grid-template-columns: 1fr;
  }

  .building-details__grid {
    grid-template-columns: 1fr;
  }

  .building-details__table th,
  .building-details__table td {
    display: block;
    width: 100%;
  }
}
</style>
