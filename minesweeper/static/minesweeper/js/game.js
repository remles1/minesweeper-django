const socket = new WebSocket(`ws://localhost:8000/ws/game/${difficulty_name}`);
let firstClick = true;
let startTime = null;
let timerRunning = false;

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


let fastMode = getCookie('fastMode') === 'true';


const fastModeButton = document.getElementById('toggleButton');

fastModeButton.textContent = `Fast Mode: ${fastMode ? "ON" : "OFF"}`;

// Add click event listener
fastModeButton.addEventListener('click', () => {
    // Toggle the boolean value
    fastMode = !fastMode;

    // Update the button text
    fastModeButton.textContent = `Fast Mode: ${fastMode ? "ON" : "OFF"}`;
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
    let user_board = JSON.parse(data["message"])
    user_board = user_board.map(row =>
        row.map(cell => user_board_dict[cell])
    )
    //console.log(user_board)
    render_user_board(user_board)
    let gameOver = data["over"];
    if (gameOver) {
        timerRunning = false;
        let timeSpent = data["time"] / 1000;
        console.log(timeSpent);
        document.getElementById("timer").innerHTML = timeSpent.toString();
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

    if (this.classList.contains(user_board_dict["0"])) {
        return;
    }

    if (fastMode && this.classList.contains(user_board_dict["c"]) || this.classList.contains(user_board_dict["f"])) {
        const message = JSON.stringify({
            btn: "r",
            message: this.id.replace(/^id/, "")
        })
        socket.send(message)
    } else {
        const message = JSON.stringify({
            btn: "l",
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
        this.classList.toggle(user_board_dict["c"]);
        this.classList.toggle(user_board_dict["f"]);

        if (!fastMode) {
            const message = JSON.stringify({
                btn: "r",
                message: this.id.replace(/^id/, "")
            })
            socket.send(message)
        } else {
            const message = JSON.stringify({
                btn: "l",
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
    if (!timerRunning) {
        return;
    }
    const now = performance.now();
    const elapsed = (now - startTime) / 1000;
    document.getElementById("timer").textContent = elapsed.toFixed(3);
    requestAnimationFrame(timer); // Continuously update the timer
}

