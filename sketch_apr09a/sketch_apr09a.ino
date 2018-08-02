int data;


void setup() {
  Serial.begin(9600);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  }


void forward()
  {
  digitalWrite(5,HIGH);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,HIGH);
  Serial.println("forward");
  }


void right()
  {
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,HIGH);
  Serial.println("right");
  }


void left()
  {
  digitalWrite(5,HIGH);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  Serial.println("left");
  }


void stop()
  {
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  Serial.println("stop");
  }

void loop() 
  {
  while (Serial.available())
    {
    data = Serial.read();
    }


  if (data == '0')
  left();

  else if (data == '1')
  right();

  else if (data == '2')
  forward();

  else
  stop();
  }
