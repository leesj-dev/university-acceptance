scrapeElement = function(link, pathArray) {
    let xhr = new XMLHttpRequest();
    let arr = [];
    xhr.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == this.DONE) {  // 서버 상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때
            let dom = new DOMParser().parseFromString(xhr.responseText, 'text/html');
            for (let i = 0; i < pathArray.length; i++) {
                arr[i] = dom.querySelector(pathArray[i]).innerHTML;
            }
        }
    };
    xhr.open("GET", "https://proxy.cors.sh/" + link, true);  // CORS 위반 때문에 proxy server로 우회.
    xhr.send();
    return arr;
}

class Department {
    constructor(page, path, plist, timestamp) {
        this.page = page;
        this.pathArray = [path + plist[0], path + plist[1], path + plist[2], timestamp];
    }
    getInfo() {
        return scrapeElement(this.page, this.pathArray);
    }
}

updateHTML = function(i, name, dep) {
    let id = "NAME" + String(i + 1);
    let depInfo = dep.getInfo();
    document.getElementById(id).innerHTML = "<th>" + name + "</th><td>" + depInfo[0] + "</td><td>" + depInfo[1] + "</td><td>" + depInfo[2] + "</td><td>" + depInfo[3] + "</td>";
}

// 유웨이
const NAME1 = "울산대 지역인재";
const PAGE1 = "http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==";
let dep1 = new Department(PAGE1, "#Tr_02B02034_002080000 > td:nth-child", ["(3)", "(4)", "(5) > font > b"], "#ID_DateStr > label");

const NAME2 = "경희대 네오르네상스";
const PAGE2 = "http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=";
let dep2 = new Department(PAGE2, "#Tr_01312_000700000 > td:nth-child", ["(3)", "(4)", "(5) > font > b"], "#ID_DateStr > label");

const NAME3 = "고려대 학업우수";
const PAGE3 = "http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==";
let dep3 = new Department(PAGE3, "#Tr_0151_000950000 > td:nth-child", ["(3)", "(4)", "(5) > font > b"], "#ID_DateStr > label");

// 진학사
const NAME4 = "부산대 지역인재";
const PAGE4 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html";
let dep4 = new Department(PAGE4, "#SelType4F > table > tbody > tr:nth-child(29) > td:nth-child", ["(3)", "(4)", "(5)"], "#RatioTime");

const NAME5 = "한양대 일반";
const PAGE5 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html";
let dep5 = new Department(PAGE5, "#SelType4B > table > tbody > tr:nth-child(23) > td:nth-child", ["(3)", "(4)", "(5)"], "#RatioTime");

const NAME6 = "아주대 ACE";
const PAGE6 = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html";
let dep6 = new Department(PAGE6, "#SelType402 > table > tbody > tr:nth-child(21) > td:nth-child", ["(2)", "(3)", "(4)"], "#RatioTime");

const names = [NAME1, NAME2, NAME3, NAME4, NAME5, NAME6];
let deps = [dep1, dep2, dep3, dep4, dep5, dep6];
for (let i = 0; i < names.length; i++) {
    updateHTML(i, names[i], deps[i]);
}

