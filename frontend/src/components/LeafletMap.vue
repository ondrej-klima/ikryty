<template>
	<div class="map">
		<div ref="mapSearch" class="map-search">
			<v-text-field
				v-model="searchQuery"
				prepend-inner-icon="mdi-magnify"
				clearable
				density="compact"
				variant="solo"
				hide-details
				label="Filtrovat podle adresy"
			/>
		</div>
		<l-map ref="map" :zoom="zoom" :center="[49.2265592, 16.5957531]" :options="mapOptions" @ready="addControls">
			<l-control-layers position="topright"></l-control-layers>
			<l-tile-layer
				v-for="tileProvider in baseLayers"
				:key="tileProvider.name"
				:name="tileProvider.name"
				:visible="tileProvider.visible"
				:url="tileProvider.url"
				:attribution="tileProvider.attribution"
				:maxZoom="tileProvider.maxZoom"
				layer-type="base"
			></l-tile-layer>
			<l-wms-tile-layer
				v-for="layer in wmsBaseLayers"
				:key="layer.name"
				:url="layer.url"
				:layers="layer.layers"
				:visible="layer.visible"
				:name="layer.name"
				:transparent="false"
				layer-type="base"
				format="image/png"
				:maxZoom="layer.maxZoom"
			/>
			<l-wms-tile-layer
				v-for="layer in wmsOverlayLayers"
				:key="layer.name"
				:url="layer.url"
				:layers="layer.layers"
				:visible="layer.visible"
				:name="layer.name"
				:transparent="true"
				:opacity="layer.opacity"
				layer-type="overlay"
				format="image/png"
				:maxZoom="layer.maxZoom"
			/>
			<l-control-scale position="bottomleft" :imperial="false" :metric="true"></l-control-scale>
			<l-geo-json
				:geojson="filteredGeojson"
				:options="options"
			/>
			<l-geo-json
				:geojson="filteredTargetGeojson"
				:options="targetOptions"
			/>
			
		</l-map>
	</div>
  <div id="sidebar">
    <MainMenu></MainMenu>
  </div>
  <div id="avatar">
    <VuetifyAvatar></VuetifyAvatar>
  </div>
  <div id="credits">
    <ProjectCredits></ProjectCredits>
  </div>
  <add-shelter-dialog ref="addShelter" />
  <add-target-dialog ref="addTarget" />
  <delete-shelter-dialog ref="deleteShelterDialog" />
  <delete-target-dialog ref="deleteTargetDialog" />
  <div ref="tooltip" id="tooltip" style="display: none">
    {{ $t("shelter.shelter") }} {{tooltipData.id}}: {{tooltipData.title}}
  </div>
  <!-- <VueUnityComponent ref="virtualTour" /> -->
</template>

<script>
/**
 * @file MapComponent.vue
 * @brief Hlavní mapová komponenta aplikace.
 * 
 * @description
 * Tato komponenta tvoří jádro aplikace. Integruje mapový framework Leaflet a poskytuje
 * uživatelské rozhraní pro správu a vizualizaci úkrytů civilní ochrany a cílů útoku.
 * 
 * Klíčové funkce:
 * - **Zobrazení mapy:** Podpora WMS vrstev, přepínání podkladů (base layers) a překryvů (overlays).
 * - **Vizualizace dat:** Zobrazuje úkryty a cíle jako GeoJSON vrstvy s vlastními ikonami
 *   (barva ikony úkrytu indikuje jeho stav/skóre).
 * - **Interaktivita:**
 *   - Kontextové menu (pravé tlačítko) pro přidávání objektů.
 *   - Klikatelné markery s menu pro editaci/mazání.
 *   - Vyhledávání adres (Geosearch).
 *   - Lokalizace uživatele (LocateControl).
 * - **Správa dialogů:** Řídí otevírání modálních oken pro editaci (`addShelterDialog`, `addTargetDialog`)
 *   a mazání (`DeleteShelterDialog`, `DeleteTargetDialog`).
 * 
 * @component
 * @example
 * <map-component />
 */

import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControlScale, LWmsTileLayer } from "@vue-leaflet/vue-leaflet";

import 'leaflet-contextmenu';
import 'leaflet-contextmenu/dist/leaflet.contextmenu.min.css';

import * as L from 'leaflet'
import "leaflet-sidebar/src/L.Control.Sidebar.css"
import "@/components/sidebar.css"
import 'leaflet-sidebar';

