<template>
	<v-menu
			v-model="menu"
			offset-y>
		<template v-slot:activator="{ on: menu }">

			<v-tooltip bottom>
				<template v-slot:activator="{ on: tooltip }">
					<v-btn
							icon
							v-on="{ ...tooltip, ...menu }"
					>
						<img
								:src="currentLanguageIcon"
								v-if="currentLanguageIcon"
						/>
						<v-icon v-else>mdi-earth</v-icon>
					</v-btn>
				</template>
				<span>Switch Language</span>
			</v-tooltip>
		</template>

		<v-card min-width="300">
			<v-list>
				<v-list-item
						v-for="language in languages"
						:key="language.id"
						@click="changeLanguage(language.id)"
				>
					<template v-slot:prepend>
						<v-avatar :rounded="0">
							tile
							size="24"

						<v-img :src="language.flagSrc"></v-img>
						</v-avatar>
					</template>
					<v-list-item-title>{{ language.title }}</v-list-item-title>
				</v-list-item>
			</v-list>
		</v-card>
	</v-menu>
</template>

<script>
/**
 * @file LanguageSwitcher.vue
 * @brief Komponenta pro přepínání jazyka aplikace.
 * 
 * @description
 * Tato komponenta zobrazuje tlačítko (s vlajkou aktuálního jazyka nebo ikonou země).
 * Po kliknutí zobrazí rozbalovací menu (`v-menu`) se seznamem dostupných jazyků.
 * 
 * Je navržena pro použití s i18n frameworkem (např. Nuxt i18n), jelikož
 * spoléhá na globální metodu `switchLocalePath` pro změnu routy.
 * 
 * @component
 * @example
 * <language-switcher 
 *    :languages="[{id: 'cs', title: 'Čeština', flagSrc: '/flags/cz.png'}]" 
 *    :current-language="'cs'"
 *    @languageChanged="onLanguageChanged"
 * />
 */

/**
 * @event languageChanged
 * @brief Vyvoláno po kliknutí na nový jazyk.
 * @param {string} id - ID (kód) vybraného jazyka.
 */

//https://github.com/lupas/vuetify-i18n-language-switcher-nuxt/tree/master
export default {
	name: "LanguageSwitcher",
	props: {
        /**
         * Seznam dostupných jazyků.
         * Očekává pole objektů ve formátu: `{ id: string, title: string, flagSrc: string }`.
         */
		languages: {
			type: Array,
			required: true
		},
    /**
         * ID aktuálně vybraného jazyka (např. 'cs', 'en').
         */
		currentLanguage: {
			type: String,
			required: false,
			default: null
		}
	},
	data() {
		return {
			/** Řídí viditelnost rozbalovacího menu. */
			menu: false,
		}
	},
	computed: {
    /**
         * Vrací URL obrázku vlajky pro aktuálně zvolený jazyk.
         * Vyhledá odpovídající objekt v poli `languages` podle `currentLanguage`.
         * @type {string|null}
         */
		currentLanguageIcon() {
			if (!this.currentLanguage || !this.currentLanguage) {
				return null;
			}
			return this.languages.filter(x => x.id === this.currentLanguage)[0]
					.flagSrc;
		}
	},
	methods: {
		/**
         * Změní jazyk aplikace.
         * Přesměruje router na cestu odpovídající vybranému locale (pomocí `switchLocalePath`)
         * a emituje událost o změně.
         * 
         * @param {string} id - ID jazyka, na který se má přepnout.
         * @public
         * @method changeLanguage
         * @return {void}
         */
		changeLanguage(id) {
			this.$router.push(this.switchLocalePath(id));
			this.$emit("languageChanged", id);
		}
	}
};
</script>

<style lang="scss" scoped></style>