<template>
  <LeafletMap v-if="isLoggedIn"/>
</template>

<script>
import LeafletMap from "@/components/LeafletMap.vue";
import {useAuthStore} from "@/stores/authStore";

export default {
  name: "MapView",
  components: {
    LeafletMap
  },
  computed: {
    isLoggedIn: function (){
      return useAuthStore().isAuthenticated
    }
  }
}
</script>