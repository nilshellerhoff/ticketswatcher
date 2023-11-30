<template id="templateFormattedDate">
  <span>[[ formattedDate ]]</span>
</template>

<script>
const formattedDate = {
  delimiters: ['[[', ']]'],
  template: '#templateFormattedDate',
  props: ['date'],
  computed: {
    formattedDate() {
      const datetime = new Date(this.date)
      const dateOptions = {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      }
      return datetime.toLocaleString('de-DE', dateOptions)
    }
  }
}

app.component('formattedDate', formattedDate);
</script>