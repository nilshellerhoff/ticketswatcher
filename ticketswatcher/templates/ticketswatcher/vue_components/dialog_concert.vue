<template id="templateDialogConcert">
  <v-dialog v-model="show" max-width="1200" :height="height" :fullscreen="isFullscreen">
    <v-card
      height="100%"
    >
      <v-toolbar
          dark
          color="primary"
      >
        <v-btn
            icon
            dark
            @click="close()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>[[ concertTitle ]]</v-toolbar-title>
      </v-toolbar>

      <div class="pa-6" style="height: 100%">
        <iframe :src="`/concert/${concertId}`" style="width: 100%; height: 100%"></iframe>
      </div>
    </v-card>

  </v-dialog>
</template>

<script>
const dialogConcert = {
  delimiters: ['[[', ']]'],
  template: '#templateDialogConcert',
  props: ['show', 'concertId', 'concertTitle'],
  data() {
    return {
      isFullscreen: window.innerWidth <= 600,
      height: window.innerWidth <= 600 ? '100%' : '80%'
    }
  },
  // computed: {
  //   isFullscreen() { return window.innerWidth <= 600 },
  //   height() { return window.innerWidth <= 600 ? '100%' : '80%' },
  // },
  methods: {
    close() {
      this.$emit('concert-dialog-close')
    }
  }
}

app.component('dialogConcert', dialogConcert);
</script>