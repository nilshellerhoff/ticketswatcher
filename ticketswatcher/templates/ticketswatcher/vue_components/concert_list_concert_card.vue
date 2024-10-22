<template id="templateConcertListConcertCard">
  <v-card
      class="mx-auto"
      max-width="344"
  >
    <v-img
        height="200px"
        :src="concert.fields.image || '/static/img/placeholder.png'"
        cover
    ></v-img>

    <v-card-item>
      <div>[[ provider ]]</div>
      <v-card-title style="font-size: 16px">
        [[ concert.fields.title ]]
      </v-card-title>


      <div style="font-size: 14px">
        <i class="bi bi-clock-fill"></i>&nbsp;
        <formatted-date :date="concert.fields.datetime"></formatted-date>
        <span :class="`badge ${availablePill.color} rounded-pill`"
              style="float: right">[[ availablePill.label ]]</span>
        <br>
        <i class="bi bi-geo-alt-fill"></i>&nbsp;[[ concert.fields.venue ]]
      </div>

      <v-card-actions>
        <v-btn
            :prepend-icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
            @click.stop="show = !show"
            :disabled="!detailsHtml"
        >details
        </v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="show">
          <v-card-text>
            <span v-html="detailsHtml"></span>
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card-item>
  </v-card>
</template>

<script>
const concertListConcertCard = {
  delimiters: ['[[', ']]'],
  template: '#templateConcertListConcertCard',
  props: ['concert', 'providers'],
  data: () => ({
    imageWidth: window.innerWidth > 600 ? 80 : 60,
    show: false,
  }),
  computed: {
    availablePill() {
      const avail = this.concert.fields.available_tickets
      if (avail >= 20) return {label: '20+', color: 'bg-success'}
      else if (avail > 0) return {label: avail, color: 'bg-warning'}
      else if (avail !== null) return {label: avail, color: 'bg-danger'}
      else return {label: '--', color: 'bg-secondary'}
    },
    provider() {
      return this.providers.filter(provider => provider.name == this.concert.fields.provider)[0].title;
    },
    detailsHtml() {
      return this.concert.fields.details?.replaceAll('\n\n', '\n').replaceAll('\n\n', '\n').replaceAll('\n', '<br>')
    }
  }
}

app.component('concertListConcertCard', concertListConcertCard);
</script>