ArrayList particles;

Wind windSensor;
String statusStr = "";
int windSpeed = 0;
String windDirection = "";
boolean isConnected = false;
int particleMultiplier = 0;
float directionMultiplierX = 0;
float directionMultiplierY = 0;


// the setup is only executed once at the startup 
void setup() {
  
  size(displayWidth, displayHeight);
  colorMode(HSB, 255, 100, 100, 300);
  background(0);
  strokeWeight(1);
  particles = new ArrayList();
  noFill();
  frameRate(60);
  noCursor();
  randomSeed(System.currentTimeMillis());

  //initialize windSensor
  windSensor = new Wind(true);
  
  //initializing graphics
  textSize(18);
  smooth(); 
}


void draw()
{

  background(0);
  
  stroke(255);
  strokeWeight(1);
  bezier(width/2, height/2, width/2, height-(height/4), width/2 - 20, height - 100, width/2 - 20, height - 100);
  
  particleMultiplier = (int) map(windSpeed, 0, 100, 2, 5);
  
  if (windDirection.equals("S"))
  {
    directionMultiplierX = 0;
    directionMultiplierY = 40;
  }
  if (windDirection.equals("N"))
  {
    directionMultiplierX = 0;
    directionMultiplierY = -40;
  }
  if (windDirection.equals("E"))
  {
    directionMultiplierX = 40;
    directionMultiplierY = 0;
  }
  if (windDirection.equals("W"))
  {
    directionMultiplierX = -40;
    directionMultiplierY = 0;
  }
  if (windDirection.equals("SE"))
  {
    directionMultiplierX = 40;
    directionMultiplierY = 40;
  }
  if (windDirection.equals("SW"))
  {
    directionMultiplierX = -40;
    directionMultiplierY = 40;
  }
  if (windDirection.equals("NE"))
  {
    directionMultiplierX = 40;
    directionMultiplierY = -40;
  }
  if (windDirection.equals("NW"))
  {
    directionMultiplierX = -40;
    directionMultiplierY = -40;
  }
  
  
  for(int i=0; i<particleMultiplier; i++)
  {
    particles.add(new Particle(this, new PVector(width/2, height/2), new PVector(random(-50,50)+directionMultiplierX, random(-50,50)+directionMultiplierY), color(255)));
  }
  for (int p=0; p<particles.size(); p++)
  {
    Particle particle = (Particle)particles.get(p); 
    if (particle.step())
    {
      particle.draw();
    }
    else
    {
      particles.remove(particle);
    }
  }
  
  //we choose the text color 
  //fill(200);
  //we print the wind direction and screen on the screen
  //statusStr = (isConnected) ? "connected, wind direction="+windDirection + ", speed="+windSpeed : "not connected";
  //text(statusStr, 20,40);
}

 

