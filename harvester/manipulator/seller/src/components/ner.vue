<template>
  <Manipulator name="Manipulator">
    <div class="ner-container">
      <div class="ner-input-container">
        <h1>命名实体</h1>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="ner-button-container">
          <el-button class="submit" type="primary" @click="nerContent">实体识别</el-button>
        </div>
      </div>
      <div class="ner-result-container" v-show="sentence_list.length > 0" v-loading="loading">
        <div class="sentence-item" v-for="(word_list, index) in sentence_list">
          <div class="sentence-index">{{index + 1}}.</div>
          <div class="word-item" v-for="word in word_list">
            <span :class="'word ' + word.ner">{{word.word}}</span>
            <span class="ner">{{word.ner_n}}</span>
          </div>
        </div>
      </div>
    </div>
  </Manipulator>
</template>

<script>
import Manipulator from './menu';

export default {
  name: 'Ner',
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
    nerContent: function() {
      this.loading = true;
      var data = {'content': this.content};
      this.$http.post(this.API_BASE + 'nlp/ner/', data).then(
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
  .ner-container {
    width: 90%;
    margin: auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .ner-input-container {
    margin-top: 6rem;
    height: 80px;
    display: flex;
  }
  .input-container {
    margin: auto;
    height: auto;
    border-radius: 10px;
  }
  .ner-input-container .el-textarea {
    width: 60%;
    height: auto;
  }
  .ner-input-container .ner-button-container {
    width: 10%;
    height: auto;
    margin: auto;
  }
  .ner-button-container .submit {
    color: hotpink;
    background-color: lightblue;
    width: 100%;
  }
  .ner-result-container {
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
  .ner {
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
