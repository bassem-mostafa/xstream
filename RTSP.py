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

class RTSP(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, str) and self._source.find(f"rtsp://", 0, len(f"rtsp://")) != -1:
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        self._type = "RTSP"
        self._specifications["frame-rate"] = None
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r"]:
            raise ValueError(f"Not supported operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        self._content = cv2.VideoCapture(str(self._source))
        self._specifications["frame-rate"] = self._content.get(cv2.CAP_PROP_FPS)
        self._specifications["frame-width"] = self._content.get(cv2.CAP_PROP_FRAME_WIDTH)
        self._specifications["frame-height"] = self._content.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self._specifications["frame-channels"] = self._content.get(cv2.CAP_PROP_VIDEO_TOTAL_CHANNELS)
        return self._content.isOpened()
    def close(self):
        self._content.release()
        self._content = None
        return True
    def read(self):
        if self._mode not in ["r"]:
            raise RuntimeError(f"Not supported operation `read` for mode `{self._mode}` for stream source `{self._source}`")
        status, frame = self._content.read()
        if not status:
            frame = None
        return frame
    def write(self):
        if self._mode not in []:
            raise RuntimeError(f"Not supported operation `write` for mode `{self._mode}` for stream source `{self._source}`")
        return False

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