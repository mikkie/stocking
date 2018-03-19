var cont = document.getElementsByClassName('board-hq')[0].children[0].innerHTML.replace(/<span>(\d+)<\/span>/,'');
var j = 0;
var res = [];
var start = function(){
    trArray = document.getElementById('maincont').children[0].children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[1];
       td1 = tr.children[2];
       code = td.firstChild.innerHTML;
       name = td1.firstChild.innerHTML;
       if(/^6/.test(code)){
       	  res.push(code + '.XSHG');
       }
       else{
       	  res.push(code + '.XSHE');
       } 
    }
};
var inter = setInterval(function(){
    try{
        start();
    }
    catch(e){
    }
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
        console.log(cont);  
        if(res.length <= 100){
          console.log(res);
        }
        else{
          var step = 100;
          var begin = 0;
          var end = begin + step;
          if(end > res.length){
             end = res.length;
          }
          while(begin < res.length){
             var temp = res.slice(begin,end);
             console.log(temp);  
             begin = end;
             end = begin + step; 
             if(end > res.length){
                end = res.length;
             }
          }   
        }
     } 
},3000);