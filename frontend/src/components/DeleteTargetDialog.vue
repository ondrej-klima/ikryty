<template>
  <div class="text-center">
    <v-dialog
        ref="dialog"
        v-model="dialog"
      width="560"
        content-class="draggable-delete-target-dialog"
    >
      <v-card>
        <v-toolbar color="primary">
          <v-toolbar-title
            class="draggable-dialog__handle"
            @pointerdown.stop="startDrag"
          >
            {{ $t('target.removeTarget') }}
          </v-toolbar-title>
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
      dragPointerId: null,
      dragOffset: {
        x: 0,
        y: 0,
      },
      id: null,
      name: null
    }
  },
  watch: {
    dialog(isOpen) {
      if (isOpen) {
        this.$nextTick(() => {
          window.requestAnimationFrame(() => {
            this.resetDialogPosition()
          })
        })
        return
      }

      this.stopDrag()
    }
  },
  methods: {
    getDialogSurface() {
      return document.querySelector('.draggable-delete-target-dialog')
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

:deep(.draggable-delete-target-dialog) {
  position: fixed;
  margin: 0;
  max-width: calc(100vw - 32px);
  max-height: calc(100vh - 32px);
  overflow: auto;
  transform: none;
}
</style>
