<template>
  <v-container
      fluid
      style="height: 300px"
  >

    <v-row justify="center">
      <v-menu
          min-width="200px"
          rounded
      >
        <template v-slot:activator="{ props }">
          <v-btn
              icon
              v-bind="props"
          >
            <v-avatar
                color="brown"
                size="large"
            >
              <span v-if="$keycloak.authenticated" class="text-h5">{{ initials }}</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-card-text>
            <div class="mx-auto text-center">
              <v-avatar
                  color="brown"
              >
                <span v-if="$keycloak.authenticated" class="text-h5">{{ initials }}</span>
              </v-avatar>
              <h3>{{ fullName }}</h3>
              <p class="text-caption mt-1" v-if="$keycloak.authenticated">{{ $keycloak.tokenParsed.preferred_username }}</p>
              <p v-if="userRealmRoles && userRealmRoles.length > 0">
                <span v-for="role in userRealmRoles" :key="role">
                  {{ role }}
                </span>
              </p>
              <p class="text-caption mt-1">
                {{ email }}
              </p>
              <v-divider class="my-3"></v-divider>
              <v-btn
                  rounded
                  variant="text"
                  @click="buttonLogout"
              >
								{{ $t("user.signOut") }}
							</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-menu>
    </v-row>
  </v-container>
</template>

<script>
/**
 * @file VuetifyAvatar.vue
 * @brief Komponenta uživatelského profilu (Avatar).
 * 
 * @description
 * Tato komponenta zobrazuje avatar s iniciály přihlášeného uživatele (obvykle v rohu mapy).
 * Po kliknutí na avatar se otevře rozbalovací menu (v-menu) obsahující:
 * - Celé jméno a uživatelské jméno.
 * - Uživatelské role (Realm roles).
 * - Email.
 * - Tlačítko pro odhlášení.
 * 
 * Komponenta je plně závislá na globálním objektu `$keycloak` pro získávání
 * informací o identitě a pro provádění odhlášení.
 * 
 * @component
 * @example
 * <vuetify-avatar />
 */
//import {useAuthStore} from "@/stores/authStore";

export default {
  name: 'VuetifyAvatar',
  data() {
    return {
    }
  },
	computed: {
    /**
     * Získá email uživatele z Keycloak tokenu.
     * Pokud není k dispozici, vrací fallback hodnotu.
     * @type {string}
     */
		email() {
			return this.$keycloak?.tokenParsed?.email || "john@dow.com"; //useAuthStore().$state.user.email
		},
    // A good practice to check if the user is authenticated
      /**
   * Ověří, zda je uživatel autentizován vůči Keycloaku.
   * @type {boolean}
   */
    isAuthenticated() {
      // The keycloak object and its `authenticated` property are provided by the plugin
      return this.$keycloak && this.$keycloak.authenticated;
    },
    // A computed property for the user's full name for easier access
      /**
   * Získá celé jméno uživatele z tokenu.
   * Pokud není k dispozici, vrací 'Guest'.
   * @type {string}
   */
    fullName() {
      // Use optional chaining (?.) to prevent errors if tokenParsed is not yet available
      return this.$keycloak?.tokenParsed?.name || 'Guest';
    },
      /**
   * Získá seznam rolí uživatele (Realm roles) z tokenu.
   * Slouží pro zobrazení oprávnění v menu.
   * @type {Array<string>}
   */
    userRealmRoles() {
      console.log(this.$keycloak.hasRealmRole("supervisor"))
      //console.log(this.$keycloak.tokenParsed.realm_access.roles)
      // Use optional chaining (?.) to prevent errors if the path doesn't exist.
      // Return an empty array as a fallback.
      return this.$keycloak?.tokenParsed?.realm_access?.roles ?? [];
    },

    // **THE COMPUTED PROPERTY FOR THE INITIALS**
      /**
   * Vypočítá iniciály uživatele z jeho celého jména.
   * Rozdělí jméno podle mezer, vezme první písmeno každé části a převede na velká písmena.
   * Pokud uživatel není přihlášen, vrátí 'G'.
   * @type {string}
   */
    initials() {
      // First, ensure the user is authenticated and the name exists
      if (this.isAuthenticated && this.fullName && this.fullName !== 'Guest') {
        // Now apply the splitting logic from before
        return this.fullName
          .split(/\s+/) // Split by one or more whitespace characters
          .filter(Boolean) // Remove empty strings
          .map(word => word[0]) // Get the first character of each word
          .join('') // Join them together
          .toUpperCase(); // Often, initials are displayed in uppercase
      }
      // Provide a fallback if there is no name or the user is not logged in
      return 'G';
    }
	},
  methods: {
     /**
     * Odhlásí uživatele.
     * Volá metodu `logout` na instanci Keycloaku a přesměruje uživatele na kořenovou adresu aplikace.
     * 
     * @public
     * @method buttonLogout
     * @return {void}
     */
    buttonLogout() {
      this.$keycloak.logout({ redirectUri: window.location.origin });
      /*
      const authStore = useAuthStore()
      authStore.logOut()
      this.$router.push('/login')*/
    }
  }
}
</script>
