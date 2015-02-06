import processing.core.PVector;
import processing.core.PApplet;
import java.util.ArrayList;

class Particle
{
  private PVector current;
  private PVector speed;
  private ArrayList past;
  private PApplet context;
  private int age;
  private int currentColor;
  private int particleSize;

  
  private static int MAX_AGE = 80;
  private static float GRAVITY = 1;
  private static float DRAG = (float)0.8;
  
  
  Particle(PApplet father, PVector initialPosition, PVector initialSpeed, int c)
  {
    this.current = initialPosition;
    this.speed = initialSpeed;
    this.past = new ArrayList();
    this.context = father;
    this.age = 0;
    this.currentColor = c;
    this.particleSize = 5;
  }
  
  public boolean step()
  {
    if (this.age >= this.MAX_AGE)
    {
      return false;
    }
    
    this.age++;
    this.past.add(new PVector(this.current.x, this.current.y));
      
    this.current.x = this.current.x+this.speed.x;
    this.current.y = this.current.y+this.speed.y;
    this.speed.x = this.speed.x*this.DRAG;
    
    if(this.speed.y < this.GRAVITY) 
    {
      this.speed.y = this.speed.y*this.DRAG+(float)0.1;
    }
    
    return true;
  }
  
  public void draw()
  {
    this.context.strokeWeight(10);
    this.context.stroke(this.currentColor, this.MAX_AGE - this.age);
    this.context.point(this.current.x, this.current.y);
    
    for(int i=this.past.size()-1; i>=0; i--)
    {
      PVector p = (PVector) this.past.get(i);
      int alpha = this.MAX_AGE - this.age - (this.past.size() - i);
      if(alpha > 0)
      {
        this.context.strokeWeight(this.particleSize);
        this.context.stroke(this.currentColor, alpha);
        this.context.point(p.x, p.y);
      }
    }
  }
}
