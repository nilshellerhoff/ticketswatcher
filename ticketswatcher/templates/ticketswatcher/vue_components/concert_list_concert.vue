<template id="templateConcertListConcert">
  <span>
    <li class="list-group-item d-flex justify-content-between align-items-start">
      <div class="ms-2 me-auto">
        [[ concert.fields.provider_title ]]
        <div class="fw-bold">[[ concert.fields.title ]]</div>
        <div style="font-size: 14px">
          <i class="bi bi-clock-fill"></i>&nbsp;
          <formatted-date :date="concert.fields.datetime"></formatted-date>
          <br>
          <i class="bi bi-geo-alt-fill"></i>&nbsp;[[ concert.fields.venue ]]
        </div>
      </div>
      <span :class="`badge ${availablePill.color} rounded-pill`">[[ availablePill.label ]]</span>
    </li>
    </span>
</template>

<script>
const concertListConcert = {
  delimiters: ['[[', ']]'],
  template: '#templateConcertListConcert',
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
}

app.component('concertListConcert', concertListConcert);
</script>