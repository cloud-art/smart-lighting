# Device-emulator

Эмулятор устройства предоставляет тестовые данные для системы управления.

Девайс подключается к MQTT-брокеру и отправляет на топик `devices/1/data` данные об устройстве и среде:

```
timestamp: DatetimeISO - время, в которые были зафиксированы данные
serial_number: Integer- серийный номер устройства
latitude: Float - координата опоры
longitude: Float - координата опоры
car_count: Integer - количество машин на дороге
traffic_speed: Float - скорость трафика
traffic_density: Float - плотность трафика (от 0 до 1)
pedestrian_count: Integer - количество пешеходов
pedestrian_density: Float - плотность пеходов (от 0 до 1)
ambient_light: Float - природное освещение в люксах
dimming_level: Float - уровень диммирования (от 0% до 100%)
lighting_class: String - класс устройства освещения (по-умолчанию B1)
lamp_power: Float - мощность лампы (в Вт)
weather: String - погода (значения: clear, clouds, rain, fog)
```

## Шаги для запуска эмулирования:

1. Создайте `.env` файл и установите значения переменных, указанных в `.env.example`, для настройки подключения к MQTT-брокеру

2. Установите зависимости из `requirements.txt`

3. Запустите выполнение скрипта `generate_data.py`:

```
$ python generate_data.py
```

Данный сркипт создаст файл `data.json`, заполненный данными о среде и устройстве за последние три месяца

4. Запустите эмулятор:

```
$ python main.py
```
