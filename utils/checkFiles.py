import sys
from pathlib import Path
import os 
import subprocess

def check_correct(pcap_path, echo_ip):
        #Comprueba el tamaño de informacion transmitida entre el dispositivo Amazon Echo (echo_ip) y Amazon Voice Service.
        #Si el numero de bytes transmitidos es null o menor a 1000B, devuelve False.
        #En caso contrario, devuelve True.

        tcpComm = subprocess.Popen("sudo tcptrace -l --csv '-fhostaddr==" + echo_ip + "&& (hostaddr==52.95.121.5 || hostaddr==52.95.117.89 || hostaddr==52.95.122.231 || hostaddr==52.95.119.186 || hostaddr==52.95.115.208 || hostaddr==52.95.113.144)' " + str(pcap_path) + ' | tail -n +10', \
                stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        stdout = tcpComm.communicate()

        all_val = [x.strip() for x in stdout[0].split(',')]    		
        values_split = all_val[110:112]  

        try:
            if all_val[90] != "192.168.4.18":
                values_split_new = []
                for i in range(0,2,2):
                    values_split_new.append(values_split[i+1])
                    values_split_new.append(values_split[i])
                if int(values_split_new[1]) < 1000:
                    return False
                else:
                    return True
                
            else:
                if int(values_split[1]) < 1000:            
                    return False
                else:          
                    return True
        except:
            return False


def list_dir(path):
    #Lista todos los ficheros del directorio "path"
	list_files = []
	q_files = os.listdir(path)
	list_files.extend(map(lambda f: os.path.join(path, f), q_files))	
	return list_files


def main():
	print('\n######################################################')
	print('##                                                  ##')
	print('##                   CHECK DATA                     ##')
	print('##                                                  ##')
	print('######################################################\n')
	
    '''
    ~Argumentos de entrada~
    #path: directorio donde se encuentran los PCAP a comprobar
    #echo_ip: direccion IP dispositivo Amazon Echo
    '''
    
	path = sys.argv[1]   
	echo_ip = sys.argv[2]  
	l_q = list_dir(path)
       
	for query in l_q:
            print("\nCOMANDO: ", query)
            l_f = list_dir(query)
            
            for file in l_f:          
                res = check_correct(file, echo_ip)                
                if res == False:
                    print("Removed: ", file)
                    os.remove(file)    
	
if __name__ == "__main__":
		main()  