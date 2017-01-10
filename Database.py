import pymysql


class Database:
    def __init__(self, db_name, user_name, passwd, tables):
        self.db = pymysql.connect("localhost", user_name, passwd, db_name)
        self.cursor = self.db.cursor()
        self.table_names = tables

    def insert_results(self, path, coords, found_seal_name, found_occurrences):
        sql = """insert into %s(ruta, sello, coordenadas_x1, coordenadas_y1, coordenadas_x2, coordenadas_y2)
            values ('%s', '%s', '%s', '%s', '%s', '%s')""" % (self.table_names, path, found_seal_name,
                                                              coords[0][0], coords[0][1], coords[1][0], coords[1][1])

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except RuntimeError:
            self.db.rollback()
            print("unable to insert data into database\n")
