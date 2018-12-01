<template>
  <Manipulator name="Manipulator">
    <div class="graph-container">
      <div class="graph-search-input-container">
        <h1>分词</h1>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="你可以问：梅西的儿子是谁？"></el-input>
        <div class="cut-button-container">
          <el-button class="submit" type="primary" @click="cutContent">分词</el-button>
        </div>
      </div>
    </div>
    <div class="graph-result-container" v-show="sentence_list.length > 0" v-loading="loading">
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
  name: "Graph",
  components: {
    Manipulator,
  },
  data() {
    return {
      loading: false,
      content: '',
      sentence_list: []
    }
  }
}
</script>

<style scoped>

</style>
