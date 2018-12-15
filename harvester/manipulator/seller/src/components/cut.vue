<template>
  <Manipulator name="Manipulator">
    <div class="cut-container">
      <div class="content-input-container">
        <h1>分词</h1>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="cut-button-container">
          <el-button class="submit" type="primary" @click="cutContent">分词</el-button>
        </div>
      </div>
    </div>
    <div class="result-container" v-show="sentence_list.length > 0" v-loading="loading">
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
  name: 'Cut',
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
    cutContent: function() {
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
  .cut-container {
    width: 90%;
    margin: 6rem auto 0 auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .content-input-container {
    height: 80px;
    display: flex;
  }
  .input-container {
    margin: auto;
    height: auto;
    border-radius: 10px;
  }
  .content-input-container .el-textarea {
    width: 60%;
    height: auto;
  }
  .content-input-container .cut-button-container {
    width: 10%;
    height: auto;
    margin: auto;
  }
  .cut-button-container .el-button--primary {
    color: hotpink;
    background-color: lightblue;
    width: 100%;
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
  .word.n {
    background-color: #2ca9e1;
  }
  .word.nr {
    background-color: #38b48b;
  }
  .word.v {
    background-color: #ea5506;
  }
  .word.ns {
    background-color: #6b7b6e;
  }
  .word.nt {
    background-color: #705b67;
  }
  .word.nz {
    background-color: #ec6d71;
  }
  .word.a {
    background-color: #c3d825;
  }
  .word.ad {
    background-color: #f6ad49;
  }
  .word.ag {
    background-color: #f08300;
  }
  .word.an {
    background-color: #007bbb;
  }
  .word.b {
    background-color: #b7282e;
  }
  .word.c {
    background-color: #d9333f;
  }
  .word.d {
    background-color: #954e2a;
  }
  .word.df {
    background-color: #852e19;
  }
  .word.e {
    background-color: #b0ca71;
  }
  .word.f {
    background-color: #ae7c4f;
  }
  .word.j {
    background-color: #e8d3c7;
  }
  .word.l {
    background-color: #8491c3;
  }
  .word.m {
    background-color: #00a381;
  }
  .word.nrt {
    background-color: #5383c3;
  }
  .word.nrtg {
    background-color: #5383c3;
  }
  .word.ng {
    background-color: #dccb18;
  }
  .word.o {
    background-color: #6f4b3e;
  }
  .word.p {
    background-color: #b28c6e;
  }
  .word.q {
    background-color: #e95295;
  }
  .word.r {
    background-color: #00a3af;
  }
  .word.rr {
    background-color: #a59aca;
  }
  .word.rz {
    background-color: #65318e;
  }
  .word.t {
    background-color: #00552e;
  }
  .word.u {
    background-color: #ee836f;
  }
  .word.uv {
    background-color: #df7163;
  }
  .word.ui {
    background-color: #bb5548;
  }
  .word.un {
    background-color: #e0c38c;
  }
  .word.x {
    background-color: #6b7b6e;
  }
  .word.y {
    background-color: #3eb370;
  }
  .word.z {
    background-color: #afafb0;
  }
  .word.w {
    background-color: #888084;
  }
  .word.eng {
    background-color: #93b69c;
  }
  .word.yg {
    background-color: #e5e4e6;
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
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
    user-select: none; /* Standard */
  }
</style>
