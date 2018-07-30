#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<unistd.h>
#include "python2.7/Python.h"

float theVelocity=80.0;
int thePitch=5;
int pulse_per_rotation=2000;
float endDistance=500.0;
float curDistance=0.0;
float acceleration=500.0;
float per_pulse_distance=0.0025;
int total_pulses=0;

float dist=0.0;
double initialVelocity=0.0;
double finalVelocity=0.0;
int pulses_per_mm=400;
int pulses=0;
double dela=0.0;
double temp=0.0;
int count=0;
float delay=0.0;	
/*	clock_t t;
	t=clock();
	
	t=clock()-t;
	double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	printf("count:%d",count);
	printf("time:%lf",time_taken);
*/

static PyObject* py_myOtherFunction1(PyObject* self, PyObject* args)
{
		PyArg_ParseTuple(args, "d", &initialVelocity);
	  	//printf("Initial vel:%f",initialVelocity);
		temp=(initialVelocity*initialVelocity)-(2*acceleration*per_pulse_distance);
		finalVelocity=sqrt(temp);
		//printf("final vel:%f",finalVelocity);
		dela=(initialVelocity - finalVelocity)/acceleration;
		//sleep(dela);
		// printf("delay value:%f %f\n",dela, finalVelocity);

	 	return Py_BuildValue("dd", finalVelocity,dela);
}

static PyObject* py_myOtherFunction(PyObject* self, PyObject* args)
{
	  	PyArg_ParseTuple(args, "d", &initialVelocity);
	  	//printf("Initial vel:%f",initialVelocity);
		temp=(initialVelocity*initialVelocity)+(2*acceleration*per_pulse_distance);
		finalVelocity=sqrt(temp);
		//printf("final vel:%f",finalVelocity);
		dela=(finalVelocity-initialVelocity)/acceleration;
		//sleep(dela);
		// printf("delay value:%f %f\n",dela, finalVelocity);

	 	return Py_BuildValue("dd", finalVelocity,dela);
}

static PyMethodDef CNC_Machine_methods[] = {
  {"myOtherFunction1", py_myOtherFunction1, METH_VARARGS},
  {"myOtherFunction", py_myOtherFunction, METH_VARARGS},
  {NULL, NULL}
};

void initCNC_Machine()
{
  (void) Py_InitModule("CNC_Machine", CNC_Machine_methods);
}

/*
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}
*/
