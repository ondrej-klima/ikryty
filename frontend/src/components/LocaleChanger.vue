<script setup lang="ts"/>

<template>
  <div class="locale-changer">
    <select v-model="$i18n.locale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang.code">
        {{ lang.text }}
				<v-img src="cz.png" />
      </option>
    </select>
  </div>
</template>

<script>
/**
 * @file LocaleChanger.vue
 * @brief Jednoduchý přepínač jazyka.
 * 
 * @description
 * Tato komponenta poskytuje základní rozhraní pro změnu lokalizace aplikace.
 * Využívá nativní HTML element `<select>` pro výběr jazyka a přímo modifikuje
 * globální proměnnou `$i18n.locale`.
 * 
 * Komponenta je pozicována fixně (vlevo nahoře) pomocí CSS.
 * 
 * *Poznámka: Tento soubor se zdá být alternativou nebo starší verzí k `LanguageSwitcher.vue`,
 * který používá Vuetify komponenty.*
 * 
 * @component
 * @example
 * <locale-changer />
 */
export default {
  name: "locale-changer",
  data() {
    return {
      /**
       * Seznam dostupných jazyků pro výběr.
       * Obsahuje kód jazyka (pro i18n) a zobrazovaný text.
       * @type {Array<{code: string, text: string}>}
       */
      langs: [
        { code: "cs", text: "česky" },
        { code: "en", text: "English" },
        // { code: "ja", text: "日本" },
      ],
    };
  },
};
</script>

<style>
.locale-changer {
  position: fixed;
  z-index: 9999;
  top: 15px;
  left: 55px;
	background: white;
	border: solid 2px lightgray;
	text-align: center;
}
</style>
