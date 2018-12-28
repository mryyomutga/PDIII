void setup(){
    digitalWrite(2, HIGH);
    digitalWrite(12, HIGH);
}
void loop(){
    analogWrite(3, 40);
    analogWrite(11, 32);
    analogWrite(9, 40);
    analogWrite(10, 40);
    delay(2000);
    // analogWrite(3, 0);
    // analogWrite(11, 0);
    // analogWrite(9, 0);
    // analogWrite(10, 0);
    // delay(2000);
    digitalWrite(2,  LOW);
    digitalWrite(12, LOW);
    digitalWrite(8,  HIGH);
    digitalWrite(7,  HIGH);
    analogWrite(3, 40);
    analogWrite(11, 32);
    analogWrite(9, 40);
    analogWrite(10, 40);
    // delay(2000);
    // analogWrite(3, 0);
    // analogWrite(11, 0);
    // analogWrite(9, 0);
    // analogWrite(10, 0);
    delay(2000);
    digitalWrite(2,  HIGH);
    digitalWrite(12, HIGH);
    digitalWrite(8,  LOW);
    digitalWrite(7,  LOW);

}

