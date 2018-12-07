<template>
  <!--<router-view/>-->
  <component :is="menu">
    <router-view :menu.sync="menu"/>
  </component>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      menu: 'div'
    };
  },
  created: function () {
      var lastLogined = this.$session.get('lastLogined');
      if (!lastLogined) {
        this.$router.push({
          path: '/login'
        })
      }
      else if (new Date().getTime() - lastLogined > 1000 * 60 * 60) {
        this.$router.push({
          path: '/login'
        })
      }
      else {
        this.$store.state.LoginState = true
      }
    }
}
</script>

<style>
  * {
    margin: 0;
  }

#app {
  /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  margin: 0;
  padding: 0;
  height: 100vh;
  background: url('./assets/backgroud.jpg') center center no-repeat fixed;
  background-size: cover;
  font-family: 'Lato', "PingFang SC", "Microsoft YaHei", sans-serif;
  z-index: -1;
  /*overflow-y: scroll;*/
}
</style>
