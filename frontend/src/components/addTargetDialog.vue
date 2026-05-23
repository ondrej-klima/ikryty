<template>
  <div class="text-center">
    <v-dialog
      ref="dialog"
      v-model="show"
      width="1024"
      persistent
      content-class="draggable-target-dialog"
    >
      <v-form
        fast-fail
        @submit.prevent="submit"
      >
      <v-card>
        <v-toolbar color="primary">
          <v-toolbar-title
            class="draggable-dialog__handle"
            @pointerdown.stop="startDrag"
          >
            {{ $t('target.title') }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
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
      dragPointerId: null,
      dragOffset: {
        x: 0,
        y: 0,
      },
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
  watch: {
    show(isOpen) {
      if (isOpen) {
        this.$nextTick(() => {
          window.requestAnimationFrame(() => {
            this.resetDialogPosition()
          })
        })
        return
      }

      this.stopDrag()
    },
  },
  methods: {
    getDialogSurface() {
      return document.querySelector('.draggable-target-dialog')
    },
    startDrag(event) {
      const surface = this.getDialogSurface()

      if (!surface) {
        return
      }

      const rect = surface.getBoundingClientRect()
      this.dragPointerId = event.pointerId
      this.dragOffset.x = event.clientX - rect.left
      this.dragOffset.y = event.clientY - rect.top

      window.addEventListener('pointermove', this.onDrag)
      window.addEventListener('pointerup', this.stopDrag)
      window.addEventListener('pointercancel', this.stopDrag)

      event.currentTarget?.setPointerCapture?.(event.pointerId)
    },
    onDrag(event) {
      if (this.dragPointerId !== event.pointerId) {
        return
      }

      const surface = this.getDialogSurface()

      if (!surface) {
        return
      }

      const rect = surface.getBoundingClientRect()
      const handle = this.getHandleMetrics(surface, rect)
      const nextLeft = event.clientX - this.dragOffset.x
      const nextTop = event.clientY - this.dragOffset.y

      this.setSurfacePosition(
        surface,
        this.clampToHandle(nextLeft, window.innerWidth, handle.left, handle.width),
        this.clampToHandle(nextTop, window.innerHeight, handle.top, handle.height)
      )
    },
    stopDrag() {
      this.dragPointerId = null
      window.removeEventListener('pointermove', this.onDrag)
      window.removeEventListener('pointerup', this.stopDrag)
      window.removeEventListener('pointercancel', this.stopDrag)
    },
    resetDialogPosition() {
      const surface = this.getDialogSurface()

      if (!surface) {
        return
      }

      const rect = surface.getBoundingClientRect()
      const handle = this.getHandleMetrics(surface, rect)
      this.setSurfacePosition(
        surface,
        this.clampToHandle((window.innerWidth - rect.width) / 2, window.innerWidth, handle.left, handle.width),
        this.clampToHandle((window.innerHeight - rect.height) / 2, window.innerHeight, handle.top, handle.height)
      )
    },
    getHandleMetrics(surface, surfaceRect) {
      const handle = surface.querySelector('.draggable-dialog__handle')

      if (!handle) {
        return {
          left: 0,
          top: 0,
          width: Math.min(surfaceRect.width, 160),
          height: 64,
        }
      }

      const handleRect = handle.getBoundingClientRect()

      return {
        left: handleRect.left - surfaceRect.left,
        top: handleRect.top - surfaceRect.top,
        width: handleRect.width,
        height: handleRect.height,
      }
    },
    setSurfacePosition(surface, left, top) {
      surface.style.left = `${left}px`
      surface.style.top = `${top}px`
      surface.style.right = 'auto'
      surface.style.bottom = 'auto'
      surface.style.margin = '0'
      surface.style.transform = 'none'
    },
    clampToHandle(nextValue, viewportSize, handleOffset, handleSize) {
      const visibleHandle = Math.min(handleSize, Math.max(handleSize * 0.35, 48))
      const min = visibleHandle - handleOffset - handleSize
      const max = viewportSize - handleOffset - visibleHandle

      return Math.min(Math.max(nextValue, min), max)
    },
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

<style scoped>
.draggable-dialog__handle {
  background-color: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  cursor: move;
  display: inline-flex;
  max-width: 50%;
  min-width: min(50%, 320px);
  padding: 8px 14px;
  user-select: none;
  touch-action: none;
}

:deep(.draggable-target-dialog) {
  position: fixed;
  margin: 0;
  max-width: min(1024px, calc(100vw - 32px));
  max-height: calc(100vh - 32px);
  overflow: auto;
  transform: none;
}
</style>
