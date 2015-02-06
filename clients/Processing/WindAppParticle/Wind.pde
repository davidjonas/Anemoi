import io.socket.*;
import org.json.*;

class Wind
{
  //for communicating with the wind server we need a socket 
  SocketIO socket;
  //wind speed & direction             
  // the url server is set in the setup function
  String urlServer = "";
  //turn this to true when connecting to the wifi connection created by the Raspberry Pi 
  
  Wind(boolean accessPointWifiMode)
  {
    if(accessPointWifiMode){
      urlServer = "http://192.168.42.1:8080/";
    }else{
       urlServer = "http://outside.mediawerf.net:8080/";
    }
    //we connect to the wind server
    this.initSockets();
  }
  
  void initSockets(){
  //Sockets
    try
    {
      this.socket = new SocketIO(this.urlServer);
    }
    catch(Exception ex)
    {
      println("Bad URL");
    }
  
    this.socket.connect(new IOCallback() {

        public void onMessage(org.json.JSONObject json, IOAcknowledge ack) {
      }
  

        public void onMessage(String data, IOAcknowledge ack) {
        System.out.println("Server said: " + data);
      }
  

        public void onError(SocketIOException socketIOException) {
        System.out.println("an Error occured");
           socketIOException.printStackTrace();  
      }
  

        public void onDisconnect() {
          System.out.println("Connection terminated.");
          isConnected = false;
          }
  

        public void onConnect() {
          System.out.println("Connection established");
          isConnected = true;
      }
  

        public void on(String event, IOAcknowledge ack, Object... args) {      
  
          if ("windDirectionUpdate".equals(event) && args.length > 0) {                
           try{
               org.json.JSONObject json = (org.json.JSONObject)args[0];
               windDirection = json.getString("value");
               println("windDirection="+windDirection);             
               
       }catch (org.json.JSONException e) {                  
             e.printStackTrace();
             println("Exception on!! "+e.getMessage());
          }           
        }
            
        //speed
       if ("windSpeedUpdate".equals(event) && args.length > 0) {                
           try{
              org.json.JSONObject json = (org.json.JSONObject)args[0];
              windSpeed = json.getInt("value");
              println("windSpeed="+windSpeed);
   
           }catch (org.json.JSONException e) {
             e.printStackTrace();
             println("Exception on!! "+e.getMessage());
          }                   
        }                  
      }
    }
    );  
  }
}
