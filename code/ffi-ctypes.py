import ctypes

_libcrypt = ctypes.cdll.LoadLibrary('libcrypt.so')

crypt = _libcrypt.crypt
crypt.restype = ctypes.c_char_p
crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

print crypt('secret', '$6$randomsalt')
# $6$randomsalt$IJynOtjaPVh8n1ZrY6d.YwXK98nJZCZ4v3fkC7...
