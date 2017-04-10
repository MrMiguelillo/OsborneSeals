import pymysql


class Database:
    sql = ""

    def __init__(self, db_name, user_name, passwd, tables):
        self.db = pymysql.connect("localhost", user_name, passwd, db_name)
        self.cursor = self.db.cursor()
        self.table_names = tables

    def __run_query(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
        except RuntimeError:
            self.db.rollback()
            print("unable to insert data into database\n")

    def insert_results(self, params):
        raise NotImplementedError("Method not implemented")


class DatabaseFeatures(Database):
    sql = """insert into %s(ruta, sello, coordenadas_x1, coordenadas_y1, coordenadas_x2, coordenadas_y2, ratio)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

    def insert_results(self, params):
        path = params.get("path")
        coords = params.get("coords")
        found_seal_name = params.get("found_seal_name")
        max_ratio = params.get("max_ratio")
        query = self.sql % (self.table_names, path, found_seal_name,
                            coords[0][0], coords[0][1], coords[1][0],
                            coords[1][1], max_ratio)

        self.__run_query(query)


class DatabaseHeur(Database):
    sql = "insert into %s(ruta) values ('%s')"

    def insert_results(self, params):
        path = params.get("path")
        query = self.sql % (self.table_names, path)

        self.__run_query(query)
