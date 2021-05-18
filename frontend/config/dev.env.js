"use strict";
const merge = require("webpack-merge");
const prodEnv = require("./prod.env");

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // 에러 추적 : 유저가 어느때에 정확히 어떤 에러가 난건지 서술
  USE_SENTRY: "0"
});
