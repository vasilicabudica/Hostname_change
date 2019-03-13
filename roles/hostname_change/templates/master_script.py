# Python script for password update on hostname update
import base64
import mysql.connector
import subprocess
import hashlib

password = base64.urlsafe_b64encode("%s.%s" % ('{{new_hostname}}','{{api_user}}'))

cnx = mysql.connector.connect(user='root',host='{{localhost}}',unix_socket='{{unix_socket}}',database='{{database}}')
cursor = cnx.cursor()

query = ("select salt from users where username='{{api_user}}'")

cursor.execute(query)
salt = cursor.fetchone()[0]
passwordsalt = password+salt

subprocess.call(echo -n "import hash" | openssl dgst -sha1)
hashlib_object  = hashlib.sha1(passwordsalt)
hash = print hashlib_object.hexdigest()

query1 = ("update users set password = '%s' where username='{{api_user}}';" % hash)

cursor.execute(query1);
