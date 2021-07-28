<template>
<div>
  <Panel>
     <el-form ref="form" :model="board" :rules="rules" label-position="top" label-width="100px">
               <el-row :gutter="20">
          <el-col :span="6">
            <div>{{$t('m.Write')}}</div>
          </el-col>
          <el-col :span="18">
            <el-form-item prop="title" :label="$t('m.Title')" required>
              <el-input :placeholder="$t('m.Title')" v-model="board.title"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      <el-form-item :label="$t('m.Category')">
        <el-select size="small" :placeholder="$t('m.Choose_Category')">
        <el-option :label="$t('m.Free')" value="Free"></el-option>
        <el-option :label="$t('m.Question')" value="Question"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <Simditor v-model="board.content"></Simditor>
      </el-form-item>
      
    </el-form>
  </Panel>
</div>
</template>

<script>
  import Simditor from '../../../../admin/components/Simditor'

  export default {
    name: 'Board',
    components: {
      Simditor
    },
    data () {
      return {
        rules: {
          title: {required: true, message: '제목이 필요합니다.', trigger: 'blur'},
          category: {required: true, message: '카테고리 선택이 필요합니다.', trigger: 'blur'}
        },
        board: ''
      }
    }
  }
</script>
<style scoped>
  .page {
    margin-top: 20px;
    text-align: right
  }

</style>
