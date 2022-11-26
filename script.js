ScrapeElement = function(link, pathArray) {  // path는 array여야 함.
    var xmlHttp = new XMLHttpRequest();  // XMLHttpRequest 객체를 생성함.
    var arr = [];
    xmlHttp.onreadystatechange = function() {  // onreadystatechange 이벤트 핸들러를 작성함.
        if(this.status == 200 && this.readyState == this.DONE) {  // 서버 상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때
            var dom = new DOMParser().parseFromString(xmlHttp.responseText, 'text/html');
            for (var i = 0; i < pathArray.length; i++) {
                arr[i] = dom.querySelector(pathArray[i]).innerHTML;
            }
        }
    };
    xmlHttp.open("GET", "https://cors-anywhere.herokuapp.com/" + link, true);  // proxy server로 우회.
    xmlHttp.send();
    return arr;
}

class Department {
    constructor(page, path, plist, timestamp) {
        this.page = page;
        this.pathArray = new Array(path + plist[0], path + plist[1], path + plist[2], timestamp);
    }
    Scrape() {
        this.scrape = ScrapeElement(this.page, this.pathArray);
        this.accepted = this.scrape[0];
        this.sent = this.scrape[1];
        this.rate = this.scrape[2];
        this.time_string = this.scrape[3];
        return this.scrape;
    }
}

const PAGE_1 = "http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==";
var ulsan = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");
console.log(ulsan.Scrape());

const PAGE_2 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html";
var pusan = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

const PAGE_3 = "http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=";
var kyunghee = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

const PAGE_4 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html";
var hanyang = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

const PAGE_5 = "http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==";
var korea = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

const PAGE_6 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html";
var ajou = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");