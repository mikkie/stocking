var codes = [];
var j = 0;
var start = function(){
    trArray = document.getElementById('J-ajax-main').children[1].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       code = td.firstChild.innerHTML;
       codes.push("'" + code + "'");
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


