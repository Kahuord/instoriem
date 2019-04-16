import os

from instagram.application import create_application


configuration = os.environ['APPLICATION_CONFIG_FILE']

application = create_application(configuration=configuration)
