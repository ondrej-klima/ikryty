<template>
   <LocaleChanger/>
	<!-- LanguageSwitcher :languages="languages" /-->
   <router-view />
</template>

<script>

import LocaleChanger from "@/components/LocaleChanger.vue"
//import LanguageSwitcher from "@/components/LanguageSwitcher.vue";


export default {
	name: 'App',
	components: {
		LocaleChanger,
		//LanguageSwitcher
	},

	data() {
		return {
			languages: [
				{
					id: 'en',
					title: 'English',
					flagSrc: 'https://cdn.vuetifyjs.com/images/flags/us.png'
				},
				{
					id: 'kr',
					title: 'Korean',
					flagSrc: 'https://cdn.vuetifyjs.com/images/flags/kr.png'
				}
			]
		}
	},
	created () {
            document.title = "Evidence improvizovaného ukrytí";
        }
}

</script>

<style>
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	height: 100%;
}
html, body {
	height: 100%;
	width: 100%;
	margin: 0;
}
</style>
