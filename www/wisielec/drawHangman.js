let ctx;

function initCanvas() {
    const c = document.getElementById("hangmanPicture");
    ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.strokeStyle = "gray";
    ctx.lineWidth = 3;
}

function drawHangmanStep(step) {
    switch(step) {
        case 1: // _
            ctx.beginPath();
            ctx.moveTo(20, 280);
            ctx.lineTo(180, 280);
            ctx.stroke();
            break;

        case 2: // |

            ctx.beginPath();
            ctx.moveTo(50, 280);
            ctx.lineTo(50, 20);
            ctx.stroke();
            break;

        case 3: // -
            ctx.beginPath();
            ctx.moveTo(50, 20);
            ctx.lineTo(150, 20);
            ctx.stroke();
            break;

        case 4: 
            ctx.beginPath();
            ctx.moveTo(150, 20);
            ctx.lineTo(150, 50);
            ctx.stroke();
            break;

        case 5: // head
            ctx.beginPath();
            ctx.arc(150, 70, 20, 0, 2 * Math.PI);
            ctx.stroke();
            break;

        case 6: // body
            ctx.beginPath();
            ctx.moveTo(150, 90);
            ctx.lineTo(150, 150);
            ctx.stroke();
            break;

        case 7: // left arm
            ctx.beginPath();
            ctx.moveTo(150, 110);
            ctx.lineTo(120, 130);
            ctx.stroke();
            break;

        case 8: // right arm
            ctx.beginPath();
            ctx.moveTo(150, 110);
            ctx.lineTo(180, 130);
            ctx.stroke();
            break;

        case 9: // left leg
            ctx.beginPath();
            ctx.moveTo(150, 150);
            ctx.lineTo(120, 180);
            ctx.stroke();
            break;

        case 10: // right leg
            ctx.beginPath();
            ctx.moveTo(150, 150);
            ctx.lineTo(180, 180);
            ctx.stroke();
            break;
    }
}
