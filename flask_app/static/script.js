function over(element){
    element.style.backgroundColor= "black";
    element.style.color = "rgb(255,255,255)";
}

function out(element){
    element.style.backgroundColor = "rgb(255,255,255)";
    element.style.color = "black";
}

var id = null;

window.onload = function myMove() {
    var elem = document.getElementById("myAnimation");
    var pos = 0;
    clearInterval(id);
    id = setInterval(frame, 5);
    function frame(){
        if (pos==150) {
        clearInterval(id);
        } 
        else {
        pos++;
        elem.style.top = pos + 'px';
        elem.style.left = pos + 'px';
        }
    }
}