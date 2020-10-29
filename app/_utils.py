import PyPDF2
import re

class SearchFile:
     def search(self, file_path, search_term, **kwargs):
        for file in file_path:
            try:
                object = PyPDF2.PdfFileReader(file_path)
                num_pages = object.getNumPages()
                for i in range(0, num_pages):
                    page_obj = object.getPage(i)
                    text = page_obj.extractText() 
                    res = re.search(search_term, text)
                    if rse:
                        return file_path
                    else:
                        return False


            except Exception as e:
                logger.error(f'Error while extract power point {file_path}: {e}')
            return False