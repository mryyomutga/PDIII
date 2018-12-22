int incomingByte = 0;

void setup(){
    Serial.begin(9600);
}

void loop(){
    if(Serial.available() > 0){
        incomingByte = Serial.read();
        if(incomingByte != 10){
            char buf[1024];
            snprintf(buf, 1024, "OCT:%o ", incomingByte);
            Serial.print(buf);
            snprintf(buf, 1024, "HEX:%x ", incomingByte);
            Serial.print(buf);
            snprintf(buf, 1024, "C:%d", incomingByte);
            Serial.println(buf);
        }
    }
}
