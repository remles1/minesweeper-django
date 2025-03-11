const socket = new WebSocket(`ws://localhost:8000/ws/game/${difficulty_name}`);
let firstClick = true;
let startTime = null;
let timerRunning = false;
let timerInterval = null;
let minesLeft = mine_count;
mines_left_update_counter(minesLeft);
update_seconds_counter(0)


// Function to get a cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

document.querySelector('#new-game-button').addEventListener('click', () => {
    restart_game();
    const stats_div = document.getElementById("stats");
    stats_div.style.display = "none";

});

function restart_game(){
    const message = JSON.stringify({
        type: "new_game",
        message: ""
    })
    socket.send(message)
    firstClick = true;
    startTime = null;
    timerRunning = false;
    minesLeft = mine_count;
    mines_left_update_counter(minesLeft);

    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerInterval = null;
    update_seconds_counter(0);
    document.querySelector('#new-game-button').classList.value = 'face-button face-neutral';
}

let fastMode = getCookie('fastMode') === 'true';

const fastModeButton = document.getElementById('toggleButton');

fastModeButton.textContent = `One button mode: ${fastMode ? "ON" : "OFF"}`;

// Add click event listener
fastModeButton.addEventListener('click', () => {
    // Toggle the boolean value
    fastMode = !fastMode;

    // Update the button text
    fastModeButton.textContent = `One button mode: ${fastMode ? "ON" : "OFF"}`;
    setCookie('fastMode', fastMode, 7);
});


let user_board_dict = {
    "c": "cell-closed",
    "0": "cell-0",
    "f": "cell-flagged",
    "fw": "cell-flagged-wrong",
    "m": "cell-mine",
    "me": "cell-mine-exploded",
    "1": "cell-1",
    "2": "cell-2",
    "3": "cell-3",
    "4": "cell-4",
    "5": "cell-5",
    "6": "cell-6",
    "7": "cell-7",
    "8": "cell-8",
    "pressed": "cell-pressed"
}

socket.onopen = function (e) {
    console.log("WebSocket Connected!");

};

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if(data["type"] === "user_board"){
        let user_board = JSON.parse(data["message"])
        user_board = user_board.map(row =>
            row.map(cell => user_board_dict[cell])
        )
        //console.log(user_board)
        render_user_board(user_board)
        let gameOver = data["over"];
        if (gameOver) {
            timerRunning = false;
            const div = document.querySelector('#board');
            Array.from(div.children).forEach(child => {
                const clonedChild = child.cloneNode(true);
                div.replaceChild(clonedChild, child);
            });

            if(data["won"]){
                mines_left_update_counter(0);
                update_seconds_counter(Math.floor(data["time"]/1000))
                document.querySelector('#new-game-button').classList.value = 'face-button face-happy';
            }
            else {
                document.querySelector('#new-game-button').classList.value = 'face-button face-sad';
            }
            let timeSpent = data["time"] / 1000;
            console.log(timeSpent);
        }
    }
    else if (data["type"] === "game_stats"){
        let message = data["message"];
        let pbs = data["pbs"];
        message = message.replaceAll('\'','\"');
        pbs = pbs.replaceAll('\'','\"');
        console.log(message);
        console.log(pbs);
        let stats_dict = JSON.parse(message);
        pbs = JSON.parse(pbs);
        let stats_order = ["time_spent","tbv","tbv_per_second","ios","rqp"];
        let stats_names = {
            "time_spent": "Seconds",
            "tbv": "3BV",
            "tbv_per_second": "3BV/s",
            "ios": "IOS",
            "rqp": "RQP"
        };

        const stats_div = document.getElementById("stats");
        stats_div.innerHTML = '';

        stats_order.forEach(key => {
            const stat = document.createElement("div");
            stat.classList.value = 'stat';
            stat.innerHTML = `${stats_names[key]}: ${parseFloat(stats_dict[key]).toFixed(3)}`;
            if(pbs.includes(key)){
                const pb = document.createElement("div");
                pb.classList.value = 'pb';
                stat.appendChild(pb);
            }

            stats_div.appendChild(stat)


        } )


        stats_div.style.display = "flex";

    }


};

socket.onclose = function (e) {
    console.log("WebSocket Disconnected!");
};

