from __future__ import print_function, absolute_import, division
from numba import sigutils, types
from .compiler import (compile_kernel, AutoJitOneAPIKernel)


def jit(signature=None, debug=False):
    """JIT compile a python function conforming using the
    Numba-OneAPI backend
    """
    if signature is None:
        return autojit(debug=False)
    elif not sigutils.is_signature(signature):
        func = signature
        return autojit(debug=False)(func)
    else:
        return _kernel_jit(signature, debug)


def autojit(debug=False):
    return _kernel_autojit


def _kernel_jit(signature, debug):
    argtypes, restype = sigutils.normalize_signature(signature)
    if restype is not None and restype != types.void:
        msg = ("OneAPI/OpenCL kernel must have void return type "
               "but got {restype}")
        raise TypeError(msg.format(restype=restype))

    def _wrapped(pyfunc):
        return compile_kernel(pyfunc, argtypes, debug)

    return _wrapped


def _kernel_autojit(pyfunc):
    return AutoJitOneAPIKernel(pyfunc)
