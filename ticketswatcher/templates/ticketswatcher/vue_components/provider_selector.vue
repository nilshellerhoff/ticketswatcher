<template id="templateProviderSelector">
    <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" :name="provider.id" :id="provider.id"
               v-model="provider.selected">
        <label class="form-check-label" :for="provider.id">
            [[ provider.title ]]
        </label>
    </div>
</template>

<script>
    Vue.component('providerSelector', {
        delimiters: ['[[', ']]'],
        template: '#templateProviderSelector',
        props: ['provider'],
    })
</script>