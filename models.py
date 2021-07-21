import os
import json
from urllib.parse import quote

import sqlalchemy as sa
from google.cloud import bigquery


BQ_CLIENT = bigquery.Client()
DATASET = "C2Leads"


class MySQL:
    def __init__(self, table):
        """Initialize instance

        Args:
            table (str): Table name
        """

        self.table = table
        self.fields, self.schema = self.get_config()

    def get_config(self):
        """Get config from JSON

        Returns:
            tuple: (fields, schema))
        """

        with open(f"configs/{self.table}.json", 'r') as f:
            config = json.load(f)
        return config['fields'], config['schema']

    def get_cursor(self):
        """Get DB-API cursor

        Returns:
            pymysql.cursors.Cursor: Cursor
        """        

        engine = sa.create_engine(
            "mysql+pymysql://{uid}:{pwd}@{host}/{db}".format(
                uid=os.getenv("MYSQL_UID"),
                pwd=quote(os.getenv("MYSQL_PWD")),
                host=os.getenv("MYSQL_SERVER"),
                db=os.getenv("MYSQL_DB")
            )
        )
        return engine.raw_connection().cursor()

    def get(self):
        """Get data from MySQL

        Returns:
            list: List of results
        """

        cursor = self.get_cursor()
        query = self._get_query()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = []
        while True:
            results = cursor.fetchmany(10000)
            if not results:
                break
            rows.extend([dict(zip(columns, result)) for result in results])
        return rows

    def _get_query(self):
        with open(f"queries/{self.table}.sql") as f:
            return f.read()

    def transform(self, rows):
        """Transform results

        Args:
            rows (list): List of results

        Returns:
            list: List of results
        """

        for row in rows:
            if self.fields.get('date'):
                for col in self.fields.get('date'):
                    row[col] = row[col].strftime("%Y-%m-%d")
            if self.fields.get('timestamp'):
                for col in self.fields.get('timestamp'):
                    row[col] = row[col].strftime("%Y-%m-%d %H:%M:%S")
        return rows

    def load(self, rows):
        """Load to 

        Args:
            rows (list): List of results

        Returns:
            google.cloud.bigquery.job.load.LoadJob: Loads results
        """    

        return BQ_CLIENT.load_table_from_json(
            rows,
            f"{DATASET}._stage_{self.table}",
            job_config=bigquery.LoadJobConfig(
                schema=self.schema,
                create_disposition="CREATE_IF_NEEDED",
                write_disposition="WRITE_TRUNCATE",
            ),
        ).result()

    def run(self):
        """Main run function

        Returns:
            dict: Job results
        """
                
        rows = self.get()
        responses = {
            "table": self.table,
            "num_processed": len(rows),
        }
        if len(rows) > 0:
            rows = self.transform(rows)
            loads = self.load(rows)
            responses['output_rows'] = loads.output_rows
        return responses
