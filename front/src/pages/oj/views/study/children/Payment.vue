<template>
  <div>
    <h1>payment test</h1>
    <Card>
      <input v-model="impCode" placeholder="impCode"/>
      <input v-model="order.name" placeholder="상품명"/>
      <input v-model="order.amount" placeholder="상품가격"/>
      <input v-model="order.buyer_tel" placeholder="전화번호"/>
      <el-button v-on:click="requestPay">결제 요청</el-button>
    </Card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 발급받은 가맹점 식별코드
      impCode: '',
      pg: "html5_inicis",
      // 결제 수단
      pay_method: "card",
      // 서버에 주문 정보를 전달하고 서버가 생성한 주문 번호
      // 결제 완료 후 결제 위변조 여부를 검증
      merchant_uid: '',
      order: {
        // 상품 이름
        name: '',
        // 상품 가격
        amount: null,
        // 구매자 이메일
        buyer_email: '',
        // 구매자 이름? 실명?
        byuer_name: '',
        // 구매자 전화번호
        buyer_tel: ''
      }
    }
  },
  methods: {
    requestPay: function () {
      // 1. 객체 초기화 (가맹점 식별코드 삽입)
      // 2. 아임포트 라이브러리 추가
      var IMP = window.IMP;
      // 우리 관리자 대시보드의 가맹점 식별번호
      IMP.init(this.impCode);
      // 3. 결제창 호출 : IMP.request_pay(param, callback)
      // param에 결제 요청에 필요한 속성과 값
      // callback에 결제 성공,실패시 로직
      IMP.request_pay({
        pg: 'jtnet',
        pay_method: 'card',
        // merchant_uid(주문번호)는 DB에 저장하여 검증시 필요하기 때문에
        // 결제 모듈을 호출하기 전에 생성 후 merchant_uid에 값을 넣어 줘야 함
        merchant_uid: 'merchant_' + new Date().getTime(),
        name: this.order.name,
        amount: this.order.amount,
        buyer_email: this.order.buyer_email,
        buyer_name: this.order.buyer_name,
        buyer_tel: this.order.buyer_tel
      }, function (rsp) {
        // 4. 결제 요청 결과 서버(자사)에 적용하기
        if (rsp.success) { // 결제 성공 시 : 결제 승인 or 가상계좌 발급에 성공한 경우
          // 5. ajax 서버 통신 구현 : 서버사이드에서 validation check
          // jQuery로 HTTP 요청
          // jQuery.ajax ({
          //   url: "https://www.myservice.com/payments/complete", // 가맹점 서버
          //   method: "POST",
          //   headers: { "Content-Type": "application/json" },
          //   // imp_uid와 merchant_uid를 서버에 전달
          //   // 결제가 완료되면 서버에서 해당 거래의 결제금액이 위변조 되었는지 검증
          //   // 거래 데이터를 여러분의 서비스의 데이터베이스에 저장하여 데이터를 동기화
          //   data: {
          //     // 가맹점 서버에 imp_uid(거래 고유 번호)를 전달하면
          //     // 아임포트 서버에서 imp_uid로 결제 정보를 조회할 수 있음
          //     imp_uid: rsp.imp_uid,
          //     // 가맹점에서 관리하는 주문번호인 merchant_uid로
          //     // 가맹점의 데이터베이스에서 주문 정보를 조회
          //     merchant_uid: rsp.merchant_uid
          //   }
          // }).done(function (data) {
          // // 가맹점 서버 결제 API 성공시 로직
          // })
        } else {
          var errMsg = '결제에 실패하였습니다.';
          errMsg += '에러내용' + rsp.error_msg
          console.log(errMsg);
        }
      });
    }
  }
}
</script>

<style>

</style>