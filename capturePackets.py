import sys
import subprocess
import time
import os
from os import listdir, walk
from os.path import isfile, join
import pandas as pd


def tcpdump(dir_query, query_path, q_time, q_name, device_ip, iterations):
        #Captura el trafico de red mientras se ejecuta el comando "query_path"
        for i in range(iterations):
            print('Capturando paquetes...')
            capture = subprocess.Popen("sudo timeout " + str(q_time) + " tcpdump -i wlan0 -n host " + str(
                device_ip) + " -w " + dir_query + str(q_name) + str(i) + ".pcap", shell=True, stdout=subprocess.PIPE)
            time.sleep(2)
            
            comm_audio = subprocess.Popen("sudo mpg123 -q " + query_path, shell=True, stdout=subprocess.PIPE)
            
            capture.wait()        
            print('Captura de paquetes finalizado')

 
def generateDirectory(file_name):
        #Crear los directorios donde las capturas de trafico seran guardadas
	query = file_name.split('.',1)[0]
	path_dir = 'pcap/' + query
	if not os.path.exists(path_dir):
		os.mkdir(path_dir)
	return path_dir + '/'
		

def captureData(q_files, comm_path, q_times, q_names, echo_ip, n_iter):
        #Preparacion y captura del trafico de red al ejecutar los comandos de voz en "q_files"
        for i in range(len(q_files)):         
            dir_query = generateDirectory(q_files[i]) 
            tcpdump(dir_query, comm_path + q_files[i], float(q_times[i]), q_names[i].replace(" ", "_") + '.', echo_ip,
              n_iter)
            

def obtainQueries(comm_path):
        #Generar una lista con todos los comandos de voz en el directorio "comm_path"
        q_files = []
        for _,_,files in walk(comm_path):
            for filename in files:
                q_files.append(filename)
                               
        q_files = sorted(q_files, key=str.casefold)
                
        return q_files


def main():
        print('\n######################################################')
        print('##                                                  ##')
        print('##              CAPTURE PACKETS                     ##')
        print('##                                                  ##')
        print('######################################################\n')
        
        '''
        ~Argumentos de entrada~
        #data: path del CSV con el listado de comandos de voz. 
        #comm_path: path donde se encuentran los MP3 de los comandos de voz
        #echo_ip: direccion IP dispositivo Amazon Echo
        #itr: numero de capturas de trafico
        '''
        
        data = pd.read_csv(sys.argv[1])
        list_queries = data['Query']
        list_times = data['Time']

        comm_path = sys.argv[2]
        echo_ip = sys.argv[3]
        itr = int(sys.argv[4])	
        
        #Generar una lista con todos los comandos de voz en el directorio "comm_path"
        q_files = obtainQueries(comm_path)
        
        #Preparacion y captura del trafico de red al ejecutar los comandos de voz en "q_files"
        captureData(q_files, comm_path, list_times, list_queries, echo_ip, itr)


if __name__ == "__main__":
		main()  