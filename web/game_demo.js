
/**** Variable and Constants Declarations ****/

const DEFAULT_BALL_Y = 430;
const INITIAL_VELOCITY = 2;
const INITIAL_SCORE = 0;
const MARGIN = 10;

var score = INITIAL_SCORE;
var speed = INITIAL_VELOCITY;
var newGameActive = false;
var playerBar = new GameObject('bar', (CANVAS_WIDTH - BAR_WIDTH) / 2, BAR_BASE_DISTANCE, BAR_WIDTH, BAR_HEIGHT);
var gameBall = new GameObject('ball', 0, 0, BALL_WIDTH, BALL_HEIGHT);
var instruction = this.getField('instruction');
var newGameButton = this.getField('newGameButton');
var scoreArea = this.getField('scoreArea');
var mouseWarning = this.getField('mouseWarning');
var start_screen = this.getField('start_screen');
var renderer = this.getField('renderer');


/**** Functions ****/

// Set up initial ball position and state
function setupGame() {
    global.initialized = false;
    if (newGameActive) {     
        global.initialized = true;
        gameBall.x = randomBallX();
        gameBall.y = DEFAULT_BALL_Y;
        gameBall.w = BALL_WIDTH;
        gameBall.h = BALL_HEIGHT;
        gameBall.dirX = 2;
        gameBall.dirY = 2;    
        speed = INITIAL_VELOCITY;
        score = INITIAL_SCORE;  
        global.mouseX = gameBall.x + gameBall.w / 2;
        mouseWarning.value = "\r\r\r\rMove the mouse here!";
        
        hideStripes();
        startGame();
    } else {
        resetGameView();        
    }        
}

// Helper: Random horizontal position
function randomBallX() {
    return (Math.floor(Math.random() * (CANVAS_WIDTH - BALL_WIDTH - MARGIN * 2)) + MARGIN);
}

// Hide mouse sensors
function hideStripes() {
    for (var fx = 0; fx < CANVAS_WIDTH; fx++) {
        var stripe = this.getField('stripe' + fx);
        if (stripe) stripe.display = display.hidden;    
    }
}

// Draws all game objects on screen
function draw() {
    playerBar.x = global.mouseX - playerBar.w / 2;
    gameBall.draw();
    playerBar.draw();  
    scoreArea.value = "Score: " + score + " / 10";
}

// State and physics update
function update() {
    if (!newGameActive) return; // Prevents game logic (Collisions/Game Over) from running when the game is inactive
    checkCollision();
    gameBall.x += gameBall.dirX * speed;
    gameBall.y += gameBall.dirY * speed;
}

// Physics logic for boundaries and bar
function checkCollision() {    
    if (gameBall.x + (gameBall.dirX * speed) > CANVAS_WIDTH - gameBall.w || 
        gameBall.x + (gameBall.dirX * speed) < 0) {
        gameBall.dirX = -gameBall.dirX;    
    }
    if (gameBall.y + (gameBall.dirY * speed) > CANVAS_BASE + CANVAS_HEIGHT - gameBall.h) {
        gameBall.dirY = -gameBall.dirY;
    } 
    else if (gameBall.y + (gameBall.dirY * speed) < playerBar.y + playerBar.h) {
        if (gameBall.x + gameBall.w > playerBar.x && gameBall.x < playerBar.x + playerBar.w) {
            gameBall.dirY = -gameBall.dirY;             
            gameBall.w *= 0.85; // 
            gameBall.h *= 0.85; // Procedural shrinking
            score++;
            speed *= 1.1;       // Increase speed factor
            
            if (score >= 10) {
                app.alert("Congratulations! You won!");
                endGame();
            }
        } else {
            app.alert("Game Over!");
            endGame();      
        }
    }
}

// Reset loop and flags
function endGame() {
    newGameActive = false;
    global.initialized = false;
    app.clearInterval(global.gameLoop); 
    initialize();
}

// UI state management for menu
function resetGameView() {
    var gameFields = [gameBall.field, playerBar.field, scoreArea, renderer];
    for (var i = 0; i < gameFields.length; i++) {
        if (gameFields[i]) gameFields[i].display = display.hidden;
    }
    
    start_screen.display = display.visible;
    newGameButton.display = display.visible;
    instruction.display = display.visible;
}

// Logic for button interaction
function onNewGameClick() {    
    start_screen.display = display.hidden;
    newGameButton.display = display.hidden;
    instruction.display = display.hidden;    
    gameBall.field.display = display.visible;
    playerBar.field.display = display.visible;
    scoreArea.display = display.visible;    
    newGameActive = true;
    initialize();
}


/**** Main Code ****/
initialize();