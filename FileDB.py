import os

class FileDB(object):
    def __init__(self , location):
        self.location = os.path.expanduser(location)
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        

    def set(self , key , value):
        try:
            with open(self.location+self._key2file(key), 'w') as f:
                f.write(value)
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def get(self , key):
        if os.path.exists(self.location+self._key2file(key)):
            with open(self.location+self._key2file(key)) as f:
                return f.read()
        else:
            return False

    def _key2file(self, s):
        return s.replace('/','').replace(':','').replace('.','')+'.txt'
        
        
        