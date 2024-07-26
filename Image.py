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

## #############################################################################
## #### Control Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Import(s) ##############################################################
## #############################################################################

from xstream import cv2
from xstream import Path
from xstream import _Stream

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

class Image(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, (str, Path)):
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        extension = Path(self._source).suffix[1:].lower()
        if extension not in ["jpg", "jpeg", "jpe", "bmp", "png", "pbm", "pgm", "ppm", "pxm", "pnm"]:
            raise RuntimeError(f"Not supported {self.__class__.__name__} source `{self._source}` with extension `{extension}`")
        self._type = "Media/Image"
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r", "w"]:
            raise ValueError(f"Not supported {self.__class__.__name__} operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        status = Path(self._source).exists()
        if self._mode in ["w"]:
            status = True
        return status
    def close(self):
        # Nothing to be done
        return True
    def read(self):
        if self._mode not in ["r"]:
            raise RuntimeError(f"Not supported operation `read` for mode `{self._mode}` for stream source `{self._source}`")
        self._content = cv2.imread(str(self._source))
        if self._content is not None:
            self._specifications["frame-width"] = self._content.shape[1]
            self._specifications["frame-height"] = self._content.shape[0]
            self._specifications["frame-channels"] = self._content.shape[2] if len(self._content.shape) > 2 else 1
        return self._content
    def write(self, frame):
        if self._mode not in ["w"]:
            raise RuntimeError(f"Not supported operation `write` for mode `{self._mode}` for stream source `{self._source}`")
        self._content = frame
        self._specifications["frame-width"] = self._content.shape[1]
        self._specifications["frame-height"] = self._content.shape[0]
        self._specifications["frame-channels"] = self._content.shape[2] if len(self._content.shape) > 2 else 1
        if not cv2.imwrite(str(self._source), self._content):
            raise RuntimeWarning(f"Couldn't complete operation `write` for mode `{self._mode}` for stream source `{self._source}`")
        return True

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