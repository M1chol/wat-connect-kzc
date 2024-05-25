from tinydb import TinyDB, Query
import datetime

DB_POSTS_LINK = 'backend\databases\posts.json'
DB_P_O_I_LINK = 'backend\databases\pointsofintrest.json'


class ElementType():
    def __init__(self) -> None:
        pass
    def UpdateParam(self, **kwargs):
        for paramName, newVal in kwargs.items():
            if str(paramName) != 'ID' and hasattr(self, paramName):
                setattr(self, paramName, newVal)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{paramName}'")


class PostElement(ElementType):
    def __init__(self, authorID: str) -> None:
        self.ID = 0
        self.txt = ''
        self.authorID = authorID;
        self.date = str(datetime.datetime.now())
        self.experimentationDate = str(datetime.datetime.now())
        self.iconID = 0
        self.like = 0
    
class DBPostHandling():
    def __init__(self) -> None:
        self.db = TinyDB(DB_POSTS_LINK)
    
    def addEle(self, Element: PostElement) -> int:
        lastID = self.__lastID()
        self.db.insert({'ID': lastID+1, 'txt': Element.txt, 'authorID': Element.authorID,
                        'date': Element.date, 'iconID': Element.iconID, 
                        'experimentationDate': Element.experimentationDate,
                        'like': 0})
        return lastID+1
    
    def getAll(self) -> list:
        return self.db.all()

    def __clearData(self) -> None:
        self.db.truncate()
    
    def __lastID(self) -> int:
        last = 0;
        for ele in iter(self.db):
            if ele['ID'] > last:
                last = ele['ID']
        return last

#!ODZIELANIE POI OD POST
class POIElement(ElementType):
    def __init__(self) -> None:
        self.ID = 0
        self.lat = float
        self.lng = float
        self.name = ''
        self.iconID = 0
        self.posts = []
class DBPOIHandling():
    def __init__(self) -> None:
        self.db = TinyDB(DB_P_O_I_LINK)

    def _addEle(self, Element: POIElement) -> int:
        self.db.insert({'ID': self.__lastID()+1, 'lat': Element.lat, 'lng': Element.lng, 
                        'name': Element.name, 'iconID': Element.iconID, 'posts': []})

    def addPost(self, PlaceID: int , PostID: int):
        database = Query()
        place = self.db.get(database.ID == PlaceID)
        if place is not None:
            posts = place.get('posts', [])
            posts.append(PostID)
            self.db.update({'posts': posts}, database.ID == PlaceID)
        else:
            # Obsłuż sytuację, gdy PlaceID nie istnieje w bazie danych
            print("PlaceID not found in database.")

    def __lastID(self) -> int:
        last = 0;
        for ele in iter(self.db):
            if ele['ID'] > last:
                last = ele['ID']
        return last

    def getAll(self) -> list:
        return self.db.all()

    def getPost(self, PlaceID: int) -> list:
        database = Query()
        place = self.db.get(database.ID == PlaceID)
        if place is not None:
            posts = place.get('posts', [])
            return posts
        else:
            return [0]
        
#!ODZIELENIE POI OD USERPlACES
#TODO dokończyć userplaces
class UPElement(ElementType):
    def __init__(self, authorID: str) -> None:
        self.USERID = 0
        self.fav = []

if __name__ == '__main__':
    DBPostHandler = DBPostHandling()
    DBPOIHandler = DBPOIHandling()
    
    # ele1 = PostElement("twoja stara")
    # ele1.ID = ele1.UpdateParam(txt = 'WIeLka imba')
    # DBPostHandler.addEle(ele1)

    # ele2 = POIElement()
    # ele2.ID = ele2.UpdateParam(x=13, y=14, name='Hinczyk')
    # DBPOIHandler._addEle(ele2)
    # ele2.ID = ele2.UpdateParam(x=50, y=321, name='Tajne okopy drużyny 25')
    # DBPOIHandler._addEle(ele2)
    # ele2.ID = ele2.UpdateParam(x=2131250, y=5621, name='Składowisko portek Rektora')
    # DBPOIHandler._addEle(ele2)
    # ele2.ID = ele2.UpdateParam(x=10, y=31, name='Winda skrzydło któreś tam')

    # DBPOIHandler.addPost(3, 1)

    print(DBPOIHandler.getAll())