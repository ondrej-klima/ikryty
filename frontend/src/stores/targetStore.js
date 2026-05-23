/**
 * @file targetStore.js
 * @brief Pinia store pro správu Cílů (Targets).
 * 
 * @description
 * Tento store spravuje data o "Cílech útoku" (Targets), které slouží jako referenční body
 * pro výpočet ohroženosti úkrytů (vzdálenost od cíle v Kroku 5).
 * 
 * Funkcionalita:
 * - CRUD operace (Create, Read, Update, Delete) pro cíle.
 * - Výpočet minimální vzdálenosti bodu od nejbližšího cíle.
 * - Transformace dat do GeoJSON formátu pro zobrazení na mapě.
 */

import axios from "axios";
import { defineStore } from "pinia"
import { getToken } from '@josempgon/vue-keycloak'



// Assume 'this.$keycloak' is available in your component
// const accessToken = this.$keycloak.token;

export const useTargetStore = defineStore('target', {
    state: () => ({
        /** Seznam načtených cílů. */
        targets: null,
                /** 
         * Výsledek výpočtu minimální vzdálenosti. 
         * (Dynamicky přidáno akcí getMinDistance).
         * @type {Object|null} 
         */
        // minDistance: null, 
    }),
    actions: {
        /**
         * Načte seznam cílů pro aktuálního uživatele.
         * Volá endpoint `/user_targets`.
         * 
         * @public
         * @action getUserTargets
         * @returns {Promise<void>}
         */
        async getUserTargets() {
            const token = await getToken()
            await axios.get('/user_targets', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if (response.status == 200) {
                        this.$state.targets = response.data
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        },

        /**
         * Vytvoří nový cíl.
         * Volá endpoint `/create_target` a následně obnoví seznam cílů.
         * 
         * @param {Object} target - Data cíle (name, address, x, y, description).
         * @public
         * @action createTarget
         * @returns {Promise<void>}
         */
        async createTarget(target){
            const token = await getToken()
            await axios.post('/create_target', target, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserTargets()
        },

        /**
         * Aktualizuje existující cíl.
         * Volá endpoint `/target/{id}`.
         * 
         * @param {Object} target - Upravená data cíle.
         * @param {number|string} target_id - ID cíle.
         * @public
         * @action updateTarget
         * @returns {Promise<void>}
         */
        async updateTarget(target, target_id){
            const token = await getToken()
            await axios.patch(`/target/${target_id}`, target, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserTargets()
        },

        /**
         * Smaže cíl.
         * Volá endpoint `/target/{id}`.
         * 
         * @param {number|string} target_id - ID cíle.
         * @public
         * @action deleteTarget
         * @returns {Promise<void>}
         */
        async deleteTarget(target_id){
            const token = await getToken()
            await axios.delete(`/target/${target_id}`, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserTargets()
        },

        /**
         * Získá minimální vzdálenost daného bodu (lat, lon) k nejbližšímu cíli.
         * Výsledek ukládá do `state.minDistance`.
         * Používá se v Kroku 5 (Threat Assessment).
         * 
         * @param {number} lat - Zeměpisná šířka bodu (úkrytu).
         * @param {number} lon - Zeměpisná délka bodu (úkrytu).
         * @public
         * @action getMinDistance
         * @returns {Promise<void>}
         */
        async getMinDistance(lat, lon) {
            const token = await getToken()
            await axios.get(`/min_distance/${lat}/${lon}`, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if (response.status == 200) {
                        this.$state.minDistance = response.data
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        }
    },
    getters: {
         /** Vrací surový seznam cílů. */
        stateTargets: state => state.targets,

        /**
         * Převede seznam cílů do formátu GeoJSON pro zobrazení na mapě.
         * 
         * Mapování souřadnic:
         * - `target.y` -> Longitude (v souřadnicovém poli první)
         * - `target.x` -> Latitude (v souřadnicovém poli druhé)
         * 
         * @param {Object} state
         * @returns {Object} GeoJSON FeatureCollection
         */
        targetsGeoJSON: state => {
            let geojson = {
                type: "FeatureCollection",
                features: new Array()
            }
            if(state.targets) {
                state.targets.forEach((target) => {
                    geojson.features.push({
                        type: "Feature",
                        properties: {
                            "@id": target.id,
                            name: target.name,
                            user: target.user,
                            address: target.address 
                        },
                        geometry: {
                            type: "Point",
                            coordinates: [
                                target.y,
                                target.x
                            ]
                        },
                        "id": target.id
                    })
                })
            }
            return geojson
        }
    }
})