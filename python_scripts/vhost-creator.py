#!/usr/bin/python3
from dotenv import load_dotenv
import getopt
import sys
import os

#  loading dot env file for environment vars
load_dotenv()
#  getting required vars from .env
VHOST_DIR_PATH = os.getenv('VHOST_DIR_PATH')

# name will start from 5{domain}.conf
# create vhost file


def getFullDomainName(subDomain):
    return subDomain + ".trypypy.com"


def getFileName(subDomain, fullPath=False):
    if fullPath:
        return VHOST_DIR_PATH + "5" + subDomain + ".conf"
    return "5" + subDomain + ".conf"


def createVhost(subDomain):
    # creating string for vhost file
    writeString = f"""<VirtualHost *:80>
	ServerName {getFullDomainName(subDomain)}
	DocumentRoot /var/www/trypypy/root_domain/
	ErrorLog /var/www/trypypy/root_domain/logs/sub-error.log
	CustomLog /var/www/trypypy/root_domain/logs/sub-access.log combined
    RewriteEngine on
    RewriteCond %{{SERVER_NAME}} ={getFullDomainName(subDomain)}
    RewriteRule ^ https://%{{SERVER_NAME}}%{{REQUEST_URI}} [END,NE,R=permanent]
</VirtualHost>"""

    # creating and writing to vhost file
    f = open(getFileName(subDomain, fullPath=True), "w")
    f.write(writeString)
    f.close()


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:")
        if not opts:
            print('Usage: ./vhost-creator.py -d <domainName>')
        for opt, arg in opts:
            if opt == '-d':
                print('Creating vhost file')
                subDomain = arg
                createVhost(subDomain)
                print('vhost file created: ' +
                      getFileName(subDomain, fullPath=True))
                print('full domain name: ' + getFullDomainName(subDomain))

                # shell command starts

                # enabling apache 2 site
                ensiteStatus = os.system(f'a2ensite {getFileName(subDomain)}')
                if ensiteStatus == 0:
                    print('apache2 site enabled')

                    # getting ssl certificate
                    certificateStatus = os.system(
                        f'certbot --apache -n -d {getFullDomainName(subDomain)}')
                    if certificateStatus == 0:
                        print('SSL certificate issued')

                        # reloading apache2
                        reloadStatus = os.system('systemctl reload apache2')
                        if reloadStatus == 0:
                            print('Server is reloaded')
                        else:
                            print('There was error reloading apache2 server')
                            sys.exit()
                    else:
                        print('There was error issuing SSL certificate')
                        sys.exit()
                else:
                    print('there was problem wit a2ensite command')
                    sys.exit()

                # shell command ends

                sys.exit()
    except getopt.GetoptError as err:
        print('Index error: ', err)
        print('please try again')