function render_user_board(user_board) {
    const board = document.getElementById("board");
    board.innerHTML = '';
    for (let i = 0; i < user_board.length; i++) {
        for (let j = 0; j < user_board[0].length; j++) {
            let cell = document.createElement("div");
            cell.id = "id" + i + "-" + j;
            cell.className = "cell " + user_board[i][j];

            cell.addEventListener("mousedown", cellMouseDown);
            cell.addEventListener("mouseup", cellMouseUp);
            cell.addEventListener("mouseover", cellMouseOver);
            cell.addEventListener("mouseleave", cellMouseLeave);
            cell.addEventListener("contextmenu", cellRightClicked);

            board.appendChild(cell)
        }
    }
}

let leftPressed = false;

function cellMouseDown(event) {
    if (event.button !== 0) {
        return;
    }
    leftPressed = true;
    if (event.button === 0 && !this.classList.contains(user_board_dict["f"]) && !this.classList.contains(user_board_dict["0"])) {
        this.classList.add(user_board_dict["pressed"]);
    }

}

function cellMouseOver(event) {
    event.preventDefault();
    if (leftPressed) {
        this.classList.add(user_board_dict["pressed"]);
    }
}

function cellMouseLeave(event) {
    event.preventDefault();
    if (this.classList.contains(user_board_dict["pressed"])) {
        this.classList.remove(user_board_dict["pressed"]);
    }
}

function cellMouseUp(event) {
    if (event.button !== 0) {
        return;
    }
    leftPressed = false;

    if (this.classList.contains(user_board_dict["0"]) || this.classList.contains(user_board_dict["f"] )) {
        return;
    }

    if (fastMode && this.classList.contains(user_board_dict["c"]) || this.classList.contains(user_board_dict["f"])) {
        if(this.classList.contains(user_board_dict["c"])){
            minesLeft--;
        }
        if (this.classList.contains(user_board_dict["f"])){
            minesLeft++;
        }
        mines_left_update_counter(minesLeft);
        const message = JSON.stringify({
            type: "r_click",
            message: this.id.replace(/^id/, "")
        })
        socket.send(message)
    } else {
        const message = JSON.stringify({
            type: "l_click",
            message: this.id.replace(/^id/, "")
        })
        socket.send(message)
    }


    if (!fastMode && firstClick) {
        startTime = performance.now()
        timerRunning = true;
        timer();
        firstClick = false;
    }
}

function cellRightClicked(event) {
    event.preventDefault();
    if (!this.classList.contains(user_board_dict["0"])) {
        if (!fastMode) {
            if(this.classList.contains(user_board_dict["c"])){
                minesLeft--;
            }
            if (this.classList.contains(user_board_dict["f"])){
                minesLeft++;
            }
            mines_left_update_counter(minesLeft);
            const message = JSON.stringify({
                type: "r_click",
                message: this.id.replace(/^id/, "")
            })
            socket.send(message)
        } else {
            const message = JSON.stringify({
                type: "l_click",
                message: this.id.replace(/^id/, "")
            })
            socket.send(message)
        }

        if (fastMode && firstClick) {
            startTime = performance.now()
            timerRunning = true;
            timer();
            firstClick = false;
        }

    }
}


function timer() {
    let seconds = 0;
    timerInterval=setInterval(()=>{
        if (!timerRunning) {
            return;
        }
        seconds += 1;
        update_seconds_counter(seconds)
    },1000);
}

function update_seconds_counter(seconds){
    let seconds_as_digits = convertNumberTo3Digits(seconds);
        for(let i = 0; i < 3; i++){
            let digit_div = document.getElementById(`sc_d${i}`)
            digit_div.classList.value = `digit digit-${seconds_as_digits[i]}`;
        }
}

function mines_left_update_counter(mine_count){
    let mines_left_as_digits = convertNumberTo3Digits(mine_count);
    for(let i = 0; i < 3; i++){
            let digit_div = document.getElementById(`mlc_d${i}`)
            digit_div.classList.value = `digit digit-${mines_left_as_digits[i]}`;
    }
}

function convertNumberTo3Digits(number){
    if (number > 999){
        return ['9','9','9'];
    }
    let formatted = number.toString().padStart(3,'0');
    return formatted.split('');
}