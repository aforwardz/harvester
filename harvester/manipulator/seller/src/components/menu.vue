<template>
  <div class="manipulator-container">  <!--菜单容器-->
    <nav class="manipulator nav">
      <div class="navbar">
        <div class="route-item">
          <router-link to="/" class="route-link" tag="div" exact-active-class="menu-active">分词</router-link>
        </div>
        <div class="route-item">
          <router-link to="/label" class="route-link" tag="div" exact-active-class="menu-active">标注</router-link>
        </div>
        <div class="route-item">
          <router-link to="/keyword" class="route-link" tag="div" exact-active-class="menu-active">关键词</router-link>
        </div>
        <div class="route-item">
          <router-link to="/classify" class="route-link" tag="div" exact-active-class="menu-active">文本分类</router-link>
        </div>
        <div class="route-item">
          <router-link to="/ner" class="route-link" tag="div" exact-active-class="menu-active">实体识别</router-link>
        </div>
      </div>
    </nav>
    <main class="manipulator main">
      <slot/>
      <footer class="manipulator footer">
        &copy; Aforwardz
      </footer>
    </main>
  </div>
</template>
<script>
  export default {
    name: `Manipulator`,
    data() {
      return {
        user: null,
      };
    },
    created() {
      // Simulate fetching user data.
      setTimeout(() => {
        this.user = { name: 'Aforwardz' };
      }, 2000);
  },
  };
</script>

<style>
  .manipulator-container {
    /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /*text-align: center;*/
    color: #2c3e50;
    margin: 0;
    padding: 0;
    height: 100vh;
    background: url('https://c8.staticflickr.com/2/1614/23932828839_a242a8c831_b.jpg') center center no-repeat fixed;
    background-size: cover;
    font-family: 'Lato', "PingFang SC", "Microsoft YaHei", sans-serif;
    z-index: -1;
    display: inline-flex;
    /*overflow-y: scroll;*/
  }
  /*.manipulator-container {*/
    /*height: 100%;*/
  /*}*/
  .nav {
    width: 25%;
    height: 100%;
    display: flex;
  }
  .navbar {
    width: 60%;
    margin: auto;
    display: inline-flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, .8);
    opacity: 0.8;
    border-radius: 10px;
    height: 60%;
    justify-content: space-around;
    align-items: center;
  }
  .route-item {
    width: 80%;
    padding: 2px 0 ;
    margin: auto;
    color: gray;
    font-size: large;
  }
  .route-link {
    text-align: center;
  }
  .menu-active {
    background-color: gray;
    color: blue;
    opacity: 0.7;
  }
  .main {
    width: 90%;
    height: 80%;
    margin: auto;
  }
</style>
