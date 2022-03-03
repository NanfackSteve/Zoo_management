import mysql.connector as mysql

#Connection au Serveur MySQL
db = mysql.connect(host='localhost', user='sun', password='s')
sql = db.cursor()

#Creation de la BD 'Zoologie'
sql.execute("CREATE DATABASE IF NOT EXISTS Zoologie;")
db.close() #fermeture de connexion a la BD

#Reconnection a la BD 'Zoologie' du Serveur MySQL
db = mysql.connect(host="localhost",user="sun",password="s",database="Zoologie")
sql = db.cursor()

#Creattion de la Table 'Animals' dans la BD 'Zoologie'
sql.execute("""
                CREATE TABLE IF NOT EXISTS Animals (
                                            Record int(15) NOT NULL,
                                            Name varchar(20),
                                            Leg int(255),
                                            Age int(100),
                                            Weight float(5,3),
                                            PRIMARY KEY(Record)
                                            );
            """)

#Creation de la Classe 'Zoologie'
class Zoologie:
    """ Classe Zoologie"""

    animals = list()
    
    def __init__(self):
        """Constructor of Classe Zoologie"""

        self.name = ''

        #on compte le nombre d'animaux dns la BD qu'on affecte a capacity
        sql.execute("select count(Record) from Animals;")
        result = sql.fetchall()
        self.capacity = result[0].__getitem__(0)

        #on charge les donnees de la BD dans la Liste animals[]
        sql.execute("SELECT * FROM Animals;")
        result = sql.fetchall()
        for e in result:
            self.animals.append(list(e))
            
    
    def add_animal(self,animal):
        """"Method for Adding Animal"""

        if(self.capacity < 100):
            #si cet animal est dans la liste on n'ajoute pas et on sort
            if(animal in self.animals):
                return False
            
            #On ajoute dans la Liste d'animaux
            self.animals.append(animal)
            
            #on ajoute dans la BD
            sql.execute("INSERT INTO Animals(Record, Name, Leg, Age, Weight) VALUES(%s, %s, %s, %s, %s);", animal)
            db.commit()

            self.capacity +=1
            return True
        else:
            return False

    def remove_animal(self,enreg):
        """"Method for Remove Animal"""

        i=0
        for element in self.animals:
            #Si l'animal est present dans la Liste on le supprime
            if(enreg in element):
                #Supression Liste
                self.animals.remove(self.animals[i])
                
                #Suppresion dans la BD
                sql.execute("DELETE from Animals where Record='"+str(enreg)+"';")
                db.commit()
                self.capacity -=1
                return True
            i+=1
        return False

    def list_animals(self):
        """"Method for Listing all Animals"""

        if(self.capacity == 0):
            print("\nEmpty Zoo !!! Nothing to print")
            return False
        else:
            sql.execute("SELECT * FROM Animals;")
            rows = sql.fetchall()
            print("+---------------------------------------+")
            print("|Record\t|Name\t|Leg\t|Age\t|Weight\t|")
            print("+---------------------------------------+")
            for row in rows:
                print("  {}\t {}\t {}\t {}\t {}".format(row[0],row[1],row[2],row[3],row[4]))
            return True

    def get_occupation(self):
        """Give the Number of Animals"""

        return self.capacity

    def list_animal(self,enreg):
        """Print Animal by giving is ID Record"""

        for element in self.animals:
            if(enreg in element):
                print("\nInfos about ",enreg," are:")
                print("Name: ",element[1],"Leg: ",element[2]," Age: ",element[3],"Weight: ",element[4])
                return True

        print("\nSorry This Animal is not in The Zoo")
        return False

    def __del__(self):
        """Delete Object and Close DB"""

        print("\nClosing DataBase")
        db.close()

#------- Instanciations de Zoologie et Applications des Methodes --------#

zoo = Zoologie() 
print("\nNbr of animals in the Zoo:",zoo.get_occupation()) #Nombre d'Animaux presents
print(zoo.list_animals())   #Liste des animaux
print(zoo.list_animal(12345)) #Infos sur un Animal Precis

#Ajout des Animaux dans la liste
zoo.add_animal([12337, 'nom1', 4, 1, 4.5])
zoo.add_animal([12347, 'nom2', 2, 1, 20.5])
zoo.add_animal([12345, 'nom3', 4, 1, 10.5])
print("\nNbr of animals in the Zoo: ",zoo.get_occupation()) #Nombre d'Animaux presents

print(zoo.list_animals())   #Liste des animaux
zoo.remove_animal(12347)    #suppresion d'un animal 
print("\nNbr of animals in the Zoo: ",zoo.get_occupation()) #Nombre d'Animaux presents
print(zoo.list_animals())   #Liste des Animaux
del zoo                     #suppresion de l'objet et fermeture de la BD