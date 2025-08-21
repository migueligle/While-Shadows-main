<template>
  <div class="content">
    <GmapMap :center="mapCenter" :zoom="zoomLevel" style="height: 400px; width: 100%">
      <GmapMarker :position="markerCoordinates"></GmapMarker>
    </GmapMap>
  </div>
</template>

<script>
export default {
  name: 'GoogleMapVue',
  data () {
    return {
      mapCenter: { lat: 41.9531325, lng: -4.5154456 },
      zoomLevel: 15,
      markerCoordinates: { lat: 41.9531325, lng: -4.5154456 }
    }
  }
}
</script>

<style>
</style>
