<template>
  <Manipulator name="Manipulator">
    <div class="label-container">
      <div class="label-input-container">
        <h1>标注</h1>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="label-button-container">
          <el-button class="submit" type="primary" @click="labelContent">走你</el-button>
        </div>
      </div>
    </div>
    <div class="result-container" v-show="label_list.length > 0" v-loading="loading">
      <div class="raw-item" v-for="word_list in label_list">
        <div class="raw-word-item" v-for="word in word_list">
          <span class="raw-word">{{word.word}}</span>
          <span class="pos">{{word.pos_n}}</span>
        </div>
      </div>
      <div class="label-item" v-for="word_list in label_list">
        <div class="label-word-item" v-for="(word, index) in word_list">
          <span :class="'ner-word ' + word.ner">{{word.word}}</span>
          <span class="ner">{{word.ner_n}}</span>
        </div>
      </div>
    </div>
  </Manipulator>
</template>

<script>
import Manipulator from './menu';

export default {
  name: 'Label',
  components: {
    Manipulator,
  },
  data() {
    return {
      loading: false,
      content: '',
      label_list: []
    }
  },
  methods: {
    labelContent: function() {
      this.loading = true;
      var data = {'content': this.content};
      this.$http.post(this.NLP_BASE + 'label/', data).then(
        (response) => {
          this.label_list = response.body.data;
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
  .label-container {
    width: 90%;
    margin: 6rem auto 0 auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .label-input-container {
    height: 80px;
    display: flex;
  }
  .input-container {
    height: auto;
    width: auto;
    border-radius: 10px;
  }
  .label-input-container .el-textarea {
    width: 60%;
    height: auto;
  }
  .label-input-container .label-button-container {
    width: 10%;
    height: auto;
    margin: auto;
  }
  .label-button-container .submit {
    width: 100%;
    background-color: lightblue;
    color: hotpink;
  }
  .result-container {
    margin: 3rem auto;
    width: 90%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 15px;
  }
</style>
