import os


class ClassFile(object):
    def __init__(self):
        pass

    def delete_file(self,path):
        if os.path.exists(path):
            try:
                os.remove(path)
                response = ("True", "File deleted")
            except WindowsError, e:
                response = "False", e
        else:
            response = ("False", "File does not exist")
        return response

    def delete_file_from_folder(self, filename, folder):
        return self.delete_file(
            os.path.join(os.getcwd(), folder, filename))

    def search_file(self, filename):
        try:
            if os.path.exists(filename):
                response = (True, "File Exists")
            else:
                response = (False, "File does not Exist")
        except:
            response = (False, "File searching error")
        return response

    def search_all_files_by_extension(self, folder, ext):
        try:
            filelist = [x for x in os.listdir(
                folder) if x.endswith(ext)]
        except WindowsError:
            return False, "Folder cannot be found",[]
        if len(filelist) > 0:
            msg = "Found %d files" % len(filelist)
            response = True, msg, filelist
        else:
            response = False, "No file found",[]
        return response

    def delete_all_files_by_extension(self, folder, ext):
        files=self.search_all_files_by_extension(folder, ext)
        try:
            original_files = len(files[2])
        except IndexError:
            return False,"No files found"
        final_files = 0
        for i in files[2]:
            if self.delete_file_from_folder(i, folder)[0]:
                final_files += 1
        if final_files == 1:
            msg = "Deleted 1 file of %d %s file from %s folder" % (original_files, ext, folder)
            response = (True, msg)
        elif final_files > 1:
            msg = "Deleted %d files of %d %s files from  %s folder" % (final_files, original_files, ext, folder)
            response = True, msg
        else:
            return False, "No files found"
        return response














    
