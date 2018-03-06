var tds = document.getElementsByClassName('tl');
var codes = [];
for(var i = 0; i < tds.length; i++){
    href = tds[i].children[0].href;
    var code = href.replace(/http:\/\/q.10jqka.com.cn\/thshy\/detail\/code\/(\d+)\//,'$1');
    codes.push("'" + code + "'");
}
console.log(codes.join(','))


var tds = document.getElementsByClassName('tl');
var codes = [];
for(var i = 0; i < tds.length; i++){
    href = tds[i].children[0].href;
    var code = href.replace(/http:\/\/q.10jqka.com.cn\/gn\/detail\/code\/(\d+)\//,'$1');
    codes.push("'" + code + "'");
}
console.log(codes.join(','))




var j = 0;
var codes = [];
var start = function(){
    trArray = document.getElementsByClassName('m-table J-ajax-table')[1].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       td1 = tr.children[6];
       code = td.firstChild.innerHTML;
       net = td1.innerHTML;
       net = net.replace(/亿|万/,'');
       if(parseFloat(net) > 0){
          codes.push("'" + code + "'");  
       }
    }
};
var inter = setInterval(function(){
    start();
    pages = document.getElementsByClassName('m-page J-ajax-page')[0].children;
    find = false;
    for(var i = 0; i< pages.length; i++){
        if(pages[i].innerHTML == '下一页'){
            pages[i].click();
            find = true;
            break;
        } 
    }
    if(!find){
       console.log(codes.join(',')) 
       clearInterval(inter);  
    } 
},3000);

//10 percent

var codes = [];
var start = function(){
    trArray = document.getElementsByClassName('m-table J-ajax-table')[1].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       code = td.firstChild.innerHTML;
       codes.push(code);
    }
};
start();
console.log(codes);