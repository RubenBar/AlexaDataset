import sys
import os
import shutil

def rename_files(list_files, path, name):
        #Renombra los ficheros: command.index.pcap
        index = 0
        for file in list_files:
            os.rename(file, path+name+"."+str(index)+".pcap")
            index = index + 1


def move_files(source_dir, target_dir):
        #Mueve todos los ficheros del directorio "source_dir" a "target_dir"
        file_names = os.listdir(source_dir)            
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)


def list_dir(path):
        #Lista todos los ficheros que se encuentren en el directorio "path"
	list_files = []
	q_files = os.listdir(path)
	list_files.extend(map(lambda f: os.path.join(path, f), q_files))	
	return list_files


def main():
	print('\n######################################################')
	print('##                                                  ##')
	print('##                  RENAME DATA                     ##')
	print('##                                                  ##')
	print('######################################################\n')

    '''
    ~Argumentos de entrada~
    #path: directorio donde se encuentran los PCAP
    '''
	
	path = sys.argv[1]    
	l_q = list_dir(path)
       
	for query in l_q:
            name = os.path.splitext(query)[0]
            name = name.split("/")
            name = name[2]
            
            l_f = list_dir(query)
            os.mkdir(path+name+"/new/")
            
            rename_files(l_f, path+name+"/new/", name)
            
            move_files(path+name+"/new/", path+name+"/")
            os.rmdir(path+name+"/new/")            
   
	
if __name__ == "__main__":
		main()  