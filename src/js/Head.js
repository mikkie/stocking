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