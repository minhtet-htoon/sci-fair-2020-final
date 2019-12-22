# -*- coding: utf-8 -*-
"""
===========================
The double pendulum problem
===========================

This animation illustrates the double pendulum problem.
"""
""" Save before running"""
# This was used by Minhtet Htoon for ISEF 2020 and based on the code at 
# https://matplotlib.org/examples/animation/double_pendulum_animated.html
# and https://scipython.com/blog/the-double-pendulum/
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import matplotlib as mpl


""" Save before running"""

G =  9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg

"""DO NOT TOUCH"""
def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2] - state[0]
    den1 = (M1 + M2)*L1 - M2*L1*cos(del_)*cos(del_)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_) +
               M2*G*sin(state[2])*cos(del_) +
               M2*L2*state[3]*state[3]*sin(del_) -
               (M1 + M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(state[0])*cos(del_) -
               (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
               (M1 + M2)*G*sin(state[2]))/den2

    return dydx

# create a time array from 0..100 sampled at 0.05 second steps (make this number as low as possible without slowing down your PC)
# duration specifies simulation length (sec) 
dt = 0.05
duration=180
t = np.arange(0.0, duration, dt)
# th1 and th2 are the initial angles (degrees)
# w1 and w2 are the initial angular velocities (degrees per second)
# th1 >= 79.15 for divergence
th1 = 50
w1 = 0.0
th2 = 0
w2 = 0.0
sensitivity=1e9
trail_secs = 10
# This corresponds to max_trail time points.
max_trail = int(trail_secs / dt)

# initial stateS
state = np.radians([th1, w1, th2, w2])
state2 = np.radians([th1+ 1/sensitivity, w1, th2+ 1/sensitivity, w2])
state3 = np.radians([th1-1/sensitivity, w1, th2- 1/sensitivity, w2])
# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)
z = integrate.odeint(derivs, state2, t)
v = integrate.odeint(derivs, state3, t)

x1 = L1*sin(y[:, 0])
y1 = -L1*cos(y[:, 0])

x2 = L2*sin(y[:, 2]) + x1
y2 = -L2*cos(y[:, 2]) + y1

x21 = L1*sin(z[:, 0]) 
y21 = -L1*cos(z[:, 0])

x22 = L2*sin(z[:, 2]) + x21
y22 = -L2*cos(z[:, 2]) + y21

x31 = L1*sin(v[:, 0]) 
y31 = -L1*cos(v[:, 0]) 

x32 = L2*sin(v[:, 2]) + x31
y32 = -L2*cos(v[:, 2]) + y31

#No more math this is just graphics
size=L1+L2

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot( xlim=(-size, size), ylim=(-size, size))
ax.grid()
#Theming (comment out through line 119 for light theme)
ax.set_facecolor('#000000') #plot color
fig.patch.set_facecolor('#000000') #border color

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

mpl.rcParams['text.color'] = '#ffffff'
mpl.rcParams['axes.labelcolor'] = '#ffffff'
mpl.rcParams['xtick.color'] = '#ffffff'
mpl.rcParams['ytick.color'] = '#ffffff'

line, = ax.plot([], [], 'o-', c='#ff8300', lw=2)
line2, = ax.plot([], [], 'o-', c='#15f4ee', lw=2)
line3, = ax.plot([], [], 'o-', c='#39ff14', lw=2)

trail1, = ax.plot([], [], c='#ff8300', solid_capstyle='butt', lw=1)
trail2, = ax.plot([], [], c='#15f4ee', solid_capstyle='butt', lw=1)
trail3, = ax.plot([], [], c='#39ff14', solid_capstyle='butt', lw=1)

time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    
    line.set_data(thisx, thisy)

    thisx1 = [0, x21[i], x22[i]]
    thisy1 = [0, y21[i], y22[i]]
   
    line2.set_data(thisx1, thisy1)
    
    thisx2 = [0, x31[i], x32[i]]
    thisy2 = [0, y31[i], y32[i]]
   
    line3.set_data(thisx2, thisy2)
    
    imin= i- max_trail
    if imin<0:
        imin=0
    trail1.set_data(x2[imin:i], y2[imin:i]) 
    trail2.set_data(x22[imin:i], y22[imin:i]) 
    trail3.set_data(x32[imin:i], y32[imin:i]) 
    
    time_text.set_text(time_template % (i*dt))
    return line, line2, line3, trail1, trail2, trail3, time_text, 

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=30, blit=True, init_func=init)


plt.show()


