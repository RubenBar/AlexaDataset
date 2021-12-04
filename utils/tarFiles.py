import sys
import tarfile
import os.path


def tar_files(output_filename, pcap_path):
        #Comprime todos los ficheros de "pcap_path" en "output_filename.tar.gz"
        with tarfile.open(output_filename, "w:gz") as tar:
                tar.add(pcap_path, arcname=os.path.basename(pcap_path))


def list_dir(path):
        #Lista todos los ficheros que se encuentren en el directorio "path"
	list_files = []
	q_files = os.listdir(path)
	list_files.extend(map(lambda f: os.path.join(path, f), q_files))	
	return list_files


def main():
	print('\n######################################################')
	print('##                                                  ##')
	print('##                 COMPRESS DATA                    ##')
	print('##                                                  ##')
	print('######################################################\n')
	
    '''
    ~Argumentos de entrada~
    #path: directorio donde se encuentran los PCAP 
    '''    
    
	path = sys.argv[1]    
	l_q = list_dir(path)
       
	for query in l_q:
            print("\nQUERY: ", query)
            name = os.path.splitext(query)[0]
            name = name.replace('_', '')
            if name.endswith('?'):
                tar_files(name[:-1]+".tar.gz", query)
            else:
                tar_files(name+".tar.gz", query)
            
            	
if __name__ == "__main__":
		main()  