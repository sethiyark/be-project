import hal, time
import parallel'

p = parallel.Parallel()
h = hal.component("test")

# create pins and parameters with calls to h.newpin and h.newparam
h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready() # mark the component as 'ready'
#print h.getitem("13")
hal.connect()

try:
	while 1:
	    # act on changed input pins; update values on output pins
	    time.sleep(1)
	    h['out'] = h['in']
except KeyboardInterrupt: pass

