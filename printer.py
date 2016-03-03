import os
import time
from win32com import client
from filemanagement import ClassFile
class doc:
    def printwordDocument(self,folder,filename):
        os.path.join(os.getcwd(), folder, filename)
        word = client.DispatchEx("word.Application")
        word.Visible = False
        filename = os.path.abspath(filename)        
        word.Documents.Open(filename)
        word.ActiveDocument.PrintOut()
        time.sleep(2)
        word.ActiveDocument.Close()
        word.Quit()
        return 
def printing(folder):
    filelist = [x for x in
                os.listdir(folder) if x.endswith('docx')]
    for filename in filelist:        
        inst = doc()
        i = os.path.abspath(folder) +"\\"+ filename
        try:
            inst.printwordDocument(folder,i)
        except:
            pass
    del_obj = ClassFile()
    del_obj.delete_all_files_by_extension(folder,"docx")
        
    return
            
#printing("letters")
