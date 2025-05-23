Installation
============

You can install Gym Junqi using pip or directly from source code.


Using PIP
---------
To install using pip, run:

.. code-block:: sh

   pip install gym-junqi

Installing from Source
----------------------
To install from the source,

1. First download the latest release from our `repository <https://github.com/tanliyon/gym-junqi>`_.
2. Extract the files using `unzip` or `tar`

.. code-block:: sh

   unzip gym-junqi-x.x.x.zip

.. code-block:: sh

   tar -xf gym-junqi-x.x.x.zip

3. Change directory to project root:

.. code-block:: sh

   cd gym-junqi

4. Build and install:

.. code-block:: sh

   python setup.py build
   python setup.py install

Installing for Development
--------------------------
To install for development,

1. clone the repository:

.. code-block:: sh

   git clone https://github.com/Zephyr271828/gym-junqi.git

2. Change directory to project root:

.. code-block:: sh

   cd gym-junqi

3. Install Python Dependencies:

.. code-block:: sh

   pip install -r requirement.txt

.. note::

   We recommend creating a separate virtual environment just for this project.

   To create a virtual environment, run:

   .. code-block:: sh

      python -m venv <virtual environment name>

4. Install the project as Python module:

.. code-block:: sh

   pip install -e .
