#!/usr/bin/python3
import os
import sys
import getopt
from dotenv import load_dotenv

load_dotenv()
VHOST_DIR_PATH = os.getenv('VHOST_DIR_PATH')

# name will start from 5{domain}.conf
# create vhost file


def createVhost(domainName):
    fileName = VHOST_DIR_PATH + \
        "5" + domainName + ".conf"
    writeString = f"""<VirtualHost *:80>
	ServerName {domainName + ".trypypy.com"}
	DocumentRoot /var/www/trypypy/root_domain/
	ErrorLog /var/www/trypypy/root_domain/logs/sub-error.log
	CustomLog /var/www/trypypy/root_domain/logs/sub-access.log combined
    RewriteEngine on
    RewriteCond %{{SERVER_NAME}} ={domainName + ".trypypy.com"}
    RewriteRule ^ https://%{{SERVER_NAME}}%{{REQUEST_URI}} [END,NE,R=permanent]
</VirtualHost>"""
    f = open(fileName, "w")
    f.write(writeString)
    f.close()


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:")
        if not opts:
            print('Usage: ./vhost-creator.py -d <domainName>')
        for opt, arg in opts:
            if opt == '-d':
                createVhost(arg)
                sys.exit()
    except getopt.GetoptError as err:
        print('Index error: ', err)
        print('please try again')

# enable site
    # a2ensite filename

# test vhost file
    # should be done along with creation of file
# generate ssl
# add https redirect rule inside vhost
