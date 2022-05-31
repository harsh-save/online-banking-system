/*var typingTimer;                //timer identifier
var doneTypingInterval = 5000;  //time in ms, 5 second for example
var $input = $('#full_name');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
  clearTimeout(typingTimer);
});*/

//var name=document.getElementById("full_name");
//name.addEventListener("blur",blur_function,true);
document.getElementById('full_name').addEventListener('blur',blur_function);
//user is "finished typing," do something
/*function username () {
  
 
  console.log(name)
  var xhttp=new XMLHttpRequest();
  xhttp.open("POST","/username_validate",true);
  xhttp.send();


}*/
function blur_function(){
  var name = document.getElementById('full_name').value;
  var xhr = new XMLHttpRequest();
  xhr.open('GET','username_validate/?name=harsh',true);
  xhr.onload = function(){
    
    console.log(name);
    xhr.send();
  }
  
}


console.log("working");