from planetengine.frame import make_frame
from planetengine import initials
from planetengine import shapes

from modelscripts import isovisc_systemscript
from modelscripts import isovisc_observerscript

steps = 10000
res = 4

outputPath = '' #'/workspace/user_data/data/tests'

isovisc1 = make_frame(
    isovisc_systemscript.build(res = 4 * res, Ra = 1e5, aspect = 2),
    isovisc_observerscript.build(),
    initials = {'temperatureField': {'IC': initials.sinusoidal.IC(freq = 2.)}},
    outputPath = outputPath
    )

isovisc1.report()

checkpointCondition = lambda: any([
    isovisc1.status == 'pre-traverse',
    isovisc1.status == 'post-traverse',
    ])
collectCondition = lambda: False
stopCondition = lambda: isovisc1.step >= steps

isovisc1.traverse(stopCondition, collectCondition, checkpointCondition)

isovisc1.report()

isovisc2 = make_frame(
    isovisc_systemscript.build(res = 8 * res, Ra = 1e6, aspect = 2),
    isovisc_observerscript.build(),
    initials = {'temperatureField': 
        {'IC': initials.load.IC(isovisc1, 'temperatureField'), 'varBounds': [[0., 1.]]}
        },
    outputPath = outputPath
    )

isovisc2.report()

checkpointCondition = lambda: any([
    isovisc2.status == 'pre-traverse',
    isovisc2.status == 'post-traverse',
    ])
collectCondition = lambda: False
stopCondition = lambda: isovisc2.step >= steps

isovisc2.traverse(stopCondition, collectCondition, checkpointCondition)

isovisc2.report()

isovisc3 = make_frame(
    isovisc_systemscript.build(res = 16 * res, Ra = 1e7, aspect = 2),
    isovisc_observerscript.build(),
    initials = {'temperatureField': 
        {'IC': initials.load.IC(isovisc2, 'temperatureField'), 'varBounds': [[0., 1., '.', '.']]}
        },
    outputPath = outputPath
    )

isovisc3.report()

checkpointCondition = lambda: any([
    isovisc3.status == 'pre-traverse',
    isovisc3.status == 'post-traverse',
    ])
collectCondition = lambda: False
stopCondition = lambda: isovisc3.step >= steps

isovisc3.traverse(stopCondition, collectCondition, checkpointCondition)

isovisc3.report()

from modelscripts import MS98_systemscript
from modelscripts import MS98_observerscript

MS98a = make_frame(
    MS98_systemscript.build(res = 16 * res, Ra = 1e7, tau0 = 1e6, aspect = 2),
    MS98_observerscript.build(),
    initials = {'temperatureField': 
        {'IC': initials.load.IC(isovisc3, 'temperatureField'), 'varBounds': [[0., 1., '.', '.']]}
        },
    outputPath = outputPath
    )

MS98a.report()

checkpointCondition = lambda: any([
    MS98a.status == 'pre-traverse',
    MS98a.step % 100 == 0,
    MS98a.status == 'post-traverse',
    ])
collectCondition = lambda: MS98a.step % 10 == 0
stopCondition = lambda: MS98a.step >= 6 * steps

MS98a.traverse(stopCondition, collectCondition, checkpointCondition)

MS98a.report()

MS98b = make_frame(
    MS98_systemscript.build(res = 32 * res, Ra = 1e7, tau0 = 1e6, aspect = 2.),
    MS98_observerscript.build(),
    initials = {'temperatureField': 
        {'IC': initials.load.IC(MS98a, 'temperatureField'), 'varBounds': [[0., 1., '.', '.']]}
        },
    outputPath = outputPath
    )

MS98b.report()

checkpointCondition = lambda: any([
    MS98b.status == 'pre-traverse',
    MS98b.step % 100 == 0,
    MS98b.status == 'post-traverse',
    ])
collectCondition = lambda: MS98b.step % 10 == 0
stopCondition = lambda: MS98b.step >= 6 * steps

MS98b.traverse(stopCondition, collectCondition, checkpointCondition)

MS98b.report()

from modelscripts import MS98X_systemscript
from modelscripts import MS98X_observerscript

MS98X = make_frame(
    MS98X_systemscript.build(res = 32 * res, Ra = 1e7, tau = 1e6, heating = 0., aspect = 2),
    MS98X_observerscript.build(),
    initials = {
        'temperatureField': {'IC': initials.load.IC(MS98a, 'temperatureField'), 'varBounds': [[0., 1., '.', '.']]},
        'materialVar': {'IC': initials.extents.IC((1, shapes.trapezoid(longwidth = 0.3, lengthRatio = 0.9)))}
        },
    outputPath = outputPath
    )

MS98X.report()

checkpointCondition = lambda: any([
    MS98X.status == 'pre-traverse',
    MS98X.step % 1000 == 0,
    MS98X.status == 'post-traverse',
    ])
collectCondition = lambda: MS98X.step % 10 == 0
stopCondition = lambda: MS98X.step >= 30 * steps

MS98X.traverse(stopCondition, collectCondition, checkpointCondition)

MS98X.report()
