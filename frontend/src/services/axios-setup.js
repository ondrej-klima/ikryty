/**
 * @file axiosSetup.js
 * @brief Konfigurace a inicializace Axios interceptorů.
 * 
 * @description
 * Tento modul obsahuje funkci pro nastavení globálních parametrů knihovny Axios
 * a pro registraci interceptorů (zachytávačů požadavků).
 * 
 * Hlavním účelem je integrace s Keycloak autentizací:
 * - Nastavuje `baseURL` API.
 * - Před každým požadavkem kontroluje platnost Keycloak tokenu.
 * - Pokud je token expirovaný, pokusí se jej automaticky obnovit (`updateToken`).
 * - Přidává `Authorization` hlavičku s Bearer tokenem.
 * 
 * Funkce by měla být volána z `main.js` až ve chvíli, kdy je Keycloak plně inicializován.
 */

import axios from 'axios';

// This is now a function that we will call from main.js
// after Keycloak is ready.
/**
 * Nastaví globální interceptory pro Axios, které zajišťují autentizaci.
 * 
 * @param {Object} keycloak - Inicializovaná instance Keycloaku.
 * @public
 * @function setupAxiosInterceptors
 * @return {void}
 * 
 * @example
 * // v main.js
 * keycloak.init(...).then((auth) => {
 *   if (auth) {
 *     setupAxiosInterceptors(keycloak);
 *     app.mount('#app');
 *   }
 * });
 */
export function setupAxiosInterceptors(keycloak) {
  // --- Configure Global Axios Defaults ---
  axios.defaults.withCredentials = true;
  //axios.defaults.baseURL = 'http://localhost:8000';
  //axios.defaults.baseURL = 'https://civildefense.fit.vutbr.cz:8000';
  axios.defaults.baseURL = 'https://api.civildefense.fit.vutbr.cz';

  // --- Add the Global Request Interceptor ---
  axios.interceptors.request.use(
    async (config) => {
      // We no longer need to check if keycloak exists, because this function
      // is only called AFTER it's initialized.
      if (keycloak.authenticated) {
        try {
          //console.log("Updating token")
          // Use the keycloak object passed as an argument
          await keycloak.updateToken(5);
          config.headers.Authorization = `Bearer ${keycloak.token}`;
        } catch (error) {
          //console.error('Could not refresh token:', error);
          keycloak.logout();
          return Promise.reject(error);
        }
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
}
