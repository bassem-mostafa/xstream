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

from xstream import StringIO

## #############################################################################
## #### Private Type(s) ########################################################
## #############################################################################

class _frames_generator:
    '''
    frames generator
    '''
    def __init__(self, stream, start, stop, step):
        '''
        Initializes frames generator
        args:
            stream: represents the stream from which to generate frames
            start: index of first frame to be generated
            stop: index of just after last frame to be generated
            step: index increment between two consecuitive generated frames
        returns:
            a frames generator
        '''
        self._stream = stream
        self._start = start if start is not None else 0
        self._stop = stop if stop is not None else len(stream)
        self._step = step if step is not None else 1
        self._length = (self._stop - self._start) / self._step
    def __len__(self):
        '''
        Gets the frames generator total number of frames
        returns:
            total number of frames
        '''
        return int(self._length)
    def __iter__(self):
        '''
        Gets an iterator for the frames generator
        returns:
            a frames generator iterator
        '''
        return self
    def __next__(self):
        '''
        Gets next frame of the iterator for the frames generator
        returns:
            next frame of the iterator
        '''
        if self._start >= self._stop:
            raise StopIteration()
        self._stream.seek(self._start)
        self._start += self._step
        return self._stream.read()

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

class Stream:
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
    def __len__(self):
        '''
        Gets the stream total number of frames
        returns:
            total number of frames
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `__len__` for stream source `{self._source}`")
        return None
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
    def __getitem__(self, key):
        '''
        Gets frames at indices equals to provided key
        args:
            key: represents the indices of corresponding frames to be fetched
        returns:
            frames of specified indices
        '''
        if not isinstance(key, (int, slice)):
            raise RuntimeError(f"Not supported operation `__getitem__` for key `{key}` of type `{type(key)}` for stream source `{self._source}`")
        result = None
        if isinstance(key, int):
            self.seek(key)
            result = self.read()
        elif isinstance(key, slice):
            result = _frames_generator(self, key.start, key.stop, key.step)
        return result
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
    def seek(self, index):
        '''
        Seeks to index into the stream
        returns:
            True on a successful seeking, False otherwise
        '''
        raise RuntimeError(f"Not supported {self.__class__.__name__} operation `seek` for stream source `{self._source}`")
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