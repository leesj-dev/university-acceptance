ScrapeElement = function(link, pathArray) {  // path는 array여야 함.
    let xmlHttp = new XMLHttpRequest();  // XMLHttpRequest 객체를 생성함.
    let arr = [];
    xmlHttp.onreadystatechange = function() {  // onreadystatechange 이벤트 핸들러를 작성함.
        if(this.status == 200 && this.readyState == this.DONE) {  // 서버 상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때
            let dom = new DOMParser().parseFromString(xmlHttp.responseText, 'text/html');
            for (let i = 0; i < pathArray.length; i++) {
                arr[i] = dom.querySelector(pathArray[i]).innerHTML;
            }
        }
    };
    xmlHttp.open("GET", "https://proxy.cors.sh/" + link, true);  // proxy server로 우회.
    xmlHttp.send();
    return arr;
}

class Department {
    constructor(page, path, plist, timestamp) {
        this.page = page;
        this.pathArray = new Array(path + plist[0], path + plist[1], path + plist[2], timestamp);
    }
    GetInfo() {
        this.scrape = ScrapeElement(this.page, this.pathArray);
        this.accepted = this.scrape[0];
        this.sent = this.scrape[1];
        this.rate = this.scrape[2];
        this.time_string = this.scrape[3];
        return this.scrape;
    }
}

// 유웨이
const NAME_1 = "울산대 지역인재";
const PAGE_1 = "http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==";
let ulsan = new Department(PAGE_1, "#Tr_02B02034_002080000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");
let ulsanInfo = ulsan.GetInfo();
document.getElementById("PAGE_1").innerHTML = "<th>" + NAME_1 + "</th><td>" + ulsanInfo[0] + "</td><td>" + ulsanInfo[1] + "</td><td>" + ulsanInfo[2] + "</td><td>" + ulsanInfo[3] + "</td>"

const NAME_2 = "경희대 네오르네상스";
const PAGE_2 = "http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=";
let kyunghee = new Department(PAGE_2, "#Tr_01312_000700000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

const NAME_3 = "고려대 학업우수";
const PAGE_3 = "http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==";
let korea = new Department(PAGE_3, "#Tr_0151_000950000 > td:nth-child", new Array("(3)", "(4)", "(5) > font > b"), "#ID_DateStr > label");

// 진학사
const NAME_4 = "부산대 지역인재";
const PAGE_4 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html";
let pusan = new Department(PAGE_4, "#SelType4F > table > tbody > tr:nth-child(29) > td:nth-child", new Array("(3)", "(4)", "(5)"), "#RatioTime");

const NAME_5 = "한양대 일반";
const PAGE_5 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html";
let hanyang = new Department(PAGE_5, "#SelType4B > table > tbody > tr:nth-child(23) > td:nth-child", new Array("(3)", "(4)", "(5)"), "#RatioTime");

const NAME_6 = "아주대 ACE";
const PAGE_6 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html";
let ajou = new Department(PAGE_6, "#SelType402 > table > tbody > tr:nth-child(21) > td:nth-child", new Array("(2)", "(3)", "(4)"), "#RatioTime");


console.log(ulsan.GetInfo(), kyunghee.GetInfo(), korea.GetInfo(), pusan.GetInfo(), hanyang.GetInfo(), ajou.GetInfo());
