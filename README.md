## How to set development enviornment

### Windows 10 개발 환경 세팅
1. CRLF off
    ```bash
    git config --global core.autocrlf input
    ```  
2. docker 실행  
3. git 최신 소스 코드 업데이트  
    * 코드 없을 시
    ```bash
        git clone https://github.com/rhsehfm33/Codeend.git
    ```
    * 코드 이미 있다면
    ```bash
        git pull
    ```
4. git 최상위로 이동 (ex. c:/dev/Codeend/)
5. docker 서버 구동
    ```bash
        docker-compose up
    ```
6. 로컬 작업 폴더에서 백엔드 코드의 변경이 있을 경우, 해당 container를 재실행 시켜주세요.
   그래야 코드 변경 내역이 적용됩니다.


-----------------


### MAC OS 개발 환경 세팅
1. docker 실행
2. git 최신 소스 코드 업데이트
    * 코드 없을 시
    ```bash
        git clone https://github.com/rhsehfm33/Codeend.git
    ```
    * 코드 이미 있다면
    ```bash
        git pull
    ```
3. git 최상위로 이동 (ex. /your_path/Codeend/)
4. workdir의 모든 권한을 허용하도록 설정
    ```bash
        sudo chmod -R 777 ./code
    ```
5. docker 서버 구동
    ```bash
        docker compose up
    ```
6. 로컬 작업 폴더에서 백엔드 코드의 변경이 있을 경우, 해당 container를 재실행 시켜주세요. 
그래야 코드 변경 내역이 적용됩니다.

-----------------
### License
[MIT](https://opensource.org/licenses/MIT)