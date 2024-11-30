<template id="templateConcertList">
  <!-- search field -->
  <v-text-field
      v-model="searchQuery"
      clearable
      label="Search"
      prepend-inner-icon="mdi-magnify"
      variant="solo"
  ></v-text-field>

  <v-select
      v-model="selectedProviderNames"
      :items="providers"
      item-value="name"
      item-title="title"
      chips
      label="Select providers"
      prepend-inner-icon="mdi-music"
      multiple
      variant="solo"
  ></v-select>

  <v-switch
      v-model="showOnlyFree"
      color="primary"
      label="Show only concerts with tickets available"
      @update:model-value="filterConcertsDebounced"
  ></v-switch>

  <v-btn-toggle
      v-model="displayMode"
      divided
  >
    <v-btn icon="mdi-view-grid"></v-btn>
    <v-btn icon="mdi-view-list"></v-btn>
  </v-btn-toggle>

  <!-- concert list -->
  <span v-if="displayMode === 1">
    <ol id="concertList"
        class="list-group list-group-numbered">
      <span v-for="concert in concerts"
            :key="concert.pk"
      >
        <concert-list-concert
            @click="openConcert(concert)"
            :concert="concert"
            :style="{display: concertsFiltered.includes(concert) ? 'block' : 'none'}"
        ></concert-list-concert>
      </span>
    </ol>
  </span>

  <span v-else>
    <v-container fluid>
      <v-row dense>
        <v-col
            v-for="concert in concerts"
            :key="concert.pk"
            :cols="gridColumnWidth"
            :style="{display: concertsFiltered.includes(concert) ? 'block' : 'none'}"
        >
          <concert-list-concert-card
              @click="openConcert(concert)"
              :concert="concert"
              :providers="providers"
          ></concert-list-concert-card>
        </v-col>
      </v-row>
    </v-container>
  </span>

  <dialog-concert
      :show="showConcertDialog"
      :concert-id="dialogConcertId"
      :concert-title="dialogConcertTitle"
      @concert-dialog-close="showConcertDialog = false"
  ></dialog-concert>
</template>

<script>
const concertList = {
  delimiters: ['[[', ']]'],
  template: '#templateConcertList',
  props: ['providers', 'concerts'],
  data: () => ({
    selectedProviderNames: this.providers.filter(p => p.selected).map(p => p.name),
    concertsFiltered: [],
    searchQuery: null,
    dialogConcertId: null,
    dialogConcertTitle: "",
    showConcertDialog: false,
    showOnlyFree: false,
    displayMode: 0,
  }),
  computed: {
    gridColumnWidth() {
      if (window.innerWidth >= 1000) return 4
      if (window.innerWidth >= 700) return 6
      else return 12
    }
  },
  methods: {
    filterConcerts() {
      console.log("filtering concerts")
      let concertsFiltered = this.concerts;
      // filter by free
      if (this.showOnlyFree) {
        concertsFiltered = concertsFiltered.filter((concert) => {
          return concert.fields.available_tickets > 0;
        });
      }

      concertsFiltered = concertsFiltered.filter((concert) => {
        const searchableString = concert.fields.title.toLowerCase() + concert.fields.details?.toLowerCase()
        const inSearch = searchableString.includes(this.searchQuery.toLowerCase() ?? '');

        const inProvider = this.selectedProviderNames.includes(concert.fields.provider);
        return inSearch && inProvider;
      });
      this.concertsFiltered = concertsFiltered;
    },
    filterConcertsDebounced: _.debounce(function () {
      this.filterConcerts()
    }, 250),
    setProviders() {
      this.concerts.forEach(concert => {
        concert.fields.provider_title = this.providers.filter(provider => provider.name == concert.fields.provider)[0].title;
      })
    },
    openConcert(concert) {
      this.dialogConcertId = concert.pk;
      this.dialogConcertTitle = concert.fields.title;
      this.showConcertDialog = true
    }
  },
  watch: {
    selectedProviderNames: {
      handler: function () {
        this.filterConcertsDebounced();
      },
      deep: true,
    },
    searchQuery: {
      handler: function () {
        this.filterConcertsDebounced();
      }
    }
  },
  mounted() {
    this.filterConcerts();
    this.setProviders();
  },
}

app.component('concertList', concertList);
</script>