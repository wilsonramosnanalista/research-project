
/**** Variable and Constants Declarations ****/

const DEFAULT_BALL_Y = 650;
const INITIAL_VELOCITY = 0.85;
const MARGIN = 20;
const GAME_X = 65;
const GAME_Y = CANVAS_BASE - 78;
const GAME_WIDTH = CANVAS_WIDTH;
const GAME_HEIGHT = CANVAS_HEIGHT;
const GAME_RIGHT = GAME_X + GAME_WIDTH;
const GAME_TOP = GAME_Y + GAME_HEIGHT;

var speed = INITIAL_VELOCITY;
var gameBall = new GameObject('ball', 0, 0, BALL_WIDTH, BALL_HEIGHT);
var playerBar = new GameObject('bar', 0, BAR_BASE_DISTANCE, BAR_WIDTH, BAR_HEIGHT);
var renderer = this.getField('renderer');


/**** Functions ****/

// Performs the initial game setup, configuring objects, state variables, and starting conditions
function setupGame() {
    gameBall.x = randomBallX();
    gameBall.y = DEFAULT_BALL_Y;
    gameBall.dirX = 2;
    gameBall.dirY = 2;    
    speed = INITIAL_VELOCITY; 
    global.mouseX = GAME_X + (GAME_WIDTH / 2);
    hideStripes();
}

// Helper: Random X within boundaries
function randomBallX() {
    return GAME_X + Math.floor(Math.random() * (GAME_WIDTH - gameBall.w));
}

// Hide sensors
function hideStripes() {
    for (var fx = 0; fx < 197; fx++) {
        var stripe = this.getField('stripe' + fx);
        if (stripe) stripe.display = display.hidden;    
    }
}

// Draws all game objects on screen
function draw() {    
    playerBar.x = getClampedBarX();
    gameBall.draw();
    playerBar.draw();
}

// Updates game logic
function update() {
    checkCollision();
    gameBall.x += gameBall.dirX * speed;
    gameBall.y += gameBall.dirY * speed;
}

// Mouse Clamping Logic
function getClampedBarX() {
    var targetX = global.mouseX - (playerBar.w / 2);
    if (targetX < GAME_X) targetX = GAME_X;
    if (targetX > GAME_RIGHT - playerBar.w) targetX = GAME_RIGHT - playerBar.w;
    return targetX;
}

// Physics logic for boundaries and bar
function checkCollision() {
    if (gameBall.x + (gameBall.dirX * speed) + gameBall.w + 3 > GAME_RIGHT || 
        gameBall.x + (gameBall.dirX * speed) < GAME_X) {
        gameBall.dirX = -gameBall.dirX;
    }
    if (gameBall.y + (gameBall.dirY * speed) + gameBall.h + 3 >= GAME_TOP) {
        gameBall.dirY = -gameBall.dirY;
    } 
    else if (gameBall.y + (gameBall.dirY * speed) < playerBar.y + playerBar.h) {
        if (gameBall.x + gameBall.w > playerBar.x && gameBall.x < playerBar.x + playerBar.w) {
            gameBall.dirY = -gameBall.dirY;
        } else if (gameBall.y + (gameBall.dirY * speed) < GAME_Y) {
            endGame();
        }
    } 
    else if (gameBall.y + (gameBall.dirY * speed) < GAME_Y) {
        endGame();
    }
}

// Reset loop and flags
function endGame() {
    global.initialized = false;
    app.clearInterval(global.gameLoop);
    initialize();
}


/**** Main Code ****/
app.clearInterval("Inicialize");
initialize();