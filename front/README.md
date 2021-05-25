# Codeend Front End

## Reference
[dllreferenceplugin 설명](https://webpack.js.org/plugins/dll-plugin/#dllreferenceplugin)

[build/webpack.dll.conf.js 관련 설명](https://olaf.kr/2018/05/21/webpack4-dllplugin-configuration/)

## Get Started

Install nodejs **v8.12.0** first

### Linux

```bash
# 패키지 설치
cd front 
npm install

# 패키지 설치 후 한번만 실행
export NODE_ENV=development 
npm run build:dll

# 백앤드 프록시 테이블 셋팅 
# 기본적으로 localhost
export TARGET=http://Your-backend

# localhost:8080에서 핫 리로드
npm run dev
```
### Windows

```bash
# 패키지 설치
cd front 
npm install

# 패키지 설치 후 한번만 실행
$env:NODE_ENV="development"
npm run build:dll

# 백앤드 프록시 테이블 셋팅 
# 기본적으로 localhost
$env:TARGET="http://localhost"

# localhost:8080에서 핫 리로드
npm run dev
```

## LICENSE

[MIT](http://opensource.org/licenses/MIT)
