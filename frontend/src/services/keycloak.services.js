/**
 * @file keycloakState.js
 * @brief Globální reference na instanci Keycloaku.
 * 
 * @description
 * Tento modul exportuje reaktivní referenci (`shallowRef`), která drží instanci Keycloaku.
 * 
 * Důvod použití `shallowRef`:
 * Objekt Keycloak je komplexní knihovna s mnoha vnitřními metodami a cyklickými referencemi.
 * Není žádoucí, aby Vue sledovalo změny hluboko uvnitř tohoto objektu (deep reactivity),
 * protože to je výkonnostně náročné a zbytečné. Zajímá nás pouze přítomnost instance jako celku.
 * 
 * Instance je inicializována v `main.js` a následně zpřístupněna přes tento export
 * pro použití v composables nebo stores (např. Pinia), kde není přístup k `this.$keycloak`.
 */

/**
 * Globálně dostupná, mělce reaktivní reference na instanci Keycloaku.
 * Počáteční hodnota je `null`. Naplní se po úspěšné inicializaci v `main.js`.
 * 
 * @type {ShallowRef<Keycloak|null>}
 */

import { shallowRef } from 'vue';

// We use shallowRef because the keycloak instance is a large object with many
// internal properties and methods that don't need to be deeply reactive.
// We only care about reacting when the entire instance itself is assigned or replaced.
//
// This creates a single, globally accessible object that will start as `null`
// and will be updated in `main.js` once Keycloak is ready.
export const keycloakInstance = shallowRef(null);