import "leaflet-easybutton/src/easy-button.css"
import 'leaflet-easybutton'

import 'leaflet-geosearch/dist/geosearch.css'
import { CivilDefenseMapProvider, GeoSearchControl } from 'leaflet-geosearch';
//import { OpenStreetMapProvider, GeoSearchControl } from 'leaflet-geosearch';

// civil defence shelter
import VuetifyAvatar from "@/components/VuetifyAvatar.vue";
import "@/leaflet-mypanel.js"
import MainMenu from "@/components/MainMenu.vue";
//import VueUnityComponent from "@/components/VueUnityComponent.vue";
import ProjectCredits from "@/components/ProjectCredits.vue";
import {useShelterStore} from "@/stores/shelterStore";
import {useTargetStore} from "@/stores/targetStore";
import {useSearchStore} from "@/stores/searchStore";
import addShelterDialog from "@/components/addShelterDialog.vue";
import addTargetDialog from "./addTargetDialog.vue";
import DeleteShelterDialog from "@/components/DeleteShelterDialog.vue";
import DeleteTargetDialog from "./DeleteTargetDialog.vue";

import baseLayers from '@/components/baseLayers.json'
import wmsBaseLayers from '@/components/wmsBaseLayers.json'
import wmsOverlayLayers from '@/components/wmsOverlayLayers.json'

import 'leaflet.locatecontrol'
import 'leaflet.locatecontrol/dist/L.Control.Locate.css'
import 'leaflet.browser.print/dist/leaflet.browser.print'

// *** CORRECTED IMPORTS ***
// Use the hyphenated package name here.
import 'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css';
import 'leaflet-extra-markers/dist/js/leaflet.extra-markers.min.js';


