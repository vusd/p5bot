var rndSeed;

var bot;
var renderReady = false;

function preload() {
  bot = new bot();
  if (bot.preload != null) {
    bot.preload();
  }
}

function setup () {
  var main_canvas;
    
  if (bot.preferredRenderer != null) {
      main_canvas = createCanvas(440, 220, bot.preferredRenderer());
  } else {
      main_canvas = createCanvas(440, 220);
  }

  main_canvas.parent('canvasContainer');

  rndSeed = random(1024);
  if (bot.setup != null) {
    bot.setup();
  }
}

function keyTyped() {
  if (key == '!') {
    saveBlocksImages();
  }
  else if (key == '@') {
    saveBlocksImages(true);
  }
}

function reportRenderReady() {
  finalDiv = createDiv('(done drawing)');
  finalDiv.id("render_ready")
}

function draw() {
  if(renderReady) {
    return;
  }
  background(204);
  // randomSeed(0);
  resetFocusedRandom(rndSeed);
  message = bot.respond();
  var text = select('#tweet_text');
  text.html(message);
  if(renderReady == false) {
    if(bot.isDone()) {
      reportRenderReady();
      renderReady = true;
      // turn off animation
      noLoop();
    }
  }
}
