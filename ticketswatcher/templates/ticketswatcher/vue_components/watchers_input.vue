<template id="templateWatchersInput">
  <form>
    <v-row>
      <v-text-field
          v-model="email"
          clearable
          label="Email"
          prepend-inner-icon="mdi-at"
          variant="solo"
          name="email"
          type="email"
          :rules="emailRules"
      >
        <template v-slot:append>
          <v-btn
              type="submit"
              color="primary"
          >Show
          </v-btn>
        </template>
      </v-text-field>
    </v-row>
  </form>
</template>

<script>
const watchersInput = {
  delimiters: ['[[', ']]'],
  template: '#templateWatchersInput',
  props: ['defaultEmail'],
  data() {
    return {
      email: this.defaultEmail,
      emailRules: [v => /^[^\s@]+@[^\s@]+$/.test(v) || 'Please enter an email address']
    }
  },
}

app.component('watchersInput', watchersInput);
</script>