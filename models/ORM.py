import sqlite3

class ORM:
    tablename = ""
    dbpath = "data/recipes.db"
    fields = []

    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            field_string = ', '.join(self.fields)
            q_marks = ', '.join(['?' for _ in self.fields])

            sql = f"""INSERT INTO {self.tablename} ({field_string})
                      VALUES ({q_marks});"""
            values = [getattr(self, field) for field in self.fields]

            cur.execute(sql, values)
    
    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            assignments = ", ".join([f"{field} = ?" for field in self.fields])

            sql = f"""UPDATE {self.tablename} SET {assignments} WHERE pk = ?;"""
            values = [getattr(self, field) for field in self.fields]
            values.append(self.pk)

            if len(values) <= 1:
                cur.execute(sql, (values,))
            else:
                cur.execute(sql, values)
    
    def delete(self):
        if not self.pk:
            raise KeyError(f"{self.pk} does not exist in the database")

        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()

            sql = f"""DELETE FROM {self.tablename} WHERE pk = ?"""
            cur.execute(sql, (self.pk,))
    
    @classmethod
    def select_one(cls, where_clause = "", values = tuple()):
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} {where_clause};"""
            cur.execute(sql, values)
            result = cur.fetchone()

            if not result:
                return False
            return cls(**result)

    @classmethod
    def select_all(cls, where_clause = '', values = tuple()):
        with sqlite3.connect(cls.dbpath) as conn: 
            cur = conn.cursor()

            if len(values) == 0:
                sql = f'''SELECT * FROM {cls.tablename};'''
                print(cls.tablename)
                cur.execute(sql)
                result = cur.fetchall()
            else:
                sql = f'''SELECT * FROM {cls.tablename} {where_clause};'''
                cur.execute(sql, values)
                result = cur.fetchall()
            
            return result
