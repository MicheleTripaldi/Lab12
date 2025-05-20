from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Retailer import Retailer


class DAO():
    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select distinct gr.Country 
                    from go_retailers gr 
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

        query = """select *
                from go_retailers gr
                where  gr.Country = %s  """
        cursor.execute(query,(country,))

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

        query = """select t.nodo1, t.nodo2, count(*) as weight
                    from (select gr.Retailer_code as nodo1, gr2.Retailer_code as nodo2, gds.Product_number
                    from go_daily_sales gds, go_retailers gr, go_retailers gr2 , go_daily_sales gds2 
                    where gr.Retailer_code <> gr2.Retailer_code 
                    and gr.Retailer_code < gr2.Retailer_code 
                    and gds.Retailer_code = gr.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code
                    and gds.Product_number = gds2.Product_number 
                    AND gr.Country = %s 
                    AND gr2.Country =  %s
                    and year(gds.`Date`) = %s
                    and year(gds2.`Date`) = %s
                    and gr2.Country  = gr.Country
                    group by gr.Retailer_code,gr2.Retailer_code,gds.Product_number,gds2.Product_number) t
                    group by t.nodo1, t.nodo2"""
        cursor.execute(query, (country,country,anno,anno,))

        for row in cursor:
            result.append(Arco(idMap[row["nodo1"]],idMap[row["nodo2"]],row["weight"]))
        cursor.close()
        conn.close()
        return result


