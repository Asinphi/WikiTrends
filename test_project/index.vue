<template>
        <div class="container">
            <p>{{ greeting }}</p>
            <p>{{ flaskGreeting }}</p>
        </div>
</template>

<script>
export default {
        components: {
            Logo
        },
        data: function(){
            return {
                greeting: 'Hello, Vue!',
                flaskGreeting: ''
            }
        },
        created: async function(){
            const gResponse = await fetch("http://localhost:5000/greeting");
            const gObject = await gResponse.json();
            this.flaskGreeting = gObject.greeting;
        }
}
</script>
