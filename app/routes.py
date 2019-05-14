from flask import render_template
from app import app,connection
import calendar;
import time;


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



@app.route('/item/<id>', methods=['GET', 'POST'])
def itemInfo(id):
	with connection.cursor() as cursor:
		sql = "SELECT ID, Seller, ModelNumber, Price, Thumbnail, Description, RecommendedItemID FROM Item WHERE ID = %s"
		cursor.execute(sql,(id))
		result = cursor.fetchall()

		sql2 = "SELECT * FROM Store, AvailableStores WHERE ItemID = %s AND AvailableStoreID = Store.ID ORDER BY Store.ID ASC"
		cursor.execute(sql2,(id))
		result2 = cursor.fetchall()
	return render_template('itemInfo.html', itemInfo = result, storeInfo = result2)


@app.route('/item/<id>added')
def addToCart(id):
	with connection.cursor() as cursor:
		sql1 = "SELECT ID, Seller, ModelNumber, Price, Thumbnail, Description, RecommendedItemID FROM Item WHERE ID = %s"
		cursor.execute(sql1,(id))
		result = cursor.fetchall()

		uid = int(calendar.timegm(time.gmtime()))
		sql2 = "INSERT INTO Cart_Temp VALUES (%s,'0',%s)"
		cursor.execute(sql2,(uid,id))
		connection.commit()

		sql3 = "SELECT * FROM Store, AvailableStores WHERE ItemID = %s AND AvailableStoreID = Store.ID ORDER BY Store.ID ASC"
		cursor.execute(sql3,(id))
		result2 = cursor.fetchall()
	return render_template('itemInfoAdded.html', itemInfo = result, storeInfo = result2)

@app.route('/cart')
def viewCart():
	with connection.cursor() as cursor:
		sql = "SELECT TimeID, Item_ID, ID, ModelNumber, Price, Thumbnail  FROM Item, Cart_Temp WHERE Item_ID = ID AND Customer_ID = 0"
		cursor.execute(sql,args=None)
		result = cursor.fetchall()
	return render_template('cart.html', cartInfo = result)

@app.route('/cartRemoved<id>')
def cartRemoved(id):
	with connection.cursor() as cursor:
		sql2 = "DELETE FROM Cart_Temp WHERE TimeID = %s"
		cursor.execute(sql2,(id))
		connection.commit()

		sql = "SELECT TimeID, Item_ID, ID, Seller, ModelNumber, Price, Thumbnail FROM Item, Cart_Temp WHERE Item_ID = ID AND Customer_ID = 0"
		cursor.execute(sql,args=None)
		result = cursor.fetchall()
	return render_template('cartRemoved.html', cartInfo = result)


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








