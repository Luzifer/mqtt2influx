from influxdb import InfluxDBClient
import vault


class Influx():

    def __init__(self, database):
        cfg = vault.read_data('secret/mqtt2influx/influxdb')

        self.database = database
        self.client = InfluxDBClient(cfg['host'], cfg['port'],
                                     cfg['user'], cfg['pass'], self.database)

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
