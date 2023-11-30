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
      multiple
      variant="solo"
  ></v-select>

  <!-- concert list -->
  <ol id="concertList" class="list-group list-group-numbered">
    <concert-list-concert
        @click="concertForDialog = concert; showConcertDialog = true"
        v-for="concert in concertsFiltered"
        :concert="concert"
        :key="concert.pk">
    </concert-list-concert>
  </ol>

  <dialog-concert
      :show="showConcertDialog"
      :concert="concertForDialog"
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
    concertForDialog: null,
    showConcertDialog: false,
  }),
  methods: {
    filterConcerts() {
      this.concertsFiltered = this.concerts.filter((concert) => {
        const searchableString = concert.fields.title.toLowerCase() + concert.fields.details?.toLowerCase()
        const inSearch = searchableString.includes(this.searchQuery ?? '');

        const inProvider = this.selectedProviderNames.includes(concert.fields.provider);
        return inSearch && inProvider;
      });
    },
    filterConcertsDebounced: _.debounce(function () {
      this.filterConcerts()
    }, 250),
    setProviders() {
      this.concerts.forEach(concert => {
        concert.fields.provider_title = this.providers.filter(provider => provider.name == concert.fields.provider)[0].title;
      })
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