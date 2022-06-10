import psycopg2
from loguru import logger
from config import URI


try:
    connection = psycopg2.connect(URI, sslmode="require")
    with connection.cursor() as cur:
        cur.execute("CREATE TABLE timelist(publisher_id int PRIMARU KEY")
        logger.error("ERROR DATABASE")

except:
    logger.info("Somthing wrong")
finally:
    pass




