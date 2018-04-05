var cont = document.getElementsByClassName('board-hq')[0].children[0].innerHTML.replace(/<span>(\d+)<\/span>/,'');
var j = 0;
var start = function(){
    trArray = document.getElementById('maincont').children[0].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       td1 = tr.children[2];
       code = td.firstChild.innerHTML;
       name = td1.firstChild.innerHTML;
       console.log("insert into concept values('"+cont+"','"+code+"','"+name+"');");
    }
};
var inter = setInterval(function(){
    start();
    pages = document.getElementById('m-page').children;
    find = false;
    for(var i = 0; i< pages.length; i++){
        if(pages[i].innerHTML == '下一页'){
            pages[i].click();
            find = true;
            break;
        } 
    }
    if(!find){
       clearInterval(inter);  
    } 
},3000);

var cont = document.getElementsByClassName('fl')[0].innerHTML;
var j = 0;
var start = function(){
    trArray = document.getElementById('maincont').children[0].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       td1 = tr.children[2];
       code = td.firstChild.innerHTML;
       name = td1.firstChild.innerHTML;
       console.log("insert into concept values('"+cont+"','"+code+"','"+name+"');");
    }
};
var inter = setInterval(function(){
    start();
    pages = document.getElementById('m-page').children;
    find = false;
    for(var i = 0; i< pages.length; i++){
        if(pages[i].innerHTML == '下一页'){
            pages[i].click();
            find = true;
            break;
        } 
    }
    if(!find){
       clearInterval(inter);  
    } 
},3000);


var cont = document.getElementsByClassName('board-hq')[0].children[0].innerHTML.replace(/<span>(\d+)<\/span>/,'');
var j = 0;
var start = function(){
    trArray = document.getElementById('maincont').children[0].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       td1 = tr.children[2];
       code = td.firstChild.innerHTML;
       name = td1.firstChild.innerHTML;
       console.log("insert into thshy values('"+cont+"','"+code+"','"+name+"');");
    }
};
var inter = setInterval(function(){
    start();
    pages = document.getElementById('m-page').children;
    find = false;
    for(var i = 0; i< pages.length; i++){
        if(pages[i].innerHTML == '下一页'){
            pages[i].click();
            find = true;
            break;
        } 
    }
    if(!find){
       clearInterval(inter);  
    } 
},3000);