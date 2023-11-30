<template id="templateAppBar">
  <v-app-bar
      color="primary"
      prominent
  >
    <v-app-bar-nav-icon variant="text"
                        @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

    <v-toolbar-title>[[ title ]]</v-toolbar-title>

  </v-app-bar>

  <v-navigation-drawer
      v-model="drawer"
  >
    <v-list>
      <v-list-item
          v-for="link in links"
          :key="link.value"
          :value="link"
          color="primary"
          :href="link.href"
      >
        <template v-slot:prepend>
          <v-icon :icon="link.icon"></v-icon>
        </template>
        <!--        <a :href="link.href">-->
        <v-list-item-title v-text="link.title"></v-list-item-title>
        <!--        </a>-->
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn
            block
            variant="outlined"
            color="primary"
            href="https://github.com/nilshellerhoff/ticketswatcher"
            target="_blank"
        >
          <img src="https://github.githubassets.com/favicons/favicon.png"
               style="height: 20px; margin-right: 4px">Github
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
const appBar = {
  delimiters: ['[[', ']]'],
  template: '#templateAppBar',
  props: ['title'],
  data() {
    return {
      links: [{
        value: "concerts",
        title: "Concerts",
        href: "/",
        icon: "mdi-music"
      },
        {
          value: "watchers",
          title: "My Watchers",
          href: "/watchers",
          icon: "mdi-eye-outline"
        }
      ],
      drawer: null,
    }
  },
  computed: {}
}

app.component('appBar', appBar);
</script>