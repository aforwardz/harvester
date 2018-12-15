<template>
  <Manipulator name="Manipulator">
    <div class="classify-container">
      <div class="classify-input-container">
        <h1>文本分类</h1>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="classify-button-container">
          <el-button class="submit" type="primary" @click="classifyContent">分类</el-button>
        </div>
      </div>
    </div>
    <div class="classify-result-container" v-show="sentence_list.length > 0" v-loading="loading">
      <div class="sentence-item" v-for="(word_list, index) in sentence_list">
        <div class="sentence-index">{{index + 1}}.</div>
        <div class="word-item" v-for="word in word_list">
          <span :class="'word ' + word.pos">{{word.word}}</span>
          <span class="pos">{{word.pos_n}}</span>
        </div>
      </div>
    </div>
  </Manipulator>
</template>

<script>
import Manipulator from './menu';

export default {
  name: 'Classify',
  components: {
    Manipulator,
  },
  data() {
    return {
      loading: false,
      content: '',
      sentence_list: []
    }
  },
  methods: {
    classifyContent: function() {
      this.loading = true;
      var data = {'content': this.content};
      this.$http.post(this.NLP_BASE + 'cut/', data).then(
        (response) => {
          this.sentence_list = response.body.data;
          this.loading = false;
        }
      )
    }
  }
};
</script>

<style>
  h1 {
    margin: 16px 0 0 10px;
  }
  .classify-container {
    width: 90%;
    margin: 6rem auto 0 auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .classify-input-container {
    height: 80px;
    display: flex;
  }
  .classify-input-container .input-container {
    margin: auto;
    height: auto;
    border-radius: 10px;
  }
  .classify-input-container .el-textarea {
    width: 60%;
    height: auto;
  }
  .classify-input-container .classify-button-container {
    width: 10%;
    height: auto;
    margin: auto;
  }
  .classify-button-container .submit {
    color: hotpink;
    background-color: lightblue;
    width: 100%;
  }
  .classify-result-container {
    margin: 3rem auto;
    width: 90%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 15px;
  }
  .sentence-index {
    height: 38px;
    margin: 12px 2px 0 0;
  }
  .sentence-item {
    width: 95%;
    display: flex;
    margin: 10px auto;
    flex-wrap: wrap;
  }
  .word-item {
    height: 38px;
    display: flex;
    margin: 5px 6px;
    flex-direction: column;
  }
  .word {
    height: 22px;
    padding: 0 1px;
    text-align: center;
    font-weight: 500;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }
  .pos {
    height: 16px;
    padding: 0 1px;
    font-size: 12px;
    color: #f7faf5;
    text-align: center;
    background-color: #7d7d7d;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
  }
</style>
