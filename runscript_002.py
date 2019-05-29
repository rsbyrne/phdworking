import sys
sys.path.append('/workspace/user_data')

outputPath = '/workspace/user_data/data/tests/dev'

import planetengine
import modelscripts

import os

MS98X = planetengine.frame.make_frame(
    modelscripts.MS98X_systemscript.build(res = 64, Ra = 1e7, tau = 1e6, heating = 0., aspect = 2),
    modelscripts.MS98X_observerscript.build(),
    initials = {
        'temperatureField': planetengine.initials.load.IC(
            os.path.join(outputPath, 'pemod_anisopodal-craftiest'),
            'temperatureField',
            'max'
            ),
        'materialVar': planetengine.initials.extents.IC(
            (1, planetengine.shapes.trapezoid(
                longwidth = 0.3,
                lengthRatio = 0.8,
                thickness = 0.05
                ))
            )
        },
    outputPath = outputPath
    )