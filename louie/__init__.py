from wit import Wit
import wolframalpha  as wolf

# Wit.ai parameters
WIT_TOKEN = 'FCLEILUP6T2PTIH6TSWWJYFJYKG3KL2L'

# Messenger API parameters
FB_PAGE_TOKEN = 'EAAEvbHrTo9IBAJigS9lKANutM4V3qOzcnzi86PbWufrN5NJaB1c8ZBOn1DEof3lrTPX9w3qZCpWn93G9yRLw5UrtzS4dP6HLmuAenhAjKJUXDMVP67Iq2FHr2Fc3yCyZBgF87ZAj0y1PPshW0elBivNr0vXw6UPxY5BsyZA1u3gZDZD'

# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = 'hello'

# Wolfram
WOLFRAM_TOKEN = '64J9LH-5Q8357GKRK'

# Google PLaces Token
GOOGS_PLACES_TOKEN = 'AIzaSyABRaPH0tzxRT_sVBkkGr5zWkbN3y7jN9Q'

witclient = Wit(access_token=WIT_TOKEN)
wolfclient = wolf.Client(WOLFRAM_TOKEN)

from louie.query import *
