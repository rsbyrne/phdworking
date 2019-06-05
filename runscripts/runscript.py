import sys
sys.path.append('..')

import planetengine
import modelscripts

outputPath = '/workspace/user_data/data/tests/dev'

loadmodel = planetengine.frame.load_frame(outputPath, "pemod_bestand-displuviate", 'max')

model = planetengine.frame.make_frame(
    system = modelscripts.MS98_systemscript.build(**loadmodel.inFrames[0].params),
    observer = modelscripts.MS98_observerscript.build(),
    initials = {
        'temperatureField': planetengine.initials.load.IC(loadmodel, 'temperatureField', 'max')
        },
    outputPath = outputPath
    )

checkpointCondition = lambda: any([
    model.status == 'pre-traverse',
    model.step % 1000 == 0,
    model.status == 'post-traverse',
    ])
collectCondition = lambda: model.step % 10 == 0
stopCondition = lambda: model.step >= 10000

model.traverse(stopCondition, collectCondition, checkpointCondition)