## #############################################################################
## #### Copyright ##############################################################
## #############################################################################

'''
Copyright 2024 BaSSeM

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

## #############################################################################
## #### Description ############################################################
## #############################################################################

'''
X-Stream class wraps various stream sources into unified interface
'''

## #############################################################################
## #### Control Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Import(s) ##############################################################
## #############################################################################

from xstream import Path

from xstream import _Stream
from xstream import _Camera
from xstream import _RTSP
from xstream import _HTTP
from xstream import _HTTPS
from xstream import _Image
from xstream import _Video

## #############################################################################
## #### Private Type(s) ########################################################
## #############################################################################

## #############################################################################
## #### Private Method(s) Prototype ############################################
## #############################################################################

## #############################################################################
## #### Private Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Private Method(s) ######################################################
## #############################################################################

## #############################################################################
## #### Public Method(s) Prototype #############################################
## #############################################################################

## #############################################################################
## #### Public Type(s) #########################################################
## #############################################################################

class XStream:
    def __init__(self, source):
        self._stream = _Stream(source) # Abstract Stream
        if isinstance(source, int):
            self._stream = _Camera(source)
        elif isinstance(source, str) and source.find(f"rtsp://", 0, len(f"rtsp://")) != -1:
            self._stream = _RTSP(source)
        elif isinstance(source, str) and source.find(f"http://", 0, len(f"http://")) != -1:
            self._stream = _HTTP(source)
        elif isinstance(source, str) and source.find(f"https://", 0, len(f"https://")) != -1:
            self._stream = _HTTPS(source)
        elif isinstance(source, (str, Path)):
            extension = Path(source).suffix[1:].lower()
            if extension in ["jpg", "jpeg", "jpe", "bmp", "png", "pbm", "pgm", "ppm", "pxm", "pnm"]:
                self._stream = _Image(source)
            elif extension in ["mp4", "avi"]:
                self._stream = _Video(source)
    def __iter__(self):
        return self._stream.__iter__()
    def __next__(self):
        return self._stream.__next__()
    def __repr__(self):
        return self._stream.__repr__()
    def open(self, mode="r"):
        return self._stream.open(mode)
    def read(self):
        return self._stream.read()
    def write(self, frame):
        return self._stream.write(frame)
    def close(self):
        return self._stream.close()

## #############################################################################
## #### Public Method(s) #######################################################
## #############################################################################

## #############################################################################
## #### Public Variable(s) #####################################################
## #############################################################################

## #############################################################################
## #### Main ###################################################################
## #############################################################################

if __name__ == "__main__":
    ...

## #############################################################################
## #### END OF FILE ############################################################
## #############################################################################