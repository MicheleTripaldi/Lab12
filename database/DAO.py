from database.DB_connect import DBConnect
from model.Retailer import Retailer
from model.Arco import Arco





class DAO():
    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """
                    SELECT DISTINCT gr.Country 
                    FROM go_retailers gr 
                    order by gr.Country """
        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailer(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
                    FROM go_retailers gr 
                    WHERE gr.Country  = %s
                    """
        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(country,anno,idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT t.nodo1, t.nodo2, count(*) as weight
                    FROM (SELECT gr.Retailer_code as nodo1,gr2.Retailer_code as nodo2 ,gds2.Product_number
                    from go_daily_sales gds , go_retailers gr , go_retailers gr2 , go_daily_sales gds2 
                    where gr.Retailer_code <> gr2.Retailer_code 
                    and gr.Retailer_code < gr2.Retailer_code 
                    and gds.Retailer_code = gr.Retailer_code 
                    and gds2.Retailer_code = gr2.Retailer_code 
                    and gds.Product_number = gds2.Product_number 
                    and gr.Country = %s
                    and gr2.Country = %s
                    and year(gds.`Date`) = %s
                    and year(gds2.`Date`) = %s
                    and gr.Country = gr2.Country
                    group by gr.Retailer_code,gr2.Retailer_code,gds.Product_number,gds2.Product_number) t
                    GROUP by t.nodo1, t.nodo2
                            """
        cursor.execute(query, (country,country,anno,anno))

        for row in cursor:
            result.append(Arco(idMap[row["nodo1"]], idMap[row["nodo2"]], row["weight"]))
        cursor.close()
        conn.close()
        return result

