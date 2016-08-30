function dribnet_bot() {
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

  this.setup = function() {
  }

  this.respond = function() {
    var num_owls = 0;
    var spacing = focusedRandom(20, 60, 4);
    for (var i = 35; i < width - 40; i += spacing) {
      var gray = int(focusedRandom(0, 102, 3))
      var scalar = focusedRandom(0.15, 0.75, 2);
      this.owl(i, 160, gray, scalar);
      num_owls = num_owls + 1;
    }
    var message = "Here are " + num_owls + " owls.";
    return message;
  }
}
