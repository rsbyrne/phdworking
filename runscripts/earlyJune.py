import sys
sys.path.append('/workspace/user_data')

test = True

import os
if not test:
    outputDir = '/workspace/user_data/data'
else:
    outputDir = '/workspace/user_data/data/tests/dev'
projName = 'isobenchJune'
projBranch = 'Neptune'
outputPath = os.path.join(outputDir, projName, projBranch)

import planetengine
import modelscripts

chunks = int(sys.argv[1])
chunkno = int(sys.argv[2])

suitelist = planetengine.utilities.suite_list({
    'f': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 'max'],
    'Ra': [1e4, 2e4, 4e4, 16e4, 32e4, 64e4, 128e4, 256e4, 512e4, 1024e4],
    }, shuffle = True, chunks = chunks)

localJobs = suitelist[chunkno]

for index, job in enumerate(localJobs):

    model = planetengine.frame.make_frame(
        modelscripts.isovisc_systemscript.build(**job, res = 16),
        modelscripts.isovisc_observerscript_NOFIGS.build(),
        {'temperatureField': planetengine.initials.sinusoidal.IC(freq = 1.)},
        outputPath
        )

    if not test:
        steps = int(job['Ra'] / 1e4 * 100)
    else:
        steps = 10

    conditions = {
        'stopCondition': lambda: model.step > steps,
        'collectCondition': lambda: model.step % 10 == 0,
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
