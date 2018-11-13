<template>
  <Manipulator name="Manipulator">
    <div class="cut-container">
      <h1>分词</h1>
      <!--<p>-->
        <!--Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy-->
        <!--eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam-->
        <!--voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet-->
        <!--clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit-->
        <!--amet.-->
      <!--</p>-->
      <div class="content-input-container">
        <el-input placeholder="请输入内容"></el-input>
        <div class="cut-button-container">
          <button class="submit">分词</button>
        </div>
      </div>
      <h2>Amet sit</h2>
      <p>
        Eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
        voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
        clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
        amet.
      </p>
    </div>
  </Manipulator>
</template>

<script>
import Manipulator from './menu';

export default {
  name: 'Cut',
  components: {
    Manipulator,
  },
};
</script>

<style>
  h1 {
    /*margin: 10px 10px;*/
  }
  .cut-container {
    width: 90%;
    margin: auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .content-input-container {
    margin-top: 5rem;
    height: 80px;
    display: flex;
  }
  .input-container {
    height: 50%;
    width: 60%;
    margin: auto;
    border-radius: 10px;
  }
  .cut-button-container {
    width: 10%;
    height: 40%;
    margin: auto;
  }
  .submit {
    width: 60%;
    height: 100%;
    background-color: lightblue;
    border-radius: 8px;
    color: hotpink;
  }
</style>