export default {
	components: {
		ProjectCredits,
		MainMenu,
		//VueUnityComponent,
		VuetifyAvatar,
			LMap,
			LTileLayer,
			LGeoJson,
			LControlLayers,
			LControlScale,
			"l-wms-tile-layer": LWmsTileLayer,
		addShelterDialog,
		addTargetDialog,
		DeleteShelterDialog,
		DeleteTargetDialog,
	},
	data() {
		return {
			dialog: {
				show: false,
				text: null,
			},
			geosearchLocation: null,
			tooltipData: {
				title: null,
				id: null
			},
			zoom: 13,
			baseLayers: baseLayers.baseLayers,
			wmsBaseLayers: wmsBaseLayers.wmsBaseLayers,
			wmsOverlayLayers: wmsOverlayLayers.wmsOverlayLayers,
			mapOptions: {
				contextmenu: true,
				contextmenuWidth: 200,
				contextmenuItems: [
					{
						text: this.$t('shelter.newShelter'),
						callback: (e) => {
							this.$refs.addShelter.showDialog(e.latlng)
						},
					},
					{
						text: 'Přidat stavbu podle adresy..',
						callback: async () => {
							//console.log(this.$data.geosearchLocation)
							if(this.$data.geosearchLocation != null) {							
								this.$data.geosearchLocation.lng = this.$data.geosearchLocation.x
								this.$data.geosearchLocation.lat = this.$data.geosearchLocation.y
								await this.$refs.addShelter.showDialog(this.$data.geosearchLocation)
								await this.$refs.addShelter.showDialog(this.$data.geosearchLocation)
								this.$refs.addShelter.$forceUpdate()
								await this.$refs.addShelter.showDialog(this.$data.geosearchLocation)
								this.$data.geosearchLocation = null
							}
						},
					},
					{
						text: 'Přidat terč',
						callback: async (e) => {
							this.$refs.addTarget.showDialog(e.latlng)
						},
					},
					{
						text: 'Přidat terč podle adresy..',
						callback: async () => {
							//console.log(this.$data.geosearchLocation)
							if(this.$data.geosearchLocation != null) {							
								this.$data.geosearchLocation.lng = this.$data.geosearchLocation.x
								this.$data.geosearchLocation.lat = this.$data.geosearchLocation.y
								await this.$refs.addTarget.showDialog(this.$data.geosearchLocation)
								await this.$refs.addTarget.showDialog(this.$data.geosearchLocation)
								this.$refs.addTarget.$forceUpdate()
								await this.$refs.addTarget.showDialog(this.$data.geosearchLocation)
								this.$data.geosearchLocation = null
							}
						},
					},
					{
						separator: true,
						index: 1
					},
					{
						text: "Google Street View",
						callback: (e) => {
							window.open('https://www.google.com/maps?layer=c&cbll='+e.latlng.lat+','+e.latlng.lng, 'GSV')
						}
					}
				]
			},
			targetOptions: {
				pointToLayer: (feature, latlng) => {
					let color = 'red'; // Default color
					/*
					if (feature.properties.type === 'capital') {
						color = 'red';
					}*/

					// This part of the code remains the same.
					// The plugin attaches itself to the global L object as L.ExtraMarkers
					const extraMarkerIcon = L.ExtraMarkers.icon({
						icon: 'fa-star', // Example icon (requires Font Awesome)
						markerColor: color, // 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'violet', 'pink', 'cyan'
						shape: 'circle',
						prefix: 'fa'
					});
					
					return L.marker(latlng, { icon: extraMarkerIcon });
				},
				onEachFeature: (feature, layer) => {
					layer.bindTooltip(feature.properties.name || feature.properties.address|| 'Terč ' + feature.id)
					/*
					layer.bindTooltip(feature.properties.name,
						layer.bindPopup(() => {
							this.$data.tooltipData = {
								id: feature.id,
								title: feature.properties.name
							}
							this.$refs.tooltip.style.display="block"
							return this.$refs.tooltip
						}),
						{
							permanent: false,
							sticky: true
						});*/
						layer.bindContextMenu({
							contextmenu: true,
							contextmenuInheritItems: false,
							contextmenuItems: [{
								text: this.$t('target.edit'),
								callback: () => {
									this.$refs.addTarget.showDialog({
										lng: feature.geometry.coordinates[0],
										lat: feature.geometry.coordinates[1],
										title: feature.properties.name,
										id: feature.id
									})
								}
								},
								{
									text: this.$t('target.delete'),
									callback: () => {
									this.$refs.deleteTargetDialog.showDialog(feature.id, feature.properties.name)
									}
								},
								{
									text: "Google Street View",
									callback: () => {
										window.open('https://www.google.com/maps?layer=c&cbll='+feature.geometry.coordinates[1]+','+feature.geometry.coordinates[0], 'GSV')
									}
								}]
						});
					
				},
			},

		};
	},
	computed: {
		searchQuery: {
			get() {
				return useSearchStore().searchQuery
			},
			set(value) {
				useSearchStore().setSearchQuery(value)
			}
		},
		filteredGeojson() {
			const shelterStore = useShelterStore()
			const filteredIds = new Set(useSearchStore().filteredBuildingIds)
			const geojson = shelterStore.sheltersGeoJSON

			return {
				...geojson,
				features: geojson.features.filter((feature) => filteredIds.has(feature.id))
			}
		},
		filteredTargetGeojson() {
			const targetStore = useTargetStore()
			const filteredTargets = useSearchStore().filteredTargets
			const filteredIds = new Set(filteredTargets.map((target) => target.id))
			const geojson = targetStore.targetsGeoJSON

			return {
				...geojson,
				features: geojson.features.filter((feature) => filteredIds.has(feature.id))
			}
		},
        /**
         * Konfigurace pro GeoJSON vrstvu Úkrytů (Shelters).
         * Dynamicky mění barvu markeru podle stavu úkrytu (property `SC`).
         * @type {Object}
         */
		options() {
			return {
				onEachFeature: this.onEachFeatureFunction,
				pointToLayer: (feature, latlng) => {
					let color = 'green'; // Default color

					//console.log('Hello world!')
					//console.log(feature.properties.SC)
					//console.log(feature.properties)

					if (feature.properties.SC == null) {
						color = 'yellow';
					}
					else if (feature.properties.SC < 1) {
						color = 'blue';
					}


					// This part of the code remains the same.
					// The plugin attaches itself to the global L object as L.ExtraMarkers
					const extraMarkerIcon = L.ExtraMarkers.icon({
						icon: 'fa-home', // Example icon (requires Font Awesome)
						markerColor: color, // 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'violet', 'pink', 'cyan'
						shape: 'circle',
						prefix: 'fa'
					});
					
					return L.marker(latlng, { icon: extraMarkerIcon });
				}
			};
		},

    /**
         * Funkce aplikovaná na každý feature (úkryt) v GeoJSON vrstvě.
         * Připojuje tooltip a kontextové menu pro editaci/mazání.
         * @type {Function}
         */
		onEachFeatureFunction() {
			return (feature, layer) => {
				layer.bindTooltip(feature.properties.name || feature.properties.address|| 'Úkryt ' + feature.id)/*,
					layer.bindPopup(() => {
						this.$data.tooltipData = {
							id: feature.id,
							title: feature.properties.name || feature.properties.address
						}
						this.$refs.tooltip.style.display="block"
						return this.$refs.tooltip
					}),
					{
						permanent: false,
						sticky: true
					});*/
					layer.bindContextMenu({
						contextmenu: true,
						contextmenuInheritItems: false,
						contextmenuItems: [{
							text: this.$t('shelter.edit'),
							callback: () => {
											this.$refs.addShelter.showDialog({
												lng: feature.geometry.coordinates[0],
												lat: feature.geometry.coordinates[1],
												title: feature.properties.name,
												id: feature.id
											})
										}
							},/*
							{
								text: 'Virtuální prohlídka',
								callback: () => {
									this.$refs.virtualTour.showDialog()
								}
							},*/
							{
								text: this.$t('shelter.delete'),
								callback: () => {
								this.$refs.deleteShelterDialog.showDialog(feature.id, feature.properties.name)
								}
							},
							{
								text: "Google Street View",
								callback: () => {
									window.open('https://www.google.com/maps?layer=c&cbll='+feature.geometry.coordinates[1]+','+feature.geometry.coordinates[0], 'GSV')
								}
							}]
					});
			};
		},



	},

	methods: {
		/**
         * Inicializuje ovládací prvky mapy po jejím načtení.
         * Přidává Sidebar, EasyButton pro menu, GeoSearch, LocateControl a další panely.
         * Voláno událostí `@ready` z `l-map`.
         * 
         * @public
         * @method addControls
         * @return {void}
         */
		addControls() {
			this.$nextTick(async() => {
				this.map = this.$refs.map.leafletObject
				L.DomEvent.disableClickPropagation(this.$refs.mapSearch)
				L.DomEvent.disableScrollPropagation(this.$refs.mapSearch)

				let sidebar = L.control.sidebar('sidebar', {
				position: 'left',
				autoPan: false,
				closeButton: false
				})

				sidebar.addTo(this.map)

				// https://www.npmjs.com/package/leaflet-easybutton
				L.easyButton({
				states: [{
					stateName: 'show-sidebar',
					icon: '&equiv;',
					title: this.$t('menu.showMenu'),
					onClick: function (control) {
					sidebar.show()
					control.state('hide-sidebar');
					}
				}, {
					icon: '&equiv;',
					stateName: 'hide-sidebar',
					onClick: function (control) {
					sidebar.hide()
					control.state('show-sidebar');
					},
					title: this.$t('menu.hideMenu')
				}]
				}).addTo(this.map);

						// https://stackoverflow.com/questions/67780684/leaflet-geosearch-binding-results-marker-to-an-existing-one
				const provider = new CivilDefenseMapProvider();
						//const provider = new OpenStreetMapProvider();
				const search = new GeoSearchControl({
				provider: provider,
							showMarker: true,
							searchLabel: 'Zadejte adresu'
				});

				this.map.on('geosearch/showlocation', (data) => {
					this.$data.geosearchLocation = data.location
				});

				this.map.on('geosearch/marker/dragend', () => {
					alert('marker dragged')
				});


				this.map.addControl(search);
				L.control.locate({
							position: "topleft",
							strings: {
								title: this.$t('geolocation.showMe'),

							}
						})
						.addTo(this.map);
				L.control.browserPrint({
					position: "topleft",
					printModes:	[
						"Portrait",
						"Landscape",
						"Auto"
					]}
				).addTo(this.map);

			L.control.mypanel("avatar", {
			position: 'topright'
			}).addTo(this.map);
			L.control.mypanel("credits", {
			position: 'bottomright'}
			).addTo(this.map);
      })
    }
  },
  async mounted() {
    let shelterStore = useShelterStore()
	let targetStore = useTargetStore()

    await shelterStore.getUserShelters()
	await targetStore.getUserTargets()
  },
};

</script>

<style>
.map {
	height: 100%;
	width: 100%;
	position: relative;
}

.map-search {
	position: absolute;
	top: 12px;
	left: 50%;
	transform: translateX(-50%);
	width: min(420px, calc(100% - 24px));
	z-index: 1000;
}

#tooltip {
  width: 200px;
}

</style>
