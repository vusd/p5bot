var rndSeed;

var bot;

function setup () {
  var main_canvas = createCanvas(440, 220);
  main_canvas.parent('canvasContainer');

  rndSeed = random(1024);
  bot = new dribnet_bot();
  bot.setup();
}

function keyTyped() {
  if (key == '!') {
    saveBlocksImages();
  }
  else if (key == '@') {
    saveBlocksImages(true);
  }
}

function draw() {
  background(204);
  // randomSeed(0);
  resetFocusedRandom(rndSeed);
  message = bot.respond();
  var text = select('#tweet_text');
  text.html(message);
}
