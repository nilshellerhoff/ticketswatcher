<template id="templateConcertListConcert">
  <span>
    <li class="list-group-item d-flex justify-content-between align-items-start" style="cursor: pointer">
      <div :style="{height: `${imageWidth}px`, width: `${imageWidth}px`, flexShrink: 0, margin: 'auto 0'}">
        <img :style="{objectFit: 'cover', width: '100%', height: '100%', borderRadius: '5px'}"
             :src="concert.fields.image || '/static/img/placeholder.png'"
             loading="lazy"
        />
      </div>
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
  data: () => ({
    imageWidth: window.innerWidth > 600 ? 80 : 60,
  }),
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