#define R 7
#define G 11
#define B 13
#define P A5
#define COLORS_LEN 7
#define RAISE_DELAY 30
#define FALL_DELAY 40
#define CONFIGURE_COD 100

int colors[COLORS_LEN][3] = {{0, 0, 255}, {0, 255, 0}, {0, 255, 255}, {255, 0, 0}, {255, 0, 255}, {255, 255, 0}, {255, 255, 255}};
float baseResistance[COLORS_LEN] = {1015.0, 1015.0, 1018, 1018.5, 1021, 1020.5, 1021.5}; // Массив для хранения базовых значений светимости
int iterations;
float luxValue;


void onLight() {
  setLight(255, 255, 255);
}


void offLight() {
  setLight(0, 0, 0);
}


void setLight(int r, int g, int b) {
  analogWrite(R, r);
  analogWrite(G, g);
  analogWrite(B, b);
}


void setup() {
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(P, INPUT);
  Serial.begin(9600);
}


void loop() {
  if (!Serial.available()) return;
  int cod = Serial.readString().toInt();
  if (cod == CONFIGURE_COD)
  {
    printBaseResistens();
    Serial.println(1);
    return;
  }
  int iterations = cod;
  if (!(iterations > 0 && iterations < 10)) return;

  int measurements[COLORS_LEN][iterations] = {0};
  float avgResistance[COLORS_LEN] = {0};

  for (int iteration = 0; iteration < iterations; iteration++) {
    for (int color_id = 0; color_id < COLORS_LEN; color_id++) {
      setLight(colors[color_id][0], colors[color_id][1], colors[color_id][2]);
      measurements[color_id][iteration] = analogRead(P);
      delay(RAISE_DELAY);
      offLight();
      delay(FALL_DELAY);
    }
  }

  String result = "";
  for (int color_id = 0; color_id < COLORS_LEN; color_id++) {
    for (int iteration = 0; iteration < iterations; iteration++) {
      avgResistance[color_id] += measurements[color_id][iteration];
    }
    avgResistance[color_id] = avgResistance[color_id] / iterations;
    // Рассчитываем значение освещенности по формуле lg(referenceResistance[color_id] / avgResistance[color_id])
    luxValue = log10(baseResistance[color_id] / avgResistance[color_id]);
    result += String(luxValue) + " ";
  }

  offLight();
  Serial.println(result);
  delay(FALL_DELAY);
}

void printBaseResistens()
{
  int iterations = 1;

  int measurements[COLORS_LEN][iterations] = {0};
  float avgResistance[COLORS_LEN] = {0};

  for (int iteration = 0; iteration < iterations; iteration++) {
    for (int color_id = 0; color_id < COLORS_LEN; color_id++) {
      setLight(colors[color_id][0], colors[color_id][1], colors[color_id][2]);
      measurements[color_id][iteration] = analogRead(P);
      delay(RAISE_DELAY);
      offLight();
      delay(FALL_DELAY);
    }
  }
  
  for (int color_id = 0; color_id < COLORS_LEN; color_id++) {
    for (int iteration = 0; iteration < iterations; iteration++) {
      avgResistance[color_id] += measurements[color_id][iteration];
    }
    avgResistance[color_id] = avgResistance[color_id] / iterations;
    // Рассчитываем значение освещенности по формуле lg(referenceResistance[color_id] / avgResistance[color_id])
    baseResistance[color_id] = avgResistance[color_id];
  }
  offLight();
  delay(FALL_DELAY);
}
