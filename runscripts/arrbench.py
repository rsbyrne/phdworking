import sys
sys.path.append('/home/jovyan/workspace')

import os
outputDir = '/home/jovyan/workspace/data'

projName = 'arrbench'
projBranch = 'test'
outputPath = os.path.join(outputDir, projName, projBranch)

import planetengine
import modelscripts

chunks = int(sys.argv[1])
chunkno = int(sys.argv[2])

suitelist = planetengine.utilities.suite_list({
    'f': [x / 10. for x in range(1, 11)],
    'Ra': [10. ** (x / 2.) for x in range(6, 15)],
    'eta0': [10. ** (x / 2.) for x in range(11)],
    }, shuffle = True, chunks = chunks)

localJobs = suitelist[chunkno]

planetengine.log(
    "Starting chunk no# " + str(chunkno),
    'logs'
    )

for index, job in enumerate(localJobs):

    model = planetengine.frame.make_frame(
#         modelscripts.isovisc_systemscript.build(**job, res = 64),
        modelscripts.arrhenius.build(**job, res = 16),
        {'temperatureField': planetengine.initials.sinusoidal.IC(freq = 1.)},
        outputPath
        )

    conditions = {
#         'stopCondition': lambda: model.time > 0.3,
        'stopCondition': lambda: model.step > 10,
        'collectConditions': lambda: model.step % 10 == 0,
        'checkpointCondition': lambda: any([
            model.status == 'pre-traverse',
            model.step % 1000 == 0,
            model.status == 'post-traverse',
            ]),
        }

    planetengine.log(
        "Starting chunk no# " + str(chunkno) + " job no# " + str(index) + " params: " + str(sorted(job.items())),
        'logs'
        )

    model.traverse(**conditions)

    planetengine.log(
        "Finishing chunk no# " + str(chunkno) + " job no# " + str(index) + " params: " + str(sorted(job.items())),
        'logs'
        )

planetengine.log(
    "Finishing chunk no# " + str(chunkno),
    'logs'
    )