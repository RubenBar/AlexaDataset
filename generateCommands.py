import sys
import boto3
import pandas as pd


def voiceCommand():
        #Escoger la voz para los comandos. 
	while True:
		print('¿Que voz quieres utilizar? Indique su numero.')
		try:      	
			voz = int(input('1) Conchita\n2) Lucia\n3) Enrique\n'))
		
		except ValueError:            
			print("\nError! Opcion no valida. Intentelo de nuevo.\n")

		else:
			if voz == 1:
				print('Se utilizara la voz de Conchita\n')	
				return 'conchita'			
			elif voz == 2:
				print('Se utilizara  la voz de Lucia\n')
				return 'lucia'
			elif voz == 3:
				print('Se utilizara  la voz de Enrique\n')		
				return 'enrique'
			else:
				print('\nError! Numero no valido.\n')	


def createCommand(voz):
        #Generar los comandos de voz (mp3) 
	list_comm = pd.read_csv(sys.argv[1])
	l_comm = list_comm['Query']    

	polly_client = boto3.Session(
                aws_access_key_id= '-', #RELLENAR: indicar el ID de la cuenta AWS.                     
		aws_secret_access_key='-', #RELLENAR: indicar la clave de acceso AWS.          
		region_name='us-west-2').client('polly')

	for comm in l_comm:
		c_output = comm.replace(" ", "_")   	
		
		if voz == 'conchita':			
			m_output = 'comandos_voz/conchita/' + c_output + ".mp3"
			response = polly_client.synthesize_speech(TextType='ssml', Text='<speak><break time="300ms"/>' + 'Alexa,<break time="300ms"/> ' +  comm + '</speak>', OutputFormat='mp3', VoiceId='Conchita')
			
		elif voz == 'lucia':
			m_output = 'comandos_voz/lucia/' + c_output + ".mp3"
			response = polly_client.synthesize_speech(TextType='ssml', Text='<speak><break time="300ms"/>' + 'Alexa,<break time="300ms"/> ' +  comm + '</speak>', OutputFormat='mp3', VoiceId='Lucia')

		elif voz == 'enrique':
			m_output = 'comandos_voz/enrique/' + c_output + ".mp3"
			response = polly_client.synthesize_speech(TextType='ssml', Text='<speak><break time="300ms"/>' + 'Alexa,<break time="300ms"/> ' +  comm + '</speak>', OutputFormat='mp3', VoiceId='Enrique')

		with open(m_output, 'wb') as file:
                        stream = response.get('AudioStream')
                        data = stream.read()
                        file.write(data)
                        file.close()
            			
	print('Audios generados')


def main():	
	print('\n######################################################')
	print('##                                                  ##')
	print('##              GENERATE COMMANDS MP3               ##')
	print('##                                                  ##')
	print('######################################################\n')

	#Escoger la voz para los comandos.
	voz = voiceCommand()
	
	#Generar los comandos de voz (mp3) 
	createCommand(voz)	
    

if __name__ == "__main__":
    main()