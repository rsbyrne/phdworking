import sys
sys.path.append('..')

import planetengine
import modelscripts

aspect = 1

isovisc1 = planetengine.frame.make_frame(
    modelscripts.isovisc_systemscript.build(
        res = 16,
        Ra = 1e5,
        aspect = aspect
        ),
    modelscripts.isovisc_observerscript.build(),
    initial = {
        'temperatureField': planetengine.initials.sinusoidal.IC(freq = aspect),
        }
    )

isovisc1.go(10000)

isovisc2 = planetengine.frame.make_frame(
    modelscripts.isovisc_systemscript.build(
        res = 32,
        Ra = 1e6,
        aspect = aspect
        ),
    modelscripts.isovisc_observerscript.build(),
    initial = {
        'temperatureField': planetengine.initials.load.IC(isovisc1, 'temperatureField'),
        }
    )

isovisc2.go(10000)

isovisc3 = planetengine.frame.make_frame(
    modelscripts.isovisc_systemscript.build(
        res = 64,
        Ra = 1e7,
        aspect = aspect
        ),
    modelscripts.isovisc_observerscript.build(),
    initial = {
        'temperatureField': planetengine.initials.load.IC(isovisc2, 'temperatureField'),
        }
    )

isovisc3.go(10000)

MS98 = planetengine.frame.make_frame(
    modelscripts.MS98_systemscript.build(
        res = 64,
        Ra = 1e7,
        aspect = aspect,
        tau = 1e6
        ),
    modelscripts.MS98_observerscript.build(),
    initial = {
        'temperatureField': planetengine.initials.load.IC(isovisc3, 'temperatureField'),
        }
    )

MS98.go(10000)

kitchensink = planetengine.frame.make_frame(
    modelscripts.kitchensink_systemscript.build(
        res = 128,
        buoyancy_bR = 1e7,
        aspect = aspect,
        tau0 = 1e6,
        heating = 0.
        ),
    modelscripts.kitchensink_observerscript.build(),
    initial = {
        'temperatureField': planetengine.initials.load.IC(MS98, 'temperatureField'),
        'materialVar': planetengine.initials.extents.IC(
            (1, planetengine.shapes.trapezoid(
                thickness = 0.025,
                longwidth = 1.,
                lengthRatio = 1.
                ))
            )
        }
    )

stopCondition = lambda: False #kitchensink.step >= 10
collectCondition = lambda: kitchensink.step % 10 == 0
checkpointCondition = lambda: any([
    kitchensink.status == 'pre-traverse',
    kitchensink.step % 1000 == 0,
    kitchensink.status == 'post-traverse',
    ])

kitchensink.traverse(stopCondition, collectCondition, checkpointCondition)