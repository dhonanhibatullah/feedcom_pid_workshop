uint64_t  runtime   = 0;
float     cnt       = 1.0,
          error     = 0.0;



float calcNextVelocity(float u) {
  /* States and values */
  static float  v     = 0,
                v_dot = 0,
                b     = 1,
                m     = 1,
                dt    = 0.01;

  /* Calculate next state */
  v_dot = u/m - (b/m)*v;
  v     = v + v_dot*dt;
  delay(10);

  return v;
}



float calcNextSetPoint() {
  static uint64_t last_time = 0;
  static float    set_point = 5.0;

  if(millis() - last_time > 3000) {
    set_point = 5.0 + (((float)random(100))/100.0)*5.0;
    last_time = millis();
  }

  return set_point;
}



void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));
  pinMode(23, INPUT);
  pinMode(2, OUTPUT);

  runtime = millis();
}



void loop() {
  /* Print tracking view */
  float vel = 0.0,
        sp  = calcNextSetPoint();
  Serial.printf("upper:11.0,lower:0.0,sp:%f,", sp);

  if(digitalRead(23) == 1) {
    digitalWrite(2, HIGH);
    vel = calcNextVelocity(17);
    Serial.printf("v:%f\n", vel);
  }

  else {
    digitalWrite(2, LOW);
    vel = calcNextVelocity(0);
    Serial.printf("v:%f\n", vel);
  }

  /* Calculate cumulative error */
  error = error*cnt/(cnt + 1.0) + fabs(sp - vel)/(cnt + 1.0);
  cnt   = cnt + 1.0;

  /* Stop running */
  if(millis() - runtime > 20000) {
    Serial.printf("[TOTAL ERROR] : %f\n", error);
    while(1);
  }
}