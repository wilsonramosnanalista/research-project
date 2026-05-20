
/**** Variable and Constants Declarations ****/

var player = new GameObject('farmer_worker', (CANVAS_WIDTH-FARME_WORKER_WIDTH)/4, CANVAS_BASE+100, FARME_WORKER_WIDTH, FARME_WORKER_HEIGHT);
var apple = new GameObject('apple', 0, 0, APPLE_WIDTH, APPLE_HEIGHT);
var score_field = getField("score_field");
var score = 0;


/**** Functions ****/

// Initializes game state, positions apple, focuses input, and resets score
function setupGame() {
    spawnApple();
    getField('keyboard_input').setFocus();
    score_field.value = "0";
}

// Randomly positions the apple within valid play area
function spawnApple() {
    apple.x = Math.floor(Math.random() * (CANVAS_WIDTH - apple.w - 20)) + 10;
    apple.y = Math.floor(Math.random() * (PAGE_HEIGHT - CANVAS_BASE - 110)) + CANVAS_BASE + 50;
}

// Draws all game objects on screen
function draw() {
    player.draw();
    apple.draw();
}

// Updates game logic
function update() {
    if (checkCollision(player, apple)) {        
        score++;
        score_field.value = score.toString();
        if (score >= 5) {
            app.alert("Congratulations! You collected 5 apples. You won!");
            endGame();
        }
        spawnApple();
    }
}

// Reset loop and flags
function endGame() {
    score = 0;
    global.initialized = false;
    app.clearInterval(global.gameLoop); 
    initialize();
}

// Handles keyboard input to move the player and keeps it within bounds
function handle_input(event) {
    var key = event.change.toLowerCase();
    event.target.value = ""; 

    if (key == 'a') player.x -= 10;
    if (key == 'd') player.x += 10;
    if (key == 'w') player.y += 10;
    if (key == 's') player.y -= 10;

    clamp(player, 0, CANVAS_WIDTH, CANVAS_BASE + 20, PAGE_HEIGHT);
}


/**** Main Code ****/

initialize();