from planetengine import utilities
from planetengine import frame
#import isovisc_systemscript as systemscript
from modelscripts import isovisc_systemscript as systemscript
from modelscripts import isovisc_observerscript as observerscript
from modelscripts import sinusinglephase_initialscript as initialscript
import sys
import os

#outputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
outputPath = 'data'

inputarg = int(sys.argv[1])
chunks = 0

suite_list = utilities.suite_list({
    'res': [64,],
    'Ra': [10. ** (i / 10. + 4) for i in range(0, 21)],
    'f': [2. / i for i in range(2, 13)],
    }, shuffle = True, chunks = chunks)

localJobs = suite_list[inputarg]

for job in localJobs:

    model = frame.Frame(
        systemscript.build(**job),
        observerscript.build(),
        initialscript.build(),
        outputPath = outputPath,
        instanceID = 'isotest',
        )

    checkpointCondition = lambda: any([
        model.status == 'pre-traverse',
        model.step % 1000 == 0,
        model.status == 'post-traverse',
        ])
    collectCondition = lambda: model.step % 10 == 0
    stopCondition = lambda: model.modeltime > 0.6

    model.traverse(stopCondition, collectCondition, checkpointCondition)
