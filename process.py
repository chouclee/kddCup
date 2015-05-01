__author__ = 'chouclee'

import sys


protocol_dict = {}
service_dict = {}
flag_dict = {}
attack_dict = {"back":"dos","buffer_overflow":"u2r","ftp_write":"r2l",
               "guess_passwd":"r2l","imap":"r2l","ipsweep":"probe",
               "land":"dos","loadmodule":"u2r","multihop":"r2l",
               "neptune":"dos","nmap":"probe","perl":"u2r","phf":"r2l",
               "pod":"dos","portsweep":"probe","rootkit":"u2r",
               "satan":"probe","smurf":"dos","spy":"r2l","teardrop":"dos",
               "warezclient":"r2l","warezmaster":"r2l","normal":"normal"}
new_attack_dict = {"saint":"probe","mscan":"probe","apache2":"dos","snmpgetattack":"r2l",
                   "processtable":"dos","httptunnel":"u2r","ps":"u2r","mailbomb":"dos",
                   "sendmail":"r2l","named":"r2l","snmpguess":"r2l","xlock":"r2l",
                   "xsnoop":"r2l","worm":"r2l","sqlattack":"u2r","xterm":"u2r",
                   "udpstorm":"dos"}
old_attack = {"dos", "u2r", "r2l", "probe", "normal"}

def toValue(dictionary, s):
    if dictionary.get(s, None) is None:
        dictionary[s] = len(dictionary) + 1
    return str(dictionary[s])


header = 'duration,protocol_type,service,flag,src_bytes,dst_bytes,' \
    'land,wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,'\
    'root_shell,su_attempted,num_root,num_file_creations,num_shells,num_access_files,'\
    'num_outbound_cmds,is_host_login,is_guest_login,count,srv_count,serror_rate,'\
    'srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,'\
    'srv_diff_host_rate,dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,'\
    'dst_host_diff_srv_rate,dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,'\
    'dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_rerror_rate,'\
    'dst_host_srv_rerror_rate,attack_type'

def process(instance):
    instance = instance.strip()
    instance = instance.split(",")
    instance[1] = toValue(protocol_dict, instance[1])
    instance[2] = toValue(service_dict, instance[2])
    instance[3] = toValue(flag_dict, instance[3])
    instance.pop(-1)
    instance[-1] = attack_dict.get(instance[-1], instance[-1])
    return instance

def generateCSV(txt_file, csv_file):
    with open(txt_file, 'r') as f, open(csv_file, 'w') as w:
        lines = f.readlines()
        w.write(header + "\n")
        for line in lines:
            line = process(line)
            w.write(",".join(line))
            w.write("\n")

generateCSV(sys.argv[1], 'train.csv')
generateCSV(sys.argv[2], 'train20Percent.csv')

with open(sys.argv[3], 'r') as f:
    lines = f.readlines()
    with open('testWithoutNewAttackTypes.csv', 'w') as wwo, \
        open('testNewAttackTypes.csv', 'w') as wnew, \
        open('test.csv', 'w') as w, \
        open('golden.csv', 'w') as wg:
        wwo.write(header + "\n")
        wnew.write(header + "\n")
        w.write(header + "\n")
        wg.write("attack_type\n")
        for line in lines:
            line = process(line)
            w.write(",".join(line))
            w.write("\n")
            wg.write(line[-1] + "\n")
            if line[-1] in old_attack:
                wwo.write(",".join(line))
                wwo.write("\n")
            else:
                line[-1] = new_attack_dict[line[-1]]
                wnew.write(",".join(line))
                wnew.write("\n")