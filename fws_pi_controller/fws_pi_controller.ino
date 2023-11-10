float vel = 0,
      sp  = 5.0;



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

  if(millis() - last_time > 2000) {
    set_point = 5.0 + (((float)random(100))/100.0)*5.0;
    last_time = millis();
  }

  return set_point;
}



float calcNextInput(float r, float xs) {
  static float  kp  = 0.0,
                ki  = 0.1;
  static float  err     = 0,
                sum_err = 0;

  err     = r - xs;
  sum_err = sum_err + err;

  return kp*err + ki*sum_err;
}



void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));
  pinMode(23, INPUT);
  pinMode(2, OUTPUT);
}



void loop() {
  sp  = calcNextSetPoint();
  vel = calcNextVelocity(calcNextInput(sp, vel));
  Serial.printf("upper:11.0,lower:0.0,sp:%f,vel:%f\n", sp, vel);
}