from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#Import CRUD operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

#Create session and connec the db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler): #This class extends from BaseHTTPRequestHandler

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                result = session.query(Restaurant.name).all()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "<br><br>"
                for rname in result:
#                    print rname[0]
                    idchecker = session.query(Restaurant.id).filter_by(name = rname[0])
                    for items in idchecker:
                        theid = items[0]
                    output += rname[0] + "<br>"
                    output += "<a href=/restaurants/"+str(theid)+"/edit>Edit</a><br>"
                    output += "<a href=#>Delete</a><br>"                    
                    output += "<br>"
                output += "</body></html>"
                self.wfile.write(output)
#                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "</h2><input name='newRestaurantName' type='text' placeholder = 'New restaurant name'>"
                output += "<input type='submit' value='Create'></form>"        
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

#            print "self.path ==> ", self.path[13:].find('/')
            nextslash = self.path[13:].find('/')
            if nextslash != -1: 
                string = self.path[13:13+nextslash]
                print "Integer of this string is : ", int(string)
#                if int(string) == True:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Rename the Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='%s'>" %self.path 
                output += "</h2><input name='renamed' type='text' placeholder = 'New restaurant name'>"
                output += "<input type='submit' value='Rename'></form>"        
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
 
        except IOError: 
            self.send_error(404, "File Not Found %s" %self.path) 

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
            nextslash = self.path[13:].find('/')
            if nextslash != -1 and int(self.path[13:13+nextslash]):
#                print "Integer following"
                string = self.path[13:13+nextslash]
                print "string is ", int(string)

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('renamed')
                    print "The message content was : ", messagecontent[0]

                    newName = session.query(Restaurant).filter_by(id = int(string)).one()
                    newName.name = messagecontent[0]
                    session.add(newName)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()                
                   
        except:
            pass



def main ():
    try:
        port = 8080
        server = HTTPServer(('',port),webServerHandler)
        #Host is left as empty string for now
        print "Web server running on port %s" %port
        server.serve_forever()
        
    
    except KeyboardInterrupt:
        print "^C entered, stopping web server ... "
        server.socket.close()

if __name__ == '__main__':
    main()
