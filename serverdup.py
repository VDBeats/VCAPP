import socket,cv2, pickle,struct,imutils
from cryptography.fernet import Fernet

#Generate key and store in a file, create instance
key = Fernet.generate_key()#generate 256-bit key
fernet = Fernet(key) #create instance with key as a constructor arguement
with open('Key.key','wb') as f:
    f.write(key) #writing key onto a .key file



# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture(0)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = imutils.resize(frame,width=500)
			a = pickle.dumps(frame) #converting image data to hexadecimal 
			a=fernet.encrypt(a) #encrypting hexa text
			message = struct.pack("Q",len(a))+a #packing datastream into packets
			client_socket.sendall(message)#sending encrypted data to client
			
			cv2.imshow('TRANSMITTING VIDEO',frame)#display video
			key = cv2.waitKey(1) & 0xFF
			if key ==ord('q'):
				client_socket.close()
