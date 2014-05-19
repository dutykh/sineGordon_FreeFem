sine-Gordon solver for FreeFem++
======

![sine-Gordon kink](/pic/Sol0_2D.jpg)

This script allows to solve numerically the sine-Gordon equation in a Y-junction geometry using the Finite Element Method (FEM). The scheme is of 2nd order in space and time. The implixit-explicit time stepping method is of the Crank-Nicolson type and it possesses excellent energy conservation properties.

Some scientific results on the sine-Gordon equation in a tree-like geometry were obtained using this method. They are briefly described in the following preprint:

* J.-G. Caputo & **D. Dutykh**. [Nonlinear waves in networks: a simple approach using the sine-Gordon equation](http://hal.archives-ouvertes.fr/hal-00951705/). Submitted, 2014

Any comments are welcome!

## Authors
  
[Denys Dutykh](http://www.denys-dutykh.com/)

[Jean-Guy Caputo](http://lmi.insa-rouen.fr/membres/20-caputo.html)

======

### FreeFem++

The code FreeFem++ is a Partial Differential Equation (PDE) solver based on the Finite Element Method (FEM) which can be freely downloaded for various platforms here:  

* [http://www.freefem.org/ff++/](http://www.freefem.org/ff++/)
