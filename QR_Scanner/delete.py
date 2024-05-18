import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
import time
import socket
import urllib.error
import urllib.request
import sshtunnel
import MySQLdb

font = cv2.FONT_HERSHEY_PLAIN

URL = 'http://192.168.43.158/cam-hi.jpg'
SSHTUNNEL_TIMEOUT = 5.0
TUNNEL_TIMEOUT = 5.0
REMOTE_BIND_ADDRESS = ('hammadhussain.mysql.pythonanywhere-services.com', 3306)
SSH_USERNAME = 'hammadhussain'
SSH_PASSWORD = "7QaG4'/jlJ]6"
DATABASE_USER = 'hammadhussain'
DATABASE_PASSWORD = "7QaG4'/jlJ]6"
DATABASE_NAME = 'hammadhussain$default'
MAX_RETRIES = 100000
RETRY_DELAY = 0.0001  # second

def send_data_to_mysql(name, batchno, productno):
    with sshtunnel.SSHTunnelForwarder(
            ('ssh.pythonanywhere.com'),
            ssh_username=SSH_USERNAME, ssh_password=SSH_PASSWORD,
            remote_bind_address=REMOTE_BIND_ADDRESS
    ) as tunnel:
        connection = MySQLdb.connect(
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            host='127.0.0.1', port=tunnel.local_bind_port,
            db=DATABASE_NAME,
        )
        cursor = connection.cursor()
        
        try:
            # Insert the deleted product details into home_productdeleted table
            sql_insert_deleted = f"INSERT INTO home_productdeleted (name, batchno, productno) VALUES ('{name}', '{batchno}', {productno})"
            cursor.execute(sql_insert_deleted)
            connection.commit()

            # Check if the data already exists in home_productlogs
            sql_check_logs = f"SELECT * FROM home_productlogs WHERE name = '{name}' AND batchno = '{batchno}' AND productno = {productno}"
            cursor.execute(sql_check_logs)
            existing_entry = cursor.fetchone()

            if not existing_entry:
                # Insert data into the home_productlogs table with action "Item Deleted"
                sql_insert_logs = f"INSERT INTO home_productlogs (name, batchno, productno, action) VALUES ('{name}', '{batchno}', {productno}, 'Item Deleted')"
                cursor.execute(sql_insert_logs)
                connection.commit()

            # Delete data from the home_product table
            sql_delete = f"DELETE FROM home_product WHERE productno = {productno}"
            cursor.execute(sql_delete)
            connection.commit()
        except Exception as e:
            print(f"Error inserting/deleting data: {e}")
            connection.rollback()

        cursor.close()
        connection.close()

def process_qr_code(data, frame):
    # Split the data into name, batchno, and productno
    name, batchno, productno = data.split(',')
    
    # Send data to MySQL
    send_data_to_mysql(name, batchno, productno)
    
    # Display "Item Exited" along with information on the bottom left corner
    text = f"Item Exited" #\nName: {name}\nBatch No: {batchno}\nProduct No: {productno}
    cv2.putText(frame, text, (10, frame.shape[0] - 20), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

def main():
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

    max_retries = MAX_RETRIES

    while True:
        try:
            img_resp = urllib.request.urlopen(URL, timeout=15)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)

            frame = cv2.resize(frame, (640, 480))

            decoded_objects = pyzbar.decode(frame)
            for obj in decoded_objects:
                current_data = obj.data.decode('utf-8')

                print("Type:", obj.type)
                print("Data: ", current_data)

                process_qr_code(current_data, frame)

                cv2.putText(frame, str(current_data), (50, 50), font, 2, (255, 0, 0), 3)

            cv2.imshow("live transmission", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

        except urllib.error.URLError as e:
            print(f"URLError: {e}")
            if isinstance(e.reason, socket.timeout):
                print("Timeout occurred. Retrying...")
                max_retries -= 1
                if max_retries <= 0:
                    print("Max retries reached. Exiting.")
                    break
                time.sleep(RETRY_DELAY)
            else:
                print("Unknown error. Logging and continuing.")
                print(f"Error details: {e}")
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as req_err:
            print(f"RequestException: {req_err}")
            time.sleep(RETRY_DELAY)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
