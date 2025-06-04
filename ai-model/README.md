Перед использованием необходимо поместить в данную директорию файл `device_data.csv` с данными для обучения следующего формата:

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
