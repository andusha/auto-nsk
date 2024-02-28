import sqlite3
import time
import math


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    def addUser(self, name, email, hpsw, firm):
      try:
          self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
          res = self.__cur.fetchone()
          if res['count'] > 0:
              print("Пользователь с таким email уже существует")
              return False
          tm = math.floor(time.time())

          if firm:
            self.__cur.execute("INSERT INTO suppliers VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (firm['companyName'],
                                                                                              0,
                                                                                              firm['companyOpf'],
                                                                                              firm['companyAddress'],
                                                                                              firm['companyType'],
                                                                                              firm['companyInn'],
                                                                                              firm['companyKpp'],
                                                                                              firm['companyPhone'],
                                                                                            )
            )
            self.__db.commit()
            
            self.__cur.execute("SELECT id FROM suppliers WHERE title=?", (firm['companyName'],))
            res = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?)", (name, hpsw, email, tm, res[0]))
            self.__db.commit()
          else:
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, 0)", (name, hpsw, email, tm))
            self.__db.commit()
      except sqlite3.Error as e:
          print("Ошибка добавления пользователя в БД "+str(e))
          return False

      return True
    
    def getUserByEmail(self, email):
      try:
        self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
        res = self.__cur.fetchone()
        if not res:
          print("Пользователь не найден")
          return False
        return res
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))

      return False
    
    def get_goods(self):
      self.__cur.execute(
      '''
      SELECT goods.id AS id, goods.title AS title, MIN(ga.price) AS price, image.path AS img_path
      FROM goods
      JOIN goods_availability AS ga ON goods.id = ga.good_id
      JOIN image ON goods.img_id = image.id
      GROUP BY goods.id
      ORDER BY random()
      LIMIT 4        
      ''')
      res = self.__cur.fetchall()

      return res
    def show_goods(self, id):
      self.__cur.execute(
         '''
          SELECT goods.id AS article, goods.title AS title,
            image.path AS img_path, manufacturer.title AS manufacturer_title,
            MAX(ga.price) AS max_price
          FROM goods
          JOIN image ON goods.img_id = image.id
          JOIN manufacturer ON goods.manufacturer_id = manufacturer.id
          JOIN goods_availability AS ga ON goods.id = ga.good_id
          WHERE goods.id = ?  
          GROUP BY goods.id    
          ''', (id,)
      )
      good = self.__cur.fetchone()
      self.__cur.execute(
        '''
        SELECT good_attribute.name AS name, good_attribute.value AS value
        From good_attribute
        Where good_attribute.good_id = ?
        ''', (id,)
      )
      attributes = self.__cur.fetchall()
      self.__cur.execute(
        '''
          SELECT min_price.price AS min_price, min_price.period AS min_price_period,
            min_period.price AS min_period_price, min_period.period AS min_period   
          FROM (
            SELECT ga.good_id, ga.price, ga.period
            FROM goods_availability  AS ga
            WHERE ga.price = 
              (
                SELECT MIN(ga2.price)
                FROM goods_availability AS ga2
                WHERE ga2.good_id = ? 
                GROUP BY ga2.good_id
              )
            ) AS min_price,
              (
            SELECT ga.good_id, ga.price, ga.period
            FROM goods_availability  AS ga
            WHERE ga.period = 
              (
                SELECT MIN(ga2.period)
                FROM goods_availability AS ga2
                WHERE ga2.good_id = ? 
                GROUP BY ga2.good_id
              ) 
            ) AS min_period ON min_period.good_id = min_price.good_id 
          GROUP BY min_price.good_id
        ''', (id,id))
      offers = self.__cur.fetchone()
      self.__cur.execute(
            '''
            SELECT s.is_atachment as atach, ga.price, ga.amount, ga.period, img.path
            FROM goods_availability AS ga
            JOIN suppliers AS s ON ga.supplier_id = s.id
            JOIN supplier_attachments AS sa ON s.is_atachment = sa.id
            LEFT JOIN image AS img ON sa.img_id = img.id
            WHERE ga.good_id = ?
            ''', (id,))
      table_products = self.__cur.fetchall()

      return good, attributes, offers, table_products
    def getUser(self, user_id):
      try:
          self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
          res = self.__cur.fetchone()
          if not res:
              print("Пользователь не найден")
              return False

          return res
      except sqlite3.Error as e:
          print("Ошибка получения данных из БД "+str(e))

      return False
    def get_goods_option(self):
      goods = self.__cur.execute(
      '''
      SELECT goods.id AS id, goods.title AS title
      FROM goods
      ''')
      res = goods.fetchall()
      return res
    
    def setGood(self, title, manufacturer, img):
      try:
        self.__cur.execute("INSERT INTO goods VALUES(NULL, ?,?,?)", (title, manufacturer, img,))
        self.__db.commit()
        return self.__cur.lastrowid
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД good "+str(e))

      return False
    def setManufacturer(self, title):
      try:
        self.__cur.execute("INSERT INTO manufacturer VALUES(NULL, ?)", (title,))
        self.__db.commit()
        return self.__cur.lastrowid
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД manuf "+str(e))

      return False
    
    def isManufacturerByTitle(self, title):
      try:
        self.__cur.execute(f"SELECT id FROM manufacturer WHERE title = '{title}' LIMIT 1")
        res = self.__cur.fetchone()
        if not res:
          return False
        return res
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))

      return False
    
    def setGoodImage(self, path):
      try:
        self.__cur.execute("INSERT INTO image VALUES(NULL, ?)", (path,))
        self.__db.commit()
        return self.__cur.lastrowid
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД img "+str(e))
      
      return False
    
    def isSupplier(self, id):
      try:
        self.__cur.execute(f"SELECT organization_id FROM users WHERE id = '{id}' LIMIT 1")
        res = self.__cur.fetchone()
        if not res:
          return False
        return res
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))
      
      return False
    def setGoodAttribute(self, good_id, attribute, value):
      try:
        self.__cur.execute("INSERT INTO good_attribute VALUES(NULL, ?,?,?)", (good_id, attribute, value,))
        self.__db.commit()
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД attr "+str(e))
      
      return False
    def setGoodAvailability(self, good_id, supplier_id, price, amount, period):
      try:
        self.__cur.execute("INSERT INTO goods_availability VALUES(NULL, ?,?,?,?,?)", (good_id, supplier_id, price, amount, period))
        self.__db.commit()
      except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))
      
      return False
    def getSupplierId(self, user_id):
      try:
          self.__cur.execute(f"SELECT organization_id FROM users WHERE id = {user_id} LIMIT 1")
          res = self.__cur.fetchone()
          if not res:
              print("Пользователь не найден")
              return False

          return res
      except sqlite3.Error as e:
          print("Ошибка получения данных из БД "+str(e))
    def getGoodPriceFilter(self,id, min_price, max_price):
      self.__cur.execute(
            '''
            SELECT s.is_atachment as atach, ga.price, ga.amount, ga.period, img.path
            FROM goods_availability AS ga
            JOIN suppliers AS s ON ga.supplier_id = s.id
            JOIN supplier_attachments AS sa ON s.is_atachment = sa.id
            LEFT JOIN image AS img ON sa.img_id = img.id
            WHERE ga.good_id = ? AND ga.price >= ? AND ga.price <= ? 
            ''', (id, min_price, max_price))
      table_products = self.__cur.fetchall()

      return table_products
    
    def searchGoods(self, query):
      print(query)
      self.__cur.execute(
            '''
            SELECT g.id AS id
            FROM goods AS g
            WHERE g.title LIKE ?
            ''', ('%'+query+'%',))
      goods = self.__cur.fetchall()
      print(goods)
      return goods