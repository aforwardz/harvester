<template>
  <div class="manipulator-container">  <!--菜单容器-->
    <nav class="manipulator nav">
        <el-menu
        :default-active="activeMenu"
        class="el-menu"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-submenu index="1">
          <template slot="title">NLP</template>
          <el-menu-item index="1-1">
            <router-link to="/" class="route-link" tag="div" exact-active-class="menu-active">分词</router-link>
          </el-menu-item>
          <el-menu-item index="1-2">
            <router-link to="/classify" class="route-link" tag="div" exact-active-class="menu-active">文本分类</router-link>
          </el-menu-item>
          <el-menu-item index="1-3">
            <router-link to="/ner" class="route-link" tag="div" exact-active-class="menu-active">实体识别</router-link>
          </el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">工具</template>
          <el-menu-item index="2-1">
            <router-link to="/label" class="route-link" tag="div" exact-active-class="menu-active">标注</router-link>
          </el-menu-item>
          <el-menu-item index="2-2" disabled>足球图谱</el-menu-item>
          <el-menu-item index="2-3" disabled>刷脸</el-menu-item>
        </el-submenu>
        <el-menu-item index="3" disabled>学习</el-menu-item>
        <el-menu-item index="4" disabled>扯淡</el-menu-item>
      </el-menu>
      <div class="user">
        <div class="user-info" v-if="user">{{user.name}}</div>
        <div class="login" v-else>登录</div>
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
    name: 'Manipulator',
    data() {
      return {
        user: null,
        activeMenu: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    },
    created() {
      // Simulate fetching user data.
      setTimeout(() => {
        this.user = { name: 'Aforwardz' };
      }, 200);
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
    width: 100%;
    height: 100vh;
    background: url('../assets/backgroud.jpg') center center no-repeat fixed;
    background-size: cover;
    font-family: 'Lato', "PingFang SC", "Microsoft YaHei", sans-serif;
    z-index: -1;
    display: inline-block;
    overflow-y: auto;
  }
  /*.manipulator-container {*/
    /*height: 100%;*/
  /*}*/
  .el-menu {
    width: 80%;
    display: flex;
    justify-content: space-around;
    opacity: 0.9;
    border-right: solid 1px rgb(230, 230, 230);
    position: absolute;
  }
  .nav {
    width: 100%;
    display: flex;
    margin-bottom: 3rem;
    position: absolute;
  }
  .user {
    width: 20%;
    display: flex;
    background-color: rgb(84, 92, 100);
    opacity: 0.9;
    border-left: 1px whitesmoke;
    border-bottom: solid 1px #e6e6e6;
  }
  .user-info {
    margin: auto;
  }
  .main {
    width: 100%;
    /*height: 80%;*/
    margin: 2rem 5% 5% auto;
  }
  .footer {
    text-align: center;
    position: absolute;
    bottom: 0;
    justify-content: center;
    width: 100%;
    color: #c8c2be;
  }
</style>
