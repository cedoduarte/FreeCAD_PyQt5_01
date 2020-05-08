from socket import *
import threading

doc = FreeCAD.newDocument()

def startServer():
	host = "localhost"
	port = 12345
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((host, port))
	sock.listen()
	conn, addr = sock.accept()
	conn.sendall("you are connected...".encode("utf-8"))
	while True:
		data = conn.recv(1024)
		if not data:
			break

		#conn.sendall(data)

		data = data.decode("ascii")
		data = data.replace("box(", "")
		data = data.replace(")", "")
		data = data.split(",")		
		boxName = data[0][data[0].index(":")+1:]
		height = data[1][data[1].index(":")+1:]
		length = data[2][data[2].index(":")+1:]
		width = data[3][data[3].index(":")+1:]
		exists = data[4][data[4].index(":")+1:]

		if exists == "True":
			App.setActiveDocument("Unnamed")
			App.ActiveDocument=App.getDocument("Unnamed")
			Gui.ActiveDocument=Gui.getDocument("Unnamed")
			FreeCAD.getDocument("Unnamed").getObject(boxName).Height = height
			FreeCAD.getDocument("Unnamed").getObject(boxName).Length = length
			FreeCAD.getDocument("Unnamed").getObject(boxName).Width = width
			doc.recompute()
			conn.sendall("box modified".encode("utf-8"))
		else:
			App.setActiveDocument("Unnamed")
			App.ActiveDocument=App.getDocument("Unnamed")
			Gui.ActiveDocument=Gui.getDocument("Unnamed")
			box = doc.addObject("Part::Box", boxName)
			FreeCAD.getDocument("Unnamed").getObject(boxName).Height = height
			FreeCAD.getDocument("Unnamed").getObject(boxName).Length = length
			FreeCAD.getDocument("Unnamed").getObject(boxName).Width = width
			doc.recompute()
			conn.sendall("box added".encode("utf-8"))

	conn.sendall("server finished...".encode("utf-8"))

thread = threading.Thread(target=startServer)
thread.start()
print("running server...")