
/**** Variable Declarations ****/

const MARGIN = 10;

var posX; 
var posY;
var dirX; 
var dirY; 
var newGameActive = false;
var ball_width_val = BALL_WIDTH;
var ball_height_val = BALL_HEIGHT;

// These variables must be synchronized with the ones created in generator_new.py
var ball = this.getField('ball');
var renderer = this.getField('renderer');
ball.value = "Test"
ball.borderStyle = border.s;

/**** Functions ****/

function initialize() {
    if (global.initialized) return; // Prevent multiple initializations    
    if (newGameActive) {        
        global.initialized = true;
        setupGame();        
        startGame();
    } else {        
        resetGameView(); // Hide all game fields until 'New Game' is pressed
    }
}

// Initialize game parameters
function setupGame() {
    posX = 390;
    posY = 430;
    dirX = 2;
    dirY = 2;
   /** Configure the game here */

}

function startGame() {
    gameLoop = app.setInterval('renderGame()', 15); // Responsible for the infinite game loop
}

// Helper function to render PDF components in real-time
function renderGame() {  
    try {
        if (typeof global.initialized === "undefined") {
            global.initialized = true; // Game initialized
        }
        renderer.display = display.visible;
        draw();
        update();
        renderer.display = display.hidden;
    } catch (e) {
        app.alert(e.toString());
    }
}

// Main game function that dynamically draws all components on screen
function draw() {    
    drawBall();   
}
    // app.alert(ball.rect); 
    // 271, 492, 341, 422
function drawBall() {
    ball.rect = [
        x=(CANVAS_WIDTH - BAR_WIDTH)/2, y=CANVAS_BASE + 30, width=ball_width_val, height=ball_height_val
    ];    
}

function update(){

    /** Update the game components here */

}

function endGame() {
    global.initialized = false;
    app.clearInterval(gameLoop); // Stop game loop
    newGameActive = false;

    /* Reset the parametres here */

    initialize();
}

function resetGameView() {    
    newGameActive = true; // TEMP
    initialize();
}

// Draw component
function drawGenericComponent(component, x, y, width, height) {
    component.rect = [
        x, y, width, height
    ];
}


/**** Main Code ****/
initialize();
