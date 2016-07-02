#include <Python.h>
#include "RCSwitch.h"


/*============================ Macro ============================*/

/*============================ Global variable ============================*/

RCSwitch mySwitch;

struct moduleStaticMemory { /* Describe static memory of module instantiation. One memory area exist per PyInit_() call */
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

/*============================ Function implementation ============================*/

/*------------------------------- init Python -------------------------------*/
static PyMethodDef rcSwitchForPythonMethods[] = {
 {   "setup",    (PyCFunction)setup,  METH_NOARGS, NULL},
 {    "send",     (PyCFunction)send, METH_VARARGS, NULL},
 {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

extern "C" int rcSwitchForPythonTraverse(PyObject * self, visitproc visit, void *arg){ /* Memory management, cyclic garbage collection support */
    Py_VISIT(GETSTATE(self)->error);
    return 0;
}

extern "C" int rcSwitchForPythonClear(PyObject * self){ /* Memory management, garbage collection */
    Py_CLEAR(GETSTATE(self)->error);
    return 0;
}

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "rcSwitchForPython",
        NULL,
        sizeof(struct moduleStaticMemory),
        rcSwitchForPythonMethods,
        NULL,
        rcSwitchForPythonTraverse,
        rcSwitchForPythonClear,
        NULL
};

PyMODINIT_FUNC PyInit_rcSwitchForPython(void){
  PyObject *module = PyModule_Create(&moduledef);

  if (module == NULL)
      return NULL;
  struct moduleStaticMemory *st = GETSTATE(module);

  st->error = PyErr_NewException("rcSwitchForPython.error", NULL, NULL);
  if (st->error == NULL) {
      Py_DECREF(module);
      return NULL;
  }
  return module;
}

#else 

PyMODINIT_FUNC initrcSwitchForPython(void){ 
  PyObject *module = Py_InitModule("rcSwitchForPython", rcSwitchForPythonMethods);

  if (module == NULL)
      return;
  struct moduleStaticMemory *st = GETSTATE(module);

  st->error = PyErr_NewException("rcSwitchForPython.error", NULL, NULL);
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
  if (wiringPiSetup () != -1){
    mySwitch = RCSwitch();
    mySwitch.enableTransmit(0);
  }

  /*-- End program --*/
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject * send(PyObject * self, PyObject * args)
{
  int state, addr, channel;

  /*-- Parse arguments --*/
  if(!PyArg_ParseTuple(args, "iii", &state, &addr, &channel)){
    /* raise exception */
    struct moduleStaticMemory *st = GETSTATE(self);
    PyErr_SetString(st->error, "Bad arguments, expected : state - addr - channel");
    return NULL;
  }

  /*-- Program --*/
  if(state){
    printf("python to rcswitch send %d, %d, %d\n", state, addr, channel);
    mySwitch.switchOn(addr, channel);
  }else{
    printf("python to rcswitch send %d, %d, %d\n", state, addr, channel);
    mySwitch.switchOff(addr, channel);
  }

  /*-- End program --*/
  Py_INCREF(Py_None);
  return Py_None;
}
