/**
 * @file main.js
 * @brief Hlavní vstupní bod Vue aplikace.
 * 
 * @description
 * Tento soubor inicializuje celou aplikaci. Jeho hlavní úkoly jsou:
 * 1. **Vytvoření Vue aplikace:** `createApp(App)`.
 * 2. **Integrace pluginů:**
 *    - **Vuetify:** UI framework (konfigurace ikon a komponent).
 *    - **Pinia:** State management.
 *    - **Vue I18n:** Lokalizace (CS, EN, JA).
 *    - **Vue Katex:** Renderování matematických rovnic.
 *    - **Vue Keycloak:** Autentizace uživatele.
 * 3. **Konfigurace Axios:** Volání `setupAxiosInterceptors` pro propojení Axiosu s Keycloak tokenem.
 * 4. **Spuštění aplikace:** Po úspěšné inicializaci Keycloaku se aplikace připojí do DOM (`mount`).
 */


import { createApp } from 'vue'
//import { VueRecaptchaPlugin } from 'vue-recaptcha';
import App from './App.vue'
import { vueKeycloak } from '@josempgon/vue-keycloak'
import router from '@/routes/index'
//mport axios from "axios";

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { createPinia } from "pinia";
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// https://stackoverflow.com/questions/57053728/vuetify-icon-not-showing
import { fa } from "vuetify/iconsets/fa";
import { aliases, mdi } from "vuetify/lib/iconsets/mdi";
// make sure to also import the coresponding css
import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader
import "@fortawesome/fontawesome-free/css/all.css"; // Ensure your project is capable of handling css files

// --- IMPORT THE AXIOS SETUP FILE FOR ITS SIDE-EFFECT ---
import './services/axios-setup.js';

// --- ADD THESE LINES FOR KATEX ---
import VueKatex from '@hsorby/vue3-katex'
import 'katex/dist/katex.min.css' // This is the stylesheet for the math
// --- END OF ADDED LINES ---


const vuetify = createVuetify({
    icons: {
        defaultSet: "mdi",
        aliases,
        sets: {
            mdi,
            fa,
        },
    },
    components,
    directives,
})
const pinia = createPinia()
const app = createApp(App)

//axios.defaults.withCredentials = true;
/*
axios.defaults.baseURL = process.env.NODE_ENV == 'development' ?
    'http://localhost:8000/' :
    'https://civildefense.fit.vutbr.cz:8000'
*/
//axios.defaults.baseURL = 'https://civildefense.fit.vutbr.cz:8000'
//axios.defaults.baseURL = 'http://localhost:8000'

app.use(vuetify)
app.use(VueKatex) // Register the KaTeX plugin
app.use(pinia)

import * as VueI18n from 'vue-i18n'

import ja from "./locales/ja.json";
import en from "./locales/en.json";
import cs from "./locales/cs.json";
import { setupAxiosInterceptors } from './services/axios-setup.js'

const i18n = VueI18n.createI18n({
  locale: 'cs', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages: { cs, en, ja },
})

app.use(i18n)

/**
 * Asynchronní inicializace aplikace.
 * Klíčovým krokem je inicializace Keycloaku. Router a mount aplikace se provede
 * až po úspěšném přihlášení/ověření uživatele.
 * 
 * @param {Object} app - Instance Vue aplikace.
 * @async
 * @function initApp
 * @return {Promise<void>}
 */
const initApp = async (app) => {
    //const app = createApp(App)
  
    // Set up keycloak plugin before the router init
    await vueKeycloak.install(app, {
     init: { 
        onLoad: 'login-required',
        //onLoad: 'check-sso',
        //redirectUrl: 'http://localhost:8080/',
        redirectUrl: 'https://civildefense.fit.vutbr.cz/',
            // Let's add a long timeout to be safe

        flow: 'standard',
            // --- ADD THESE DEBUGGING HOOKS ---
        onError: (errorData) => {
            console.error('KEYCLOAK INIT ERROR:', errorData);
            // This will show you errors like network issues or invalid server responses.
        },
        onAuthError: (errorData) => {
            console.error('KEYCLOAK AUTH ERROR:', errorData);
            // This will show you specific authentication errors, like "invalid_code".
        }
      },
      config: {
        url: 'https://civildefense.fit.vutbr.cz:8443/',
        clientId: 'account',
        realm: 'ikryty'
      },
    })
  
    setupAxiosInterceptors(app.config.globalProperties.$keycloak);
    setInterval(() => {
        const keycloak = app.config.globalProperties.$keycloak;
        //console.log('interval:keycloak', keycloak);
        if (keycloak) {
          keycloak.updateToken(70).then((refreshed) => {
            //console.log('interval:refreshed', refreshed);
            if (refreshed) {
                //console.log(`Token refreshed ${refreshed}`);
            } /*else {
              const expiry = keycloak.tokenParsed?.exp || 0;
              const timeSkew = keycloak.timeSkew || 0;
              const seconds = Math.round(expiry + timeSkew - new Date().getTime() / 1000);
              console.log(`Token not refreshed, valid for ${seconds} seconds`);
            } */
          }).catch(() => {
            //console.log('Failed to refresh token');
          });
        }
      }, 30000);

    app.use(router)
    app.mount('#app')

  }
  
initApp(app)