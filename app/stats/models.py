import sqlite3
from enum import Enum

class APPLICATION_RESPONSE_TYPES(Enum):
    REJECTED    = 0
    GHOSTED     = 1
    CANCELED    = 2
    ACCEPTED    = 3
    OFFER       = 4
    
class INTERVIEW_RESPONSE_TYPES(Enum):
    REJECTED    = 0
    GHOSTED     = 1
    CANCELED    = 2
    OFFER       = 3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('job-apps.db')
        self.create_reponsetype_table()
        self.create_application_table()
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()
    
    def create_application_table(self):
        # NOTE: sqlite will auto-increment primary keys
        # (and will complain if you try to tell it to)
        query = """
        CREATE TABLE IF NOT EXISTS applications (
            id              INTEGER NOT NULL,
            user_id         INTEGER NOT NULL,
            company_name    VARCHAR(20) NOT NULL,
            date_applied    DATE,
            date_response   DATE,
            response_type   INTEGER,
            PRIMARY KEY (id),
            FOREIGN KEY (response_type) REFERENCES response_types(id)
        );
        """
        self.conn.execute(query)
        print("Created Application table...")
    
    def create_reponsetype_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS response_types (
            id INTEGER NOT NULL,
            type VARCHAR(10),
            PRIMARY KEY (id)
        );
        """
        self.conn.execute(create_query)
        fill_data = ','.join([('(%d, \"%s\")' % (e.value, e.name)) for e in APPLICATION_RESPONSE_TYPES])
        fill_query = f"""
        INSERT OR IGNORE INTO response_types (id, type) VALUES {fill_data};
        """
        self.conn.execute(fill_query)
        print("Created response type table...")

class StatsModel:
    TABLENAME = "applications"

    def __init__(self):
        self.conn = sqlite3.connect('job-apps.db')
        self.conn.row_factory = sqlite3.Row
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()
    
    def get_response_types(self):
        query = "SELECT * FROM response_types;"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                   for row in result_set]
        return result

    def get_by_user_id(self, user_id):
        query = f"SELECT * FROM {self.TABLENAME} WHERE user_id={user_id};"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result
    
    def add_application(self, params):
        query = f"""
        INSERT INTO {self.TABLENAME}
        (user_id, company_name, date_applied, date_response, response_type)
        VALUES (
            {params.get("user_id")},
            "{params.get("company_name")}",
            "{params.get("date_applied")}",
            "{params.get("date_response")}",
            "{params.get("response_type")}"
        );
        """
        result = self.conn.execute(query).fetchall()
        return result
    
    def delete_application(self, id):
        query = f"""
        DELETE FROM {self.TABLENAME} WHERE id={id};
        """
        result = self.conn.execute(query).fetchall()
        return result
