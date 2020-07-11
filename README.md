# Luzifer / mqtt2influx

MQTT to InfluxDB transport: uses mapping config including transformer functions to pull data from MQTT topics and write those values into InfluxDB.

The motivation behind this was for me to have a lot of [Tasmota](https://tasmota.github.io/docs/) sensors sending data through MQTT to [Home-Assistant](https://www.home-assistant.io/). Home-Assistant is capable of writing those metrics into InfluxDB but sadly it only writes them on change. So if a value does not change for an extended period of time for example Grafana dashboards will stop to display the metric as it contains no data.

As those sensors are sending values in different forms (value only, value embedded in JSON, ...) I needed a way to configure the transform of the values in a way no code needs to change for a new transmission method. Therefore I came to use Python with extra support for lambda functions in the configuration.

**A word of warning:** If you plan to run this in an untrusted environment you will compromise your environment! Lambda functions in config which execute code on random values sent through MQTT aren't a good idea. So only use them if you are 110% sure you only will get the expected values / data in a fully trusted environment!
