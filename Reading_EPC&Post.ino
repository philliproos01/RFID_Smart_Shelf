#include <SoftwareSerial.h>
#include <WiFiNINA.h>

SoftwareSerial softSerial(2, 3); //RX, TX

#include "SparkFun_UHF_RFID_Reader.h" //Library for controlling the M6E Nano module
RFID nano; //Create instance

char ssid[] = "Home135";
char pass[] = "135hillsdale";

int status = WL_IDLE_STATUS;

char server[] = "pcr.bounceme.net";

String postData;
String postVariable = "temp=";

String postData1;
String postVariable1 = "ppm=";

String postData2;
String postVariable2 = "pressure=";

String postData3;
String postVariable3 = "tvoc=";
String postEPC;

float tag;

WiFiClient client;

void setup()
{
  Serial.begin(38400);
  while (!Serial); //Wait for the serial port to come online
   
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  IPAddress gateway = WiFi.gatewayIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  
  if (setupNano(38400) == false) //Configure nano to run at 38400bps
  {
    Serial.println(F("Module failed to respond. Please check wiring."));
    while (1); //Freeze!
  }

 

  

  beginWork();
}

void loop()
{
    while (status != WL_CONNECTED) {
    Serial.print("Connection lost, attempting to re-connect to Network named: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  
  if (nano.check() == true) //Check to see if any new data has come in from module
  {
    byte responseType = nano.parseResponse(); //Break response into tag ID, RSSI, frequency, and timestamp

    if (responseType == RESPONSE_IS_KEEPALIVE)
    {
      Serial.println(F("Scanning"));
    }
    else if (responseType == RESPONSE_IS_TAGFOUND)
    {
      //If we have a full record we can pull out the fun bits
      int rssi = nano.getTagRSSI(); //Get the RSSI for this tag read

      long freq = nano.getTagFreq(); //Get the frequency this tag was detected at

      long timeStamp = nano.getTagTimestamp(); //Get the time this was read, (ms) since last keep-alive message

      byte tagEPCBytes = nano.getTagEPCBytes(); //Get the number of bytes of EPC from response

      Serial.print(F(" rssi["));
      Serial.print(rssi);
      Serial.print(F("]"));

      Serial.print(F(" freq["));
      Serial.print(freq);
      Serial.print(F("]"));

      Serial.print(F(" time["));
      Serial.print(timeStamp);
      Serial.print(F("]"));

      //Print EPC bytes, this is a subsection of bytes from the response/msg array
      Serial.print(F(" epc["));
      for (byte x = 0 ; x < tagEPCBytes ; x++)
      {
        if (nano.msg[31 + x] < 0x10) Serial.print(F("0")); //Pretty print
        Serial.print(nano.msg[31 + x], HEX);
        tag = (nano.msg[31 + x], HEX);
        Serial.print(F(" "));
      }
      Serial.print(F("]"));

      Serial.println();
    }
    else if (responseType == ERROR_CORRUPT_RESPONSE)
    {
      Serial.println("Bad CRC");
    }
    else
    {
      //Unknown response
      Serial.print("Unknown error");
    }
  }

   if (client.connect(server, 80)) {
    client.println("POST /test/RFID/post.php HTTP/1.2");
    client.println("Host: pcr.bounceme.net");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    
    /*
    Serial.print(F(" epc["));
    byte tagEPCBytes = nano.getTagEPCBytes();
    for (byte x = 0 ; x < tagEPCBytes ; x++)
      {
      if (nano.msg[31 + x] < 0x10) Serial.print(F("0")); //Pretty print
      //postEPC = "1";
      Serial.print(nano.msg[31 + x], HEX);
      Serial.print(F(" "));
      }
      Serial.print(F("]"));

      Serial.println();*/
      //postData = postVariable + postEPC;
     
      //tag = (temperatureC * 9.0 / 5.0) + 32.0;
      

      postData = postVariable + " epc[" + tag + "]";
      
      
      client.println(postData.length());
      client.println();
      client.print(postData);
    /*client.println(postData1.length());
    client.println();
    client.print(postData1);
    client.println(postData2.length());
    client.println();
    client.print(postData2);
    client.println(postData3.length());
    client.println();
    client.print(postData3);*/
    
  }


  
}

//Gracefully handles a reader that is already configured and already reading continuously
//Because Stream does not have a .begin() we have to do this outside the library
boolean setupNano(long baudRate)
{
  nano.begin(softSerial); //Tell the library to communicate over software serial port

  //Test to see if we are already connected to a module
  //This would be the case if the Arduino has been reprogrammed and the module has stayed powered
  softSerial.begin(baudRate); //For this test, assume module is already at our desired baud rate
  while (softSerial.isListening() == false); //Wait for port to open

  //About 200ms from power on the module will send its firmware version at 115200. We need to ignore this.
  while (softSerial.available()) softSerial.read();

  nano.getVersion();

  if (nano.msg[0] == ERROR_WRONG_OPCODE_RESPONSE)
  {
    //This happens if the baud rate is correct but the module is doing a ccontinuous read
    nano.stopReading();

    Serial.println(F("Module continuously reading. Asking it to stop..."));

    delay(1500);
  }
  else
  {
    //The module did not respond so assume it's just been powered on and communicating at 115200bps
    softSerial.begin(115200); //Start software serial at 115200

    nano.setBaud(baudRate); //Tell the module to go to the chosen baud rate. Ignore the response msg

    softSerial.begin(baudRate); //Start the software serial port, this time at user's chosen baud rate

    delay(250);
  }

  //Test the connection
  nano.getVersion();
  if (nano.msg[0] != ALL_GOOD) return (false); //Something is not right

  //The M6E has these settings no matter what
  nano.setTagProtocol(); //Set protocol to GEN2

  nano.setAntennaPort(); //Set TX/RX antenna ports to 1

  return (true); //We are ready to rock
}

void beginWork() {
  nano.setRegion(REGION_NORTHAMERICA); //Set to North America

  nano.setReadPower(1000); //5.00 dBm. Higher values may caues USB port to brown out
  //Max Read TX Power is 27.00 dBm and may cause temperature-limit throttling

  Serial.println(F("Press a key to begin scanning for tags."));
  while (!Serial.available()); //Wait for user to send a character
  Serial.read(); //Throw away the user's character

  nano.startReading(); //Begin scanning for tags
  
}
