var sentence = "Gone with the wind"
sentence = sentence.toUpperCase();

var lengthSentence = sentence.length;
var coveredSentence = "";

/*covering sentence*/
for(i = 0; i < lengthSentence; i++) {
    if (sentence.charAt(i) == " ") coveredSentence = coveredSentence + " " 
    else coveredSentence = coveredSentence + "-"
}

function write_sentence () {
    document.getElementById("board").innerHTML = coveredSentence;
}

function write_letters () {

    var alphabet = "";

    for(i = 0; i <= 25; i ++) {
        var singleLetter = String.fromCharCode(65 + i);
        alphabet = alphabet + '<span class="letter" onclick="checkAndRewrite('+ (65 + i) + ')" id="' + (65 + i) + '">' + singleLetter + '</span>';
        if((i + 1) % 7  == 0) alphabet = alphabet + '<span style="display: block; clear: both;"></span>';
    }

    document.getElementById("alphabet").innerHTML = alphabet;
}

function start () {

    write_letters();
    write_sentence();
    initCanvas();
}

window.onload = start;


String.prototype.setChar = function(index, newChar) {

    if(index > this.length - 1) {
        return this.toString();
    }
    else {
        return this.substr(0, index) + newChar + this.substr(index + 1);
    }
}

var wrong_guesses = 0;

function checkAndRewrite (nrAscii) {
    
    var correct = false;

    for(i = 0; i < lengthSentence; i++) {  
        if (sentence.charCodeAt(i) == nrAscii) {
            coveredSentence = coveredSentence.setChar(i, String.fromCharCode(nrAscii));
            correct = true;
        }
    }

    /*span's id - ASCII of a letter*/
    let element = document.getElementById(nrAscii);
    element.style.background = "blue";
    element.style.pointerEvents = "none"; 
    element.style.cursor = "default"; 

    if(!correct) {
        wrong_guesses++;
        drawHangmanStep(wrong_guesses);
        setTimeout(isEnd, 100);
    }

    write_sentence();
}

function isEnd () {
    if(wrong_guesses == 10) {
        alert("Game over ;-;");
    }
}


