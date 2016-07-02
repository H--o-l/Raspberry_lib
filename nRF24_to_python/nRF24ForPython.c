#include <Python.h>
#include "nRF24.h"

/*============================ Macro ============================*/

/*============================ Global variable ============================*/

struct moduleStaticMemory {  /* Describe static memory of module instantiation. One memory area exist per PyInit_() call */
    PyObject *error; /* Py object return by PyErr_NewException */
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct moduleStaticMemory*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct moduleStaticMemory _state;
#endif

/*============================ Local Function interface ============================*/

static PyObject * setup(PyObject * self);
static PyObject * send(PyObject * self, PyObject * args);
static PyObject * received(PyObject * self, PyObject * args);

/*============================ Function implementation ============================*/

/*------------------------------- init Python -------------------------------*/
static PyMethodDef nRF24ForPythonMethods[] = {
 {   "setup",    (PyCFunction)setup,  METH_NOARGS, NULL},
 {    "send",     (PyCFunction)send, METH_VARARGS, NULL},
 {"received", (PyCFunction)received, METH_VARARGS, NULL},
 {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

extern "C" int nRF24ForPythonTraverse(PyObject * self, visitproc visit, void *arg){ /* Memory management, cyclic garbage collection support */
    Py_VISIT(GETSTATE(self)->error);
    return 0;
}

extern "C" int nRF24ForPythonClear(PyObject * self){ /* Memory management, garbage collection */
    Py_CLEAR(GETSTATE(self)->error);
    return 0;
}

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "nRF24ForPython",
        NULL,
        sizeof(struct moduleStaticMemory),
        nRF24ForPythonMethods,
        NULL,
        nRF24ForPythonTraverse,
        nRF24ForPythonClear,
        NULL
};

PyMODINIT_FUNC PyInit_nRF24ForPython(void){
  PyObject *module = PyModule_Create(&moduledef);

  if (module == NULL)
      return NULL;
  struct moduleStaticMemory *st = GETSTATE(module);

  st->error = PyErr_NewException("nRF24ForPython.error", NULL, NULL);
  if (st->error == NULL) {
      Py_DECREF(module);
      return NULL;
  }
  return module;
}

#else 

PyMODINIT_FUNC initnRF24ForPython(void){ 
  PyObject *module = Py_InitModule("nRF24ForPython", nRF24ForPythonMethods);

  if (module == NULL)
      return;
  struct moduleStaticMemory *st = GETSTATE(module);

  st->error = PyErr_NewException("nRF24ForPython.error", NULL, NULL);
  if (st->error == NULL) {
      Py_DECREF(module);
      return;
  }
}

#endif

/*------------------------------- Function -------------------------------*/
static PyObject * setup(PyObject * self)
{
  /*-- Parse arguments --*/  

  /*-- Program --*/
  nRF24_setup();

  /*-- End program --*/
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject * send(PyObject * self, PyObject * args)
{
  char * input;

  /*-- Parse arguments --*/
  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  /*-- Program --*/
  if(!nRF24_send(input)){
    /* raise exception */
    struct moduleStaticMemory *st = GETSTATE(self);
    PyErr_SetString(st->error, nRF24_gaError);
    return NULL;
  }

  /*-- End program --*/
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject * received(PyObject * self, PyObject * args)
{
  long msTimeOut;
  char receivedData[32];
  PyObject * ret;

  /*-- Parse arguments --*/
  if (!PyArg_ParseTuple(args, "l", &msTimeOut)) {
    return NULL;
  }

  /*-- Program --*/
  if(!nRF24_received(receivedData, msTimeOut)){
    /* raise exception */
    struct moduleStaticMemory *st = GETSTATE(self);
    PyErr_SetString(st->error, nRF24_gaError);
    return NULL;
  }

  /*-- End program --*/
  ret = PyUnicode_FromString(receivedData);
  return ret;
}
