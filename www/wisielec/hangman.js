const categories = {
    "Books" : ["Gone with the wind", "Dune", "The Hobbit", "Pride and Prejudice", "The Godfather"],
    "Food" : ["Strawberry", "Watermelon", "Salmon", "Pancakes"],
    "Bands" : ["Palaye royale","Queen", "Aerosmith", "The doors", "Bon Jovi", "Nirvana", "My chemical romance", "Faith no more", "Guns n roses"]
}

let options = categories["Bands"];
let randomChoice;
let sentence;
let lengthSentence;
let coveredSentence = "";
let wrong_guesses = 0;

function write_sentence () {
    document.getElementById("board").innerHTML = coveredSentence;
}

function write_letters () {

    var alphabet = "";

    for(i = 0; i <= 25; i ++) {
        var singleLetter = String.fromCharCode(65 + i);
        alphabet = alphabet + '<span class="letter" onclick="checkAndRewrite('+ (65 + i) + ')" id="' + (65 + i) + '">' + singleLetter + '</span>';
    }

    document.getElementById("alphabet").innerHTML = alphabet;
}

function initGame () {
    randomChoice = Math.floor(Math.random() * options.length);
    sentence = options[randomChoice].toUpperCase(); 

    lengthSentence = sentence.length;
    coveredSentence = "";


    for(i = 0; i < lengthSentence; i++) {
        if (sentence.charAt(i) == " ") coveredSentence = coveredSentence + " " 
        else coveredSentence = coveredSentence + "-"
    }
    wrong_guesses = 0;
    write_sentence();
}

function start () {
    initCanvas();
    const resumed = loadGameState();
    if (!resumed) {
        initGame();
        write_letters();
    }
}

window.onload = () => {
    start();
    document.getElementById("reloadGame").addEventListener("click", () => {
        localStorage.removeItem("hangmanState"); 
        initCanvas();
        initGame();
        write_letters();
    });
}


String.prototype.setChar = function(index, newChar) {

    if(index > this.length - 1) {
        return this.toString();
    }
    else {
        return this.substr(0, index) + newChar + this.substr(index + 1);
    }
}


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
    }
    
    saveGameState();

    setTimeout(isEnd, 100);

    write_sentence();
}

function isEnd () {
    if(wrong_guesses == 10) {
        alert("Game over ;-;");
        localStorage.removeItem("hangmanState");
        setTimeout(() => start(), 500); 
    }
    if(coveredSentence == sentence) {
        alert("Congratulations!")
        localStorage.removeItem("hangmanState");
        setTimeout(() => start(), 500); 
    }
}

function saveGameState() {
    const state = {
        sentence: sentence,
        coveredSentence: coveredSentence,
        wrong_guesses: wrong_guesses,
        usedLetters: Array.from(document.querySelectorAll(".letter"))
            .filter(el => el.style.pointerEvents === "none")
            .map(el => parseInt(el.id))
    };
    localStorage.setItem("hangmanState", JSON.stringify(state));
}

function loadGameState() {
    const saved = localStorage.getItem("hangmanState");
    if (!saved) return false;

    const state = JSON.parse(saved);

    sentence = state.sentence;
    lengthSentence = sentence.length;
    coveredSentence = state.coveredSentence;
    wrong_guesses = state.wrong_guesses;

    write_sentence();
    write_letters();

    state.usedLetters.forEach(ascii => {
        const el = document.getElementById(ascii);
        if (el) {
            el.style.background = "blue";
            el.style.pointerEvents = "none";
            el.style.cursor = "default";
        }
    });

    for (let i = 1; i <= wrong_guesses; i++) {
        drawHangmanStep(i);
    }

    return true;
}
