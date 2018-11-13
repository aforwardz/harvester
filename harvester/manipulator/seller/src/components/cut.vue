<template>
  <Manipulator name="Manipulator">
    <div class="cut-container">
      <h1>分词</h1>
      <div class="content-input-container">
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="cut-button-container">
          <el-button class="submit" type="primary" @click="cutContent">分词</el-button>
        </div>
      </div>
      <div class="result-container" v-loading="loading">
        <div class="sentence-item" v-for="word_list in sentence_list">
          <div class="word-item" v-for="word in word_list">
            <span :class="'word ' + word.pos">{{word.word}}</span>
            <span class="pos">{{word.pos_n}}</span>
          </div>
        </div>
      </div>
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
  data() {
    return {
      loading: false,
      content: '',
      sentence_list: [[{'word': '你', 'pos': 'n', 'pos_n': '名词'}, {'word': '怎么', 'pos': 'j', 'pos_n': '连词'},
      {'word': '肥四', 'pos': 'v', 'pos_n': '动词'}, {'word': '小老弟', 'pos': 'n', 'pos_n': '名词'},
      {'word': '？', 'pos': 'x', 'pos_n': '符号'}]]
    }
  },
  methods: {
    cutContent: function() {
      this.loading = true;
      var data = {'content': this.content};
      this.$http.post(this.API_BASE + 'nlp/cut/', data).then(
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
    /*width: 60%;*/
    /*height: 100%;*/
    background-color: lightblue;
    border-radius: 8px;
    color: hotpink;
  }
  .result-container {
    margin: 3rem auto;
    width: 90%;
    height: 50%;
    display: flex;
  }
  .sentence-item {
    width: 100%;
    display: flex;
  }
  .word-item {
    height: 20px;
    display: flex;
    margin: 1px 6px;
    flex-direction: column;
  }
  .word {
    height: 40px;
    padding: 0 1px;
    text-align: center;
    font-weight: 500;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }
  .word.n {
    background-color: #2ca9e1;
  }
  .word.nr {
    background-color: #e6b422;
  }
  .word.v {
    background-color: #ea5506;
  }
  .word.ns {
    background-color: #6b7b6e;
  }
  .word.nt {
    background-color: #6b7b6e;
  }
  .word.nz {
    background-color: #6b7b6e;
  }
  .word.a {
    background-color: #6b7b6e;
  }
  .word.ad {
    background-color: #6b7b6e;
  }
  .word.ag {
    background-color: #6b7b6e;
  }
  .word.an {
    background-color: #6b7b6e;
  }
  .word.b {
    background-color: #6b7b6e;
  }
  .word.c {
    background-color: #6b7b6e;
  }
  .word.d {
    background-color: #6b7b6e;
  }
  .word.df {
    background-color: #6b7b6e;
  }
  .word.e {
    background-color: #6b7b6e;
  }
  .word.f {
    background-color: #6b7b6e;
  }
  .word.j {
    background-color: #6b7b6e;
  }
  .word.l {
    background-color: #6b7b6e;
  }
  .word.m {
    background-color: #6b7b6e;
  }
  .word.nrt {
    background-color: #6b7b6e;
  }
  .word.nrtg {
    background-color: #6b7b6e;
  }
  .word.ng {
    background-color: #6b7b6e;
  }
  .word.o {
    background-color: #6b7b6e;
  }
  .word.p {
    background-color: #6b7b6e;
  }
  .word.q {
    background-color: #6b7b6e;
  }
  .word.r {
    background-color: #6b7b6e;
  }
  .word.rr {
    background-color: #6b7b6e;
  }
  .word.rz {
    background-color: #6b7b6e;
  }
  .word.t {
    background-color: #6b7b6e;
  }
  .word.u {
    background-color: #6b7b6e;
  }
  .word.uv {
    background-color: #6b7b6e;
  }
  .word.ui {
    background-color: #6b7b6e;
  }
  .word.un {
    background-color: #6b7b6e;
  }
  .word.uv {
    background-color: #6b7b6e;
  }
  .word.x {
    background-color: #6b7b6e;
  }
  .word.y {
    background-color: #6b7b6e;
  }
  .word.z {
    background-color: #6b7b6e;
  }
  .word.w {
    background-color: #6b7b6e;
  }
  .word.eng {
    background-color: #6b7b6e;
  }
  .word.yg {
    background-color: #6b7b6e;
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
