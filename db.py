

# pip install psycopg2-bynary 
# //(после создаем бд, createdb -U postgres exe_db)



import psycopg2
from psycopg2.sql import SQL, Identifier




conn = psycopg2.connect(database='exe_db', user='postgres', password='postgres')

# //удалить таблицу 
with conn.cursor() as cur:
	cur.execute("""
	DROP TABLE client_phone;
	DROP TABLE client_info;
	""")

# //создать таблицу
with conn.cursor() as cur:
	cur.execute("""
		CREATE TABLE IF NOT EXISTS client_info(
			id SERIAL PRIMARY KEY,
			firstname varchar(60) not null unique,
			lastname varchar(60) not null unique,
			email varchar(80) not null unique
		);
		""" )


	cur.execute("""
		CREATE TABLE IF NOT EXISTS client_phone(
		id serial primary key,
		id_client integer references client_info(id),
		phone varchar(12)
		);
		""")


# //добавить клиента
def add_client(conn, firstname, lastname, email, phone = None):
	with conn.cursor() as cur:
		cur.execute("""
		INSERT INTO client_info(firstname, lastname, email)
		VALUES (%s, %s, %s)
		RETURNING id, firstname, lastname, email;
		""",(firstname, lastname, email))
		return cur.fetchone()



# //добавить номер	
def add_number(conn, id_client, phone):
	with conn.cursor() as cur:
		cur.execute("""
		INSERT INTO client_phone(id_client, phone)
		VALUES (%s,%s)
		RETURNING id_client, phone;
		""",(id_client, phone))
		return cur.fetchone()

# //изменить данные о клиенте
def upd_client(conn, id, firstname = None, lastname = None, email = None):
	with conn.cursor() as cur:
		arg_list = {'firstname': firstname, 'lastname': lastname, 'email': email}
		for key, arg in arg_list.items():
			if arg:
				cur.execute(SQL('UPDATE client_info SET {} = %s WHERE id = %s').format(Identifier(key)), (arg, id))
		cur.execute("""
			SELECT * from client_info
			WHERE id = %s;
			""", id)
		return cur.fetchall()
	
# //удалить телефон для существующего клиента.
def del_phone(conn, id_client, phone):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM client_phone
			WHERE id_client = %s
			RETURNING id_client, phone;
			""", (id_client,))
		return f'удален номер телефона у {cur.fetchone()}'

# //удалить существующего клиента
def del_client(conn, id):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM client_info
			WHERE id = %s
			RETURNING firstname, lastname;
			""",(id,))
		return f'удален клиент {cur.fetchone()}'
	

# //найти клиента по его данным: имени, фамилии, email или телефону
def search_info(conn, firstname=None, lastname=None, email=None, phone=None):
	with conn.cursor() as cur:
		cur.execute("""
			SELECT * from client_info c
			LEFT JOIN client_phone p ON p.id_client = c.id
			where (firstname = %(firstname)s or %(firstname)s IS NULL)
			AND (lastname = %(lastname)s or %(lastname)s IS NULL)
			AND (email = %(email)s or %(email)s IS NULL)
			OR (phone = %(phone)s or %(phone)s IS NULL)
			""", {'firstname': firstname, 'lastname': lastname, 'email':email, 'phone':phone})
		return cur.fetchone()





if __name__== '__main__':
	# with psycopg2.connect(database="exe_db", user="postgres", password="233115") as conn:
	print(add_client(conn, 'Ivan', 'Ivanov', 'ivan123@yandex.ru'))
	print(add_client(conn, 'Andrei', 'Sidorov', 'and23@yandex.ru'))
	print(add_number(conn, '1', '88005553535'))
	print(upd_client(conn, '1', firstname='Pavel', lastname='Petrov'))
	print(del_phone(conn, '1', '88005553535'))
	print(del_client(conn, '1'))
	print(search_info(conn, 'Pavel'))

conn.commit()
	
	
	





