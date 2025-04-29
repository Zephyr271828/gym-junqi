API
===
In this page we provide documentation for our Junqi environment and other APIs the
users might be interested in using.

JunQiEnv
----------
JunQiEnv provides core environment attributes and methods that all OpenAI Gym
environments provide.

.. autoclass:: gym_junqi.envs.junqi_env.JunQiEnv
  :inherited-members:
  :members:

From Piece Move to JunQiEnv Action Space
------------------------------------------
Intuitively we can interpret a piece's move having the three information:

- Piece: unique identifiable piece on the board
- Start Position: the selected piece's current Position
- End Position: the desired position the selected piece wants to move to
  
Given the piece ID, its current location and its target position, this
function encodes this information into JunQiEnv's action space and the
resulting output is an action ID which is a single integer.

.. autofunction:: gym_junqi.utils.move_to_action_space

From JunQiEnv Action Space to Piece Move
------------------------------------------
If we can encode piece move information into the action space, we should
also be able to decode the encoded action ID back into original information.

.. autofunction:: gym_junqi.utils.action_space_to_move
