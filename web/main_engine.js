
/**** JavaScript Game Engine Functions ****/

// Global variables for FPS monitoring
var lastFpsUpdateTime = new Date().getTime();
var frameCount = 0;
var fpsField = getField("fps_counter");

// Object manager to simplify positioning and drawing PDF fields
function GameObject(fieldName, x, y, w, h) {
    this.field = getField(fieldName);
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    
    this.draw = function() {
        if(this.field) {
            this.field.rect = [this.x, this.y, this.x + this.w, this.y + this.h];
        }
    };
}

// Generic Collision Detection
function checkCollision(objA, objB) {
    return (objA.x < objB.x + objB.w &&
            objA.x + objA.w > objB.x &&
            objA.y < objB.y + objB.h &&
            objA.y + objA.h > objB.y);
}

// Keeps an object within screen boundaries
function clamp(obj, minX, maxX, minY, maxY) {
    if (obj.x < minX) obj.x = minX;
    if (obj.x > maxX - obj.w) obj.x = maxX - obj.w;
    if (obj.y < minY) obj.y = minY;
    if (obj.y > maxY - obj.h) obj.y = maxY - obj.h;
}

// Main Loop
function renderGame() {
    try {
        var renderer = getField('renderer');
        
        renderer.display = display.visible;
        draw();
        update();

        // Tracks performance by passing the current timestamp to the FPS counter
        updateFpsCounter(new Date().getTime());
        
        renderer.display = display.hidden;
    } catch (e) { app.alert(e.toString()); }
}

// Initializes the engine once and starts the render loop
function initialize() {
    if (global.initialized) return;
    global.initialized = true;
    
    if (typeof setupGame === "function") setupGame();
    global.gameLoop = app.setInterval('renderGame()', 15);
}

// Calculates and updates the FPS counter on the screen
function updateFpsCounter(currentTime) {

    frameCount++;
    var elapsedTime = currentTime - lastFpsUpdateTime;  // Time passed since the last update

    // Updates the display every 1 second (1000ms) to prevent lag in the PDF
    if (elapsedTime >= 1000) {
        var currentFps = Math.round((frameCount * 1000) / elapsedTime);
        if (fpsField) {
            fpsField.value = "FPS: " + currentFps;
        }
        
        frameCount = 0; // Resets counters for the next 1-second cycle
        lastFpsUpdateTime = currentTime;
    }
}