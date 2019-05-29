import sys
sys.path.append('/workspace/user_data')

outputPath = '/workspace/user_data/data/tests/dev'

import planetengine

MS98 = planetengine.frame.load_frame(outputPath, 'pemod_anisopodal-craftiest', loadStep = 'max')