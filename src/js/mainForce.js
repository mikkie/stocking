var codes = [];
var j = 0;
var start = function(){
    trArray = document.getElementById('S_HQ_CONTAINER_ypuaz').firstChild.children[1].children;
    for(var i = 0; i < trArray.length; i++){
       tr = trArray[i];
       td = tr.children[0];
       code = td.firstChild.innerHTML;
       code = code.replace(/sh|sz/g,'');
       codes.push("'" + code + "'");
    }
};
var inter = setInterval(function(){
    start();
    document.getElementsByClassName('pages')[0].lastChild.click();
    j++;
    if(j > 41){
       console.log('[' + codes.join(',') + ']');
       clearInterval(inter);  
    } 
},3000);


