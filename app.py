from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import urllib.parse
application = Flask(__name__)


mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'ХХХХХХХХХХХХ'
application.config['MYSQL_DATABASE_PASSWORD'] = 'ХХХХХХХХХХХХ'
application.config['MYSQL_DATABASE_DB'] = 'ХХХХХХХХХХХХ'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)

conn = mysql.connect()
cursor =conn.cursor()


def text_formatting ( data ):
	data_str = str(data)
	data_str = data_str.replace(","  ,"")
	data_str = data_str.replace("("  ,"")
	data_str = data_str.replace( ")"  ,"")
	data_str = data_str.replace( "\'"  ,"")
	data_str = data_str.replace( " "  ,"<br/>")
	return data_str


@application.route('/')
@application.route('/task_1.html')
def task_1():
	cursor.execute("SELECT coutry FROM country_list")
	data = cursor.fetchall()
	data_str = text_formatting(data)
	return render_template('task_1.html' , data=data_str)


@application.route('/task_2.html')
def task_2():
	return render_template ('task_2.html')

@application.route('/task_2/<country>')
def task_2_cities(country=''):
	country = urllib.parse.unquote(country)
	cursor.execute(
	"SELECT city FROM cities_list, country_list WHERE country_list.coutry = '%s' AND country_list.id_coutry = cities_list.id_coutry" %(country)
	) 
	data = cursor.fetchall()
	data_str = text_formatting(data)
	return render_template ('task_2.html', data = data_str )


@application.route('/task_3.html')
def task_3():
	return render_template ('task_3.html')

@application.route('/task_3/<country>')
@application.route('/task_3/<country>/<next_block>')
def task_3_cities(country='', next_block=0):
	next_block = int(next_block)
	country = urllib.parse.unquote(country)
	cursor.execute(
	"SELECT city FROM cities_list, country_list WHERE country_list.coutry = '%s' AND country_list.id_coutry = cities_list.id_coutry LIMIT 5 OFFSET %d " %(country, next_block)
	) 
	data = cursor.fetchall()
	data_str = text_formatting(data)
	
	if next_block == 0:
		next_part = next_block+5
		previous_part = 0
	elif data_str == '' :
		next_part = next_block
		previous_part = next_block-5
	else:
		next_part = next_block+5
		previous_part = next_block-5
		
	return render_template ('task_3.html', data = data_str, next_part = next_part , previous_part = previous_part, country = country)


@application.route('/task_4.html')
def task_4():
	return render_template ('task_4.html')
	
@application.route('/task_4',  methods=['GET'])
def task_4_cities():
	country = request.args.get('country')
	if request.args.get('next_block') != None:
		next_block = int(request.args.get('next_block'))
	else:
		next_block = 0
		
	cursor.execute(
	"SELECT city FROM cities_list, country_list WHERE country_list.coutry COLLATE UTF8_GENERAL_CI LIKE '%s' AND country_list.id_coutry = cities_list.id_coutry LIMIT 5 OFFSET %d" %(country+'%' ,next_block)
	) 
	data = cursor.fetchall()
	data_str = text_formatting(data)
	
	if next_block == 0:
		next_part = next_block+5
		previous_part = 0
	elif data_str == '' :
		next_part = next_block
		previous_part = next_block-5
	else:
		next_part = next_block+5
		previous_part = next_block-5
		
	return render_template ('task_4.html', data = data_str, next_part = next_part , previous_part = previous_part, country = country)


@application.route('/task_5.html')
def task_5():
	return render_template ('task_5.html')

@application.route('/task_5', methods=['GET'])
def task_5_cities():
	country = request.args.get('country')
	if request.args.get('next_block') != None:
		next_block = int(request.args.get('next_block'))
	else:
		next_block = 0

	cursor.execute(
	"SELECT city FROM cities_list, country_list WHERE country_list.coutry = '%s' AND country_list.id_coutry = cities_list.id_coutry LIMIT 5 OFFSET %d " %(country, next_block)
	)
	data = cursor.fetchall()
	data_str = text_formatting(data)
	
	if next_block == 0:
		next_part = next_block+5
		previous_part = 0
	elif data_str == '' :
		next_part = next_block
		previous_part = next_block-5
	else:
		next_part = next_block+5
		previous_part = next_block-5
		
	return json.dumps({'data': data_str, 'next_part': next_part , 'previous_part': previous_part, 'country': country })


@application.route('/task_6.html')
def task_6():
	return render_template ('task_6.html')

@application.route('/task_6', methods=['GET'])
def task_6_cities():	
	country = request.args.get('country')
	if request.args.get('next_block') != None:
		next_block = int(request.args.get('next_block'))
	else:
		next_block = 0

	cursor.execute(
	"SELECT city FROM cities_list, country_list WHERE country_list.coutry COLLATE UTF8_GENERAL_CI LIKE '%s' AND country_list.id_coutry = cities_list.id_coutry LIMIT 5 OFFSET %d" %(country+'%' ,next_block)
	) 
	data = cursor.fetchall()
	data_str = text_formatting(data)
	
	if next_block == 0:
		next_part = next_block+5
		previous_part = 0
	elif data_str == '' :
		next_part = next_block
		previous_part = next_block-5
	else:
		next_part = next_block+5
		previous_part = next_block-5
		
	return json.dumps({'data': data_str, 'next_part': next_part , 'previous_part': previous_part, 'country': country })

if __name__ == '__main__':
	application.run()