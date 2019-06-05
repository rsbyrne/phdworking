import sys
sys.path.append('/workspace/user_data')

import planetengine
import modelscripts

chunks = int(sys.argv[1])
chunkno = int(sys.argv[2])

suitelist = planetengine.utilities.suite_list({
    'f': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    'Ra': [1e4, 2e4, 8e4, 16e4, 32e4, 64e4, 128e4],
    }, shuffle = True, chunks = chunks)

localJobs = suitelist[chunkno]

for index, job in enumerate(localJobs):

    model = planetengine.frame.make_frame(
        modelscripts.isovisc_systemscript.build(**job, res = 16, aspect = 'max'),
        modelscripts.isovisc_observerscript.build(),
        {'temperatureField': planetengine.initials.sinusoidal.IC(freq = 2., phase = 0.5)},
        '/workspace/user_data/data/donutfrequency'
        )

    conditions = {
        'stopCondition': lambda: model.step > 10000,
        'collectCondition': lambda: model.step % 10 == 0,
        'checkpointCondition': lambda: any([
            model.status == 'pre-traverse',
            model.step % 1000 == 0,
            model.status == 'post-traverse',
            ]),
        }

    planetengine.log("Starting chunk no# " + str(chunkno) + " job no# " + str(index) + " params: " + str(sorted(job.items())))

    model.traverse(**conditions)

    planetengine.log("Finishing chunk no# " + str(chunkno) + " job no# " + str(index) + " params: " + str(sorted(job.items())))