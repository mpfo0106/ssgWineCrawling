# ssgWineCrawling
신세계 와인( https://www.shinsegae-lnb.com/html/product/wine.html ) 정보를 크롤링

### scrapy + selenium 으로

각 와인 상품별
* 각 상품을 구분할 수 있는 값 (id)
* 와인명 (국, 영)
* 와인 상세 정보
* 와인 설명
* 와인 이미지 주소
* 와인 맛 특징

를 items 로 뽑아서 mongoDB 에 저장하는 과정까지를 구현.

### 수정해야할 것
+ 여러 페이지의 아이템들을 가져오는 부분에서 middlewares를 어떻게 짜야하는지 막혔다.
+ 현재 1페이지 외 여러페이지의 크롤링은 안되는상태..
