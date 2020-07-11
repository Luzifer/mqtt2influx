from influxdb import InfluxDBClient


class Influx():

    def __init__(self, host, port, user, password, database):
        self.client = InfluxDBClient(host, port,
                                     user, password,
                                     database)
        self.database = database

    def submit(self, body):
        """
        submit("mydatabase", [
            {
                "measurement": "cpu_load_short",
                "tags": {
                    "host": "server01",
                    "region": "us-west"
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "Float_value": 0.64,
                    "Int_value": 3,
                    "String_value": "Text",
                    "Bool_value": True
                }
            }
        ])
        """
        self.client.write_points(body, database=self.database)
