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
VideoStream class wraps various stream sources into unified interface
'''

## #############################################################################
## #### Control Variable(s) ####################################################
## #############################################################################

## #############################################################################
## #### Import(s) ##############################################################
## #############################################################################

if __name__ == "__main__":
    print(f"*"*80)
    print(f"If encountered any error related to `pafy`")
    print(f"\tmake sure you've installed both `pafy` and `youtube-dl`")
    print(f"\tusing `python3 -m pip install -U youtube-dl pafy` command")
    print(f"Also, refer to the following link(s)")
    print(f"- `https://stackoverflow.com/a/75602237`")
    print(f"- `https://github.com/mps-youtube/pafy/pull/288#issuecomment-812841914`")
    print(f"- `https://stackoverflow.com/a/75504772`")
    print(f"*"*80)
    print(f"\n"*3)

import cv2
import pafy
from io import StringIO
from pathlib import Path

## #############################################################################
## #### Private Type(s) ########################################################
## #############################################################################

class _Stream:
    '''
    Abstract Stream interface
    '''
    def __init__(self, source):
        '''
        Initializes the stream
        args:
            source: represents the source path/link/index/...etc of the stream
        returns:
            a stream instance
        '''
        self._source = source           # origin source, could be path, url, index, ...etc
        self._type = None               # detected type, could be image, video, camera, rtsp, https, ...etc
        self._mode = None               # working mode, could be read, write, ...etc
        self._content = None            # content descriptor, handle for actual stream operations
        self._specifications = dict()   # specifications, could be any related specification ex: frame rate, number of frames, frame size, ...etc
    def open(self, mode="r"):
        '''
        Opens the stream in specified mode
        args:
            mode: represents the mode for which the stream shall be opened for (default = 'r': for read-only)
        returns:
            True on a successful opening, False otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `open` for stream source `{self._source}`")
        return False
    def close(self):
        '''
        Closes the stream
        returns:
            True on a successful closing, False otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `close` for stream source `{self._source}`")
        return False
    def read(self):
        '''
        Reads a frame from the stream
        returns:
            a frame on success, None otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `read` for stream source `{self._source}`")
        return None
    def write(self, frame):
        '''
        Writes a frame into the stream
        args:
            frame: represents the frame for which to be written into the stream
        returns:
            True on success, False otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `write` for stream source `{self._source}`")
        return False
    def get(self, property):
        '''
        Gets specified property value of the stream
        args:
            property: represents the property for which to retrieve its value
        returns:
            property value on success, None otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `get` for stream source `{self._source}`")
        return None
    def set(self, property, value):
        '''
        Sets specified property value of the stream to specified value
        args:
            property: represents the property for which to set its value
            value: represents the value to be set for the specified property
        returns:
            True on success, False otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `set` for stream source `{self._source}`")
        return False
    def __repr__(self):
        '''
        Describes the stream
        returns:
            a string that describes the stream
        '''
        text = StringIO()
        print(f"{self.__class__.__name__} Attributes:", file=text)
        for key, value in self.__dict__.items():
            print(f"...\t{str(key):20s}: `{value}`", file=text)
        return text.getvalue()
    def __iter__(self):
        '''
        Gets an iterator for the stream
        returns:
            a stream iterator
        '''
        return self
    def __next__(self):
        '''
        Gets next frame of the iterator for the stream
        returns:
            next frame of the iterator
        '''
        frame = self.read()
        if frame is None:
            raise StopIteration()
        return frame
    def __getattr__(self, name):
        '''
        Controling the stream attributes' getting access
        returns:
            value of stream attribute if exists, exception otherwise
        '''
        if name in []:
            ... # TODO
        return super().__getattr__(name)
    def __setattr__(self, name, value):
        '''
        Controling the stream attributes' setting access
        '''
        if name in []:
            ... # TODO
        super().__setattr__(name, value)

class _Camera(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, (int,)):
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        self._type = "Camera"
        self._specifications["frame-rate"] = None
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r"]:
            raise ValueError(f"Not supported operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        self._content = cv2.VideoCapture(int(self._source))
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

class _RTSP(_Stream):
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

class _HTTP(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, str) and self._source.find(f"http://", 0, len(f"http://")) != -1:
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        self._type = "HTTP"
        self._specifications["frame-rate"] = None
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r"]:
            raise ValueError(f"Not supported operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        self._content = cv2.VideoCapture(pafy.new(str(self._source)).getbest(preftype="mp4").url)
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

class _HTTPS(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, str) and self._source.find(f"https://", 0, len(f"https://")) != -1:
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        self._type = "HTTPS"
        self._specifications["frame-rate"] = None
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r"]:
            raise ValueError(f"Not supported operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        self._content = cv2.VideoCapture(pafy.new(str(self._source)).getbest(preftype="mp4").url)
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
    
class _Image(_Stream):
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

class _Video(_Stream):
    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, (str, Path)):
            raise RuntimeError(f"Not supported {self.__class__.__name__} source-type `{type(self._source)}`")
        extension = Path(self._source).suffix[1:].lower()
        if extension not in ["mp4", "avi"]:
            raise RuntimeError(f"Not supported {self.__class__.__name__} source `{self._source}` with extension `{extension}`")
        self._type = "Media/Video"
        self._specifications["frame-rate"] = None
        self._specifications["frame-count"] = None
        self._specifications["frame-width"] = None
        self._specifications["frame-height"] = None
        self._specifications["frame-channels"] = None
    def open(self, mode="r"):
        if mode not in ["r", "w"]:
            raise ValueError(f"Not supported operation `open` for mode `{mode}` for stream source `{self._source}`")
        self._mode = mode
        if self._mode in ["r"]:
            self._content = cv2.VideoCapture(str(self._source))
            self._specifications["frame-rate"] = self._content.get(cv2.CAP_PROP_FPS)
            self._specifications["frame-count"] = self._content.get(cv2.CAP_PROP_FRAME_COUNT)
            self._specifications["frame-width"] = self._content.get(cv2.CAP_PROP_FRAME_WIDTH)
            self._specifications["frame-height"] = self._content.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._specifications["frame-channels"] = self._content.get(cv2.CAP_PROP_VIDEO_TOTAL_CHANNELS)
        elif self._mode in ["w"]:
            # TODO Handle un-set required specifications
            self._content = cv2.VideoWriter(
                                           filename = str(self._source),
                                           fourcc = cv2.VideoWriter_fourcc(*"mp4v"),
                                           fps = self._specifications["frame-rate"],
                                           frameSize = (self._specifications["frame-width"], self._specifications["frame-height"]),
                                           )
        return self._content.isOpened()
    def close(self):
        self._content.release()
        self._content = None
    def get(self, **kwarg):
        ... # TODO complete get procedure
    def set(self, **kwarg):
        ... # TODO complete set procedure
    def read(self):
        if self._mode not in ["r"]:
            raise RuntimeError(f"Not supported operation `read` for mode `{self._mode}` for stream source `{self._source}`")
        status, frame = self._content.read()
        if not status:
            frame = None
        return frame
    def write(self, frame):
        if self._mode not in ["w"]:
            raise RuntimeError(f"Not supported operation `write` for mode `{self._mode}` for stream source `{self._source}`")
        self._content.write(frame)
        return frame

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

class VideoStream:
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