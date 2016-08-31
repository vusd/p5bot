var rndSeed;

var bot;
var renderReady = false;

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

function reportRenderReady() {
  finalDiv = createDiv('(render ready)');  
  finalDiv.id("render_ready")
}

function draw() {
  background(204);
  // randomSeed(0);
  resetFocusedRandom(rndSeed);
  message = bot.respond();
  var text = select('#tweet_text');
  text.html(message);
  if(renderReady == false) {
    reportRenderReady();
    renderReady = true;
  }
}

if (typeof debug_interface !== 'undefined') {
  // Your variable is undefined
  var configProfile = {
    "profile": {"screenName": 'starbucks'},
    "domId": 'tweetExamples',
    "maxTweets": 5,
    "enableLinks": false,
    "showUser": false,
    "showTime": false,
    "showImages": true,
    "showInteraction": false,
    "lang": 'en'
  };
  twitterFetcher.fetch(configProfile);
}

