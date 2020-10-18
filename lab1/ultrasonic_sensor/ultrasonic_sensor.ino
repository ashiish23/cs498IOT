int trigPin = 7;
int echoPin = 6;
int ledPin = 13;
unsigned long duration;
float distance;
char logDuration;
char logDistance;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);    // sets the digital pin 7 as output for Trigger
  pinMode(ledPin, OUTPUT); 
  pinMode(6, INPUT);    // sets the digital pin 6 as input for Echo
}

void loop() {
  digitalWrite(trigPin, HIGH); // trigger sound
  delayMicroseconds(50);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH); // count time to for echo set to high and back to low
  // sprintf(logDuration,"%u microseconds",duration);
  //Serial.println(logDuration);
  Serial.println(duration);
  Serial.println("microseconds");
  // 0.344 millimeters per microsecond (mm/ms) for there and back again, so divide by 2
  distance = (0.344 * duration) / 2; 
  //sprintf(logDistance,"%lu mm away",distance);
  //Serial.println(logDistance);
  Serial.println(distance / 10);
  Serial.println("centimeters");
  Serial.println("-----------");
  if ( (distance/10) <= 15){
    digitalWrite(ledPin, HIGH);
    delay(3000);
    digitalWrite(ledPin, LOW);
  }
  else {
    digitalWrite(ledPin, LOW);
//    delay(3000);            // waits for 3 seconds before polling again
  }
  delay(3000);
//  digitalWrite(trigPin, LOW); // back to low
}
