import os
import sys
sys.path.append(os.path.abspath('..'))

from wit import Wit
from louie import WIT_TOKEN

client = Wit(access_token=WIT_TOKEN)
client.interactive()
