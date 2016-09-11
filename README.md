The current bot.js API

```javascript

function bot() {
  // Optional.
  this.preload = function() {
    // same as ps.j5 preload()
    //
    // call loadJSON, loadImage, etc. here.
    // variables will be ready by setup
  }

  // Optional.
  this.setup = function() {
    // same as ps.j5 setup()
  }

  // Required.
  this.respond = function() {
    // similar to ps.j5 draw()
    //
    // do all of your drawing here
    // at the end, return a string of text to display
  }

  // Optional. Default is true.
  this.isDone = function() {
    // return true if your bot is done responding
    // otherwise, return false to get more time
  }

  // Optional. Default is P2D.
  this.preferredRenderer = function() {
      return P2D; // Either P2D or WEBGL;
  }
}

```