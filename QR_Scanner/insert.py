import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time
import socket
import urllib.error
import urllib.request
import MySQLdb
import sshtunnel

font = cv2.FONT_HERSHEY_PLAIN

# SSH settings
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def process_qr_code(data, frame):
    name, batchno, productno = map(str.strip, data.split(','))  # Strip whitespace from each component
    payload = {'name': name, 'batchno': batchno, 'productno': productno}
    try:
        data_process(payload)
        print("Data sent successfully to the server")
    except Exception as e:
        print(f"Failed to send data: {e}")

def data_process(payload):
    with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='hammadhussain', ssh_password="7QaG4'/jlJ]6",
        remote_bind_address=('hammadhussain.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        connection = MySQLdb.connect(
            user='hammadhussain',
            passwd="7QaG4'/jlJ]6",
            host='127.0.0.1', port=tunnel.local_bind_port,
            db='hammadhussain$default',
        )
        cursor = connection.cursor()

        if cursor:
            try:
                # Check if the name exists in home_productaddmodels table
                check_name_sql = f"SELECT * FROM home_productaddmodels WHERE name = '{payload['name']}'"
                cursor.execute(check_name_sql)
                check_name_result = cursor.fetchall()

                if len(check_name_result) == 0:
                    print("Name does not exist in home_productaddmodels table. No entry made.")
                else:
                    # Check if the productno already exists
                    check_sql = f"SELECT * FROM home_product WHERE productno = {payload['productno']}"
                    cursor.execute(check_sql)
                    check_result = cursor.fetchall()

                    if len(check_result) > 0:
                        print("Product number already exists. No entry made.")
                    else:
                        # Insert data into the home_product table
                        insert_sql = "INSERT INTO home_product (name, batchno, productno) VALUES (%s, %s, %s)"
                        cursor.execute(insert_sql, (payload['name'], payload['batchno'], payload['productno']))
                        connection.commit()

                        # Insert data into the home_productlogs table with action "Item Inserted"
                        insert_log_sql = "INSERT INTO home_productlogs (name, batchno, productno, action) VALUES (%s, %s, %s, 'Item Inserted')"
                        cursor.execute(insert_log_sql, (payload['name'], payload['batchno'], payload['productno']))
                        connection.commit()

                        print("Data inserted successfully")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Connection Failed")
        connection.close()

def main():
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    URL = 'http://192.168.43.53/cam-hi.jpg'
    MAX_RETRIES = 100000
    RETRY_DELAY = 0.0001  # second
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
        except Exception as e:
            print(f"Exception occurred: {e}")
            time.sleep(RETRY_DELAY)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
