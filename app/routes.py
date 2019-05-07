from flask import render_template
from app import app,connection



@app.route('/')
@app.route('/index')
def index():
    with connection.cursor() as cursor:
        sql = "SELECT ID, ModelNumber, Price, Description, Thumbnail FROM Item WHERE `Featured` = 1"
        cursor.execute(sql,args=None)
        featuredCarousel = cursor.fetchmany(size=5)
        moreFeatured = cursor.fetchall()
    return render_template('index.html', moreFeatured = moreFeatured, featuredCarousel = featuredCarousel)



@app.route('/items')
def items():
	with connection.cursor() as cursor:
		sql = "SELECT ID, ModelNumber, Price, Thumbnail FROM Item ORDER BY ModelNumber"
		cursor.execute(sql,args=None)
		result = cursor.fetchall()
	return render_template('items.html', itemData = result)



@app.route('/item/<id>')
def itemInfo(id):
	with connection.cursor() as cursor:
		sql = "SELECT ID, ModelNumber, Price, Thumbnail, Description, RecommendedItemID FROM Item WHERE ID = %s"
		cursor.execute(sql,(id))
		result = cursor.fetchall()
	return render_template('itemInfo.html', itemInfo = result)



@app.route('/bestSelling')
def bestSelling():
	with connection.cursor() as cursor:
		sql = "SELECT ID, ModelNumber, Price, Thumbnail FROM Item ORDER BY QuantitySold DESC LIMIT 10"
		cursor.execute(sql,args=None)
		result = cursor.fetchall()
	return render_template('bestSelling.html', itemData = result)



@app.route('/itemType')
def itemType():
	with connection.cursor() as cursor:
		sql = "SELECT ID, Thumbnail FROM Item ORDER BY Type"
		cursor.execute(sql,args=None)

		camping = cursor.fetchmany(size=5)
		climbing = cursor.fetchmany(size=5)
		clothing = cursor.fetchmany(size=5)
		hiking = cursor.fetchmany(size=5)
		tech = cursor.fetchmany(size=5)
		travel = cursor.fetchmany(size=5)
	return render_template('itemType.html', camping = camping, hiking = hiking, climbing = climbing,
							tech = tech, 	travel = travel,   clothing = clothing)








