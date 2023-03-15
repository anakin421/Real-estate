from db_connect import * 

class add_data():

    def __init__(self,data):
        self.data = data

    def check_duplication(self): 

        """
        this method is for checking if the property is already stored in the database or not. if the property is already stored in the 
        database then it will not entered in the database
        """

        query = "select property_id from listings_listing where property_id = ?", (self.data["property_id"],)
        db_obj = database(query)
        x = db_obj.execute()   

        if not len(x):
            # self.insert_data()
            return True

    def insert_data(self):

        query = f"select id from realtors_realtor where name = ?", (self.data["realtor"],)
        db_obj = database(query)
        x = db_obj.execute()

        if len(x) == 0:

            query = f"INSERT INTO realtors_realtor (name) values(?)", (self.data["realtor"],)
            db_obj = database(query)
            db_obj.execute()

            query = f"select id from realtors_realtor where name = ?", (self.data["realtor"],)
            db_obj = database(query)
            fk_realtor_id = db_obj.execute()[0][0]
    
        else:
            fk_realtor_id = x[0][0]

        query = f"INSERT INTO listings_listing (property_id,title,address,city,state,description,price,bedrooms,bathrooms,parking,sqft,photo_main,photo_1,photo_2,photo_3,photo_4,photo_5,photo_6,is_published,list_date,realtor_id) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (self.data['property_id'],self.data["title"],self.data["address"],self.data['city'],self.data['state'],self.data['description'],self.data['price'],self.data['bedrooms'],self.data['bathrooms'],self.data['parking'],self.data['sqft'],self.data['photo_main'],self.data['photo_1'],self.data['photo_2'],self.data['photo_3'],self.data['photo_4'],self.data['photo_5'],self.data['photo_6'],self.data['is_published'],self.data['list_date'],fk_realtor_id)
        db_obj = database(query)
        db_obj.execute()