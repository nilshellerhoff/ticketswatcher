<template id="templateConcert">
  <a :href="`/concert/${concert.pk}`" class="text-decoration-none">
    <li class="list-group-item d-flex justify-content-between align-items-start">
      <div class="ms-2 me-auto">
        [[ concert.fields.provider_title ]]
        <div class="fw-bold">[[ concert.fields.title ]]</div>
        <div style="font-size: 14px">
          <i class="bi bi-clock-fill"></i>
          <formatted-date :date="concert.fields.datetime"></formatted-date>
          <br>
          <i class="bi bi-geo-alt-fill"></i> [[ concert.fields.venue ]]
        </div>
      </div>
      <span :class="`badge ${availablePill.color} rounded-pill`">[[ availablePill.label ]]</span>
    </li>
  </a>
</template>

<script>
Vue.component('concert', {
  delimiters: ['[[', ']]'],
  template: '#templateConcert',
  props: ['concert'],
  computed: {
    availablePill() {
      const avail = this.concert.fields.available_tickets
      if (avail >= 20) return {label: '20+', color: 'bg-success'}
      else if (avail > 0) return {label: avail, color: 'bg-warning'}
      else if (avail !== null) return {label: avail, color: 'bg-danger'}
      else return {label: '--', color: 'bg-secondary'}
    },
  }
});
</script>