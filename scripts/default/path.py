#-# Importing Packages #-#
import os

#-# Get Folder Path Location #-#
#__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = os.getcwd()

class FilePath(str):

    def __new__(cls, name: str, folder, extension) -> None:

        #self.name, self.extension, self.folder = name, extension, folder
        
        if folder:

            return super().__new__(cls, __location__ + "/" + folder + "/" + name + "." + extension)
        
        else:

            return super().__new__(cls, __location__ + "/" + name + "." + extension)       

class ImagePath(FilePath):
    
    def __new__(cls, name: str, folder=None, extension="png") -> None:

        if folder:

            return super().__new__(cls, name, "images/" + folder, extension)
        
        else:

            return super().__new__(cls, name, "images/", extension)

class FontPath(FilePath):
    
    def __new__(cls, name: str, folder=None, extension="ttf") -> None:

        if folder:

            return super().__new__(cls, name, "fonts/" + folder, extension)
        else:

            return super().__new__(cls, name, "fonts/", extension)
    
class SoundPath(FilePath): 
    
    def __new__(cls, name: str, folder=None, extension="ogg") -> None:

        if folder:

            return super().__new__(cls, name, "sounds/" + folder, extension)
        else:

            return super().__new__(cls, name, "sounds/", extension)
