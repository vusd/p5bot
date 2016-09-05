function bot() {
  this.url = 'https://query.yahooapis.com/v1/public/yql?q=select%20item.forecast%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22wellington%2Cnz%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
  this.weatherData;
  this.temperatures = [];

  this.owl = function(x, y, g, s) {
    push();
    translate(x, y);
    scale(s);  // Set the createCanvas
    stroke(g); // Set the gray value
    strokeWeight(70);
    line(0, -35, 0, -65); // Body
    noStroke();
    fill(255-g);
    ellipse(-17.5, -65, 35, 35); // Left eye dome
    ellipse(17.5, -65, 35, 35);  // Right eye dome
    arc(0, -65, 70, 70, 0, PI);  // Chin
    fill(g);
    ellipse(-14, -65, 8, 8);  // Left eye
    ellipse(14, -65, 8, 8);   // Right eye
    quad(0, -58, 4, -51, 0, -44, -4, -51); // Beak
    pop();
  }

  this.preload = function() {
    this.weatherData = loadJSON(this.url);
  }

  this.setup = function() {
    var results = this.weatherData["query"]["results"]["channel"];
    for(var i=0;i<results.length;i++) {
      var forecast = results[i]["item"]["forecast"]
      var pair = [
        parseInt(forecast["low"], 10), parseInt(forecast["high"], 10)
      ]
      this.temperatures.push(pair)
    }
    /*
    for(i=0;i<10;i++) {
      this.temperatures.push([40, 40]);
    }
    */

    console.log(this.temperatures);
  }

  this.isDone = function() {
    return true;
  }

  this.respond = function() {
    var num_owls = Math.floor(focusedRandom(5, 11, 3, 7));
    var spacing = 400 / num_owls;
    for (i=0; i<num_owls; i++) {
      var xpos = 35 + spacing * i;
      var gray = int(focusedRandom(0, 102, 3))
      var scalar = focusedRandom(0.15, 0.75, 2);
      this.owl(xpos, 220-2*this.temperatures[i][1], gray, scalar);
    }
    var message = "" + num_owls + " day weather owl forecast.";
    return message;
  }
}
