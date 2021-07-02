#!/usr/bin/python3
from dotenv import load_dotenv
import getopt
import sys
import os

load_dotenv()
VHOST_DIR_PATH = os.getenv('VHOST_DIR_PATH')


def getFullDomainName(subDomain):
    return subDomain + ".trypypy.com"


def getFileName(subDomain, fullPath=False):
    if fullPath:
        return VHOST_DIR_PATH + "5" + subDomain + ".conf"
    return "5" + subDomain + ".conf"


def createVhostFile(subDomain):
    writeString = f"""<VirtualHost *:80>
	ServerName {getFullDomainName(subDomain)}
	DocumentRoot /var/www/trypypy/root_domain/
	ErrorLog /var/www/trypypy/root_domain/logs/sub-error.log
	CustomLog /var/www/trypypy/root_domain/logs/sub-access.log combined
    RewriteEngine on
    RewriteCond %{{SERVER_NAME}} ={getFullDomainName(subDomain)}
    RewriteRule ^ https://%{{SERVER_NAME}}%{{REQUEST_URI}} [END,NE,R=permanent]
</VirtualHost>"""
    f = open(getFileName(subDomain, fullPath=True), "w")
    f.write(writeString)
    f.close()


def exCmd(command):
    return os.system(command) == 0


def reloadApache():
    return exCmd('systemctl reload apache2')


def createVhost(subDomain):
    createVhostFile(subDomain)
    exCmd(f'a2ensite {getFileName(subDomain)}')
    exCmd(f'certbot --apache -n -d {getFullDomainName(subDomain)}')
    reloadApache()


def deleteVhost(subDomain):
    exCmd(f'a2dissite 5{subDomain}*')
    exCmd(f'rm {VHOST_DIR_PATH}5{subDomain}*')
    exCmd(f'certbot delete --cert-name {subDomain}.trypypy.com')
    reloadApache()


def deleteVhosts(subDomains):
    subDomainsArray = subDomains.split(',')
    for sd in subDomainsArray:
        if sd == "":
            continue
        deleteVhost(sd)


def instructions():
    return """
            
Usage: ./vhost-creator.py -dc <subDomain>
c: create
d: delete [, separated subDomains]
            
"""


def runScript():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:d:")
        if not opts:
            print(instructions())
        for opt, arg in opts:
            if opt == '-c':
                createVhost(subDomain=arg)
            elif opt == '-d':
                deleteVhosts(subDomains=arg)
    except getopt.GetoptError as err:
        print('Index error: ', err)
        print('please try again')


if __name__ == "__main__":
    runScript()
