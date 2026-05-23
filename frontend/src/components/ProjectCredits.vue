<template>
  <div class="credits-logo">
    <a href="https://vut.cz/" target="_blank"><img src="../assets/vut.svg" alt="VUT"></a>
    <a href="https://unob.cz/" target="_blank"><img src="../assets/uo.svg" alt="UNOB"></a>
  </div>
</template>

<script>
/**
 * @file ProjectCredits.vue
 * @brief Komponenta zobrazující loga partnerů projektu.
 * 
 * @description
 * Jednoduchá prezentační komponenta, která zobrazuje loga institucí zapojených do vývoje projektu:
 * - Vysoké učení technické v Brně (VUT)
 * - Univerzita obrany (UNOB)
 * 
 * Loga fungují jako externí odkazy na webové stránky daných univerzit.
 * Komponenta je obvykle umístěna v pravém dolním rohu mapového rozhraní (uvnitř `L.control.mypanel`).
 * 
 * @component
 * @example
 * <project-credits />
 */

export default {
  name: 'ProjectCredits',
}
</script>

<style>
.credits-logo img {
  height: 80px;
}
</style>





