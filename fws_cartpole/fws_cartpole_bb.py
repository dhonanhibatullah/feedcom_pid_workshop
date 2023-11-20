import gymnasium as gym
import numpy as np



# Informations
SIMULATION_TIME = 10.0  # in seconds
SIMULATION_STEP = 0.02  # in seconds
GRAVITY_ACC     = 9.8   # in m/s^2
CART_MASS       = 1.0   # in kg
POLE_MASS       = 0.1   # in kg
POLE_LENGTH     = 0.5   # in m
KP_CONST        = 23
KI_CONST        = 0.2
KD_CONST        = 3
ANGLE_REF       = 0.0



# Control law
last_err    = 0.
sum_err     = 0.
def controlInput(state:np.ndarray) -> tuple:
    global last_err
    global sum_err

    # Calculate control law
    err         = ANGLE_REF - float(state[2])
    sum_err     += err
    diff_err    = err - last_err
    last_err    = err
    u           = KP_CONST*err + KI_CONST*sum_err + KD_CONST*diff_err

    # Determine direction
    if u < 0:
        direction = 1
    else:
        direction = 0

    # Retrun value
    return u, direction



# Create environment
env         = gym.make('CartPole-v1', render_mode='human')
(state, _)  = env.reset()



# Loop
success         = True
time_elapsed    = 0.0
for i in range(int(SIMULATION_TIME/SIMULATION_STEP)):

    # Render animation
    env.render()

    # State from new step
    u, direction                = controlInput(state)
    env.force_mag               = u
    (state, _, terminate, _, _) = env.step(direction)

    # Termination rule
    if terminate:
        success = False
        break
    else:
        time_elapsed += SIMULATION_STEP

if success:
    print('SUCCESS!')
else:
    print(f'FAILED! You survived for {time_elapsed}s')



# Close environment
env.close()