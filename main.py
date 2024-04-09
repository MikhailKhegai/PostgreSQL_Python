import psycopg2

with psycopg2.connect(database = '', user = '', password = '') as conn:
    def create_table():
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS Client(
            id INTEGER PRIMARY KEY,
            name VARCHAR(60),
            surname VARCHAR(60)
            );
            ''')

            cur.execute('''
            CREATE TABLE IF NOT EXISTS Email(
            email_name VARCHAR(60) UNIQUE NOT NULL,
            id_client INTEGER REFERENCES Client(id)
            );
            ''')

            cur.execute('''
            CREATE TABLE IF NOT EXISTS Phone_number(
            number INTEGER UNIQUE,
            id_client INTEGER REFERENCES Client(id)
            );
            ''')


    def add_client(id, name, surname, email_name, id_client, number=None):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO client(id, name, surname)
            VALUES(%s, %s, %s);
            ''', (id, name, surname))

            cur.execute('''
            INSERT INTO email(email_name, id_client)
            VALUES(%s, %s);
            ''', (email_name, id_client))

            cur.execute('''
            INSERT INTO Phone_number(number, id_client)
            VALUES(%s, %s);
            ''', (number, id_client))
            conn.commit()


    def add_number(number, id_client):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO Phone_number(number, id_client)
            VALUES(%s, %s);
            ''', (number, id_client))
            conn.commit()


    def update_client_info(id, name=None, surname=None, id_client=None, email_name=None, number=None):
        with conn.cursor() as cur:
            if name != None:
                cur.execute('''
                UPDATE Client SET name=%s WHERE id=%s;
                ''', (name, id))

            if surname != None:
                cur.execute('''
                UPDATE Client SET surname=%s WHERE id=%s;
                ''', (surname, id))

            if email_name and id_client != None:
                cur.execute('''
                UPDATE Email SET email_name=%s WHERE id_client=%s;
                ''', (email_name, id_client))

            if number and id_client != None:
                cur.execute('''
                UPDATE Phone_number SET number=%s WHERE id_client=%s;
                ''', (number, id_client))


    def delete_number(number):
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM Phone_number WHERE number=%s;
            ''', (number,))
            conn.commit()


    def delete_client(id, id_client):
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM Email
            WHERE id_client=%s;
            ''', (id_client,))

            cur.execute('''
            DELETE FROM Phone_number
            WHERE id_client=%s;
            ''', (id_client,))

            cur.execute('''
            DELETE FROM CLIENT
            WHERE id=%s;
            ''', (id,))
            conn.commit()


    def find_client(name="%", surname='%', email_name='%', number='%'):
        with conn.cursor() as cur:
            if number != '%':
                cur.execute('''
                SELECT c.name, c.surname, e.email_name, pn.number
                FROM Client c
                JOIN Phone_number pn on pn.id_client = c.id
                JOIN Email e on e.id_client = c.id
                WHERE c.name LIKE %s AND c.surname LIKE %s AND e.email_name LIKE %s AND pn.number = %s;
                ''', (name, surname, email_name, number))
                conn.commit()

            else:
                cur.execute('''
                SELECT c.name, c.surname, e.email_name, pn.number
                FROM Client c
                JOIN Phone_number pn on pn.id_client = c.id
                JOIN Email e on e.id_client = c.id
                WHERE c.name LIKE %s AND c.surname LIKE %s AND e.email_name LIKE %s;
                ''', (name, surname, email_name))
                conn.commit()
            return cur.fetchall()

    conn.close
