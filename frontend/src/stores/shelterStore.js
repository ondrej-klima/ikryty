/**
 * @file shelterStore.js
 * @brief Pinia store pro správu úkrytů (budov) a souvisejících číselníků.
 * 
 * @description
 * Tento store slouží k načítání, vytváření, aktualizaci a mazání záznamů o budovách/úkrytech.
 * Zároveň zajišťuje transformaci dat do formátu GeoJSON pro zobrazení na mapě.
 * Obsahuje také metody pro načítání číselníků (typy budov, materiály), které se ale zdají být
 * součástí starší logiky aplikace.
 * 
 * Komunikuje s API a pro každé volání si explicitně vyžádá Keycloak token.
 */

import axios from "axios";
import { defineStore } from "pinia"
import { getToken } from '@josempgon/vue-keycloak'
//import api from '@/services/api';

// Assume 'this.$keycloak' is available in your component
// const accessToken = this.$keycloak.token;

export const useShelterStore = defineStore('shelter', {
    state: () => ({
        shelters: null,
        buildingTypes: null,
        buildingSubTypes: null,
        materialTypes: null,
        materialSubTypes: null
    }),
    actions: {
        /**
         * Načte seznam všech budov (přehled) ze serveru.
         * Používá endpoint `/buildings_summary` (dříve `/user_shelters`).
         * Nastaví `state.shelters`.
         * 
         * @public
         * @action getUserShelters
         * @returns {Promise<void>}
         */
        async getUserShelters() {
            const token = await getToken()
            await axios.get('/buildings_summary', {
            //await axios.get('/user_shelters', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if (response.status == 200) {
                        this.$state.shelters = response.data
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        },
        async createShelter(shelter){
            const token = await getToken()
            await axios.post('/create_shelter', shelter, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserShelters()
        },
        async updateShelter(shelter, shelter_id){
            const token = await getToken()
            await axios.patch(`/shelter/${shelter_id}`, shelter, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserShelters()
        },
        async deleteShelter(shelter_id){
            const token = await getToken()
            await axios.delete(`/shelter/${shelter_id}`, { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              })
            await this.getUserShelters()
        },
        async initBuildingProperties(){
            await this.getBuildingTypes()
            await this.getBuildingSubTypes()
            await this.getMaterialTypes()
            await this.getMaterialSubTypes()
        },
        async getBuildingTypes(){
            const token = await getToken()
            await axios.get('/buildingtypes', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if(response.status == 200) {
                        this.$state.buildingTypes = [{id:null, caption:null}].concat(response.data)
                        //console.log(this.$state.buildingTypes)
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        },
        async getBuildingSubTypes(){
            const token = await getToken()
            await axios.get('/buildingsubtypes', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if(response.status == 200) {
                        this.$state.buildingSubTypes = [{id:null, caption:null}].concat(response.data)
                        //console.log(this.$state.buildingSubTypes)
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        },
        async getMaterialTypes(){
            const token = await getToken()
            await axios.get('/materialtypes', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if(response.status == 200) {
                        this.$state.materialTypes = [{id:null, caption:null}].concat(response.data)
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        },
        async getMaterialSubTypes(){
            const token = await getToken()
            await axios.get('/materialsubtypes', { // URL of your Python backend
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              }).then(async (response) => {
                    if(response.status == 200) {
                        this.$state.materialSubTypes = [{id:null, caption:null}].concat(response.data)
                    }
                }
            ).catch(async (error) => {
                //console.log(error.toJSON())
                console.log(error)
            })
        }
    },
    getters: {
        stateShelters: state => state.shelters,
        buildingType: state => {
            let result = [{id:null, caption:null}] //new Array()
            if(state.buildingTypes) {
                state.buildingTypes.forEach((buildingType) => {
                    result.push({
                        'label': buildingType.caption,
                        'id': buildingType.id,
                    })
                })
                //return result
            }
            //return [{null: null}]
            return result
        },
        /**
         * Převede seznam budov/úkrytů do formátu GeoJSON.
         * Tento formát je vyžadován mapovou komponentou (Leaflet).
         * 
         * Mapování vlastností:
         * - `name_address` -> `name`
         * - `user_id` -> `user`
         * - `max_s_c` -> `SC` (Skóre pro barvení markerů)
         * - `gps_long`, `gps_lat` -> Geometry coordinates
         * 
         * @param {Object} state
         * @returns {Object} GeoJSON FeatureCollection
         */
        sheltersGeoJSON: state => {
            let geojson = {
                type: "FeatureCollection",
                features: new Array()
            }
            if(state.shelters) {
                state.shelters.forEach((shelter) => {
                    geojson.features.push({
                        type: "Feature",
                        properties: {
                            "@id": shelter.id,
                            name: shelter.name_address,
                            address: shelter.name_address,
                            user: shelter.user_id, 
                            SC: shelter.max_s_c,
                            //SC: 0
                        },
                        geometry: {
                            type: "Point",
                            coordinates: [
                                shelter.gps_long,
                                shelter.gps_lat
                                /*
                                shelter.y,
                                shelter.x
                                */
                            ]
                        },
                        "id": shelter.id
                    })
                })
            }
            /*
            if(state.shelters) {
                state.shelters.forEach((shelter) => {
                    geojson.features.push({
                        type: "Feature",
                        properties: {
                            "@id": shelter.id,
                            name: shelter.name,
                            address: shelter.address,
                            user: shelter.user, 
                            SC: shelter.SC,
                        },
                        geometry: {
                            type: "Point",
                            coordinates: [
                                shelter.y,
                                shelter.x
                            ]
                        },
                        "id": shelter.id
                    })
                })
            }
            */
            return geojson
        }
    }
})