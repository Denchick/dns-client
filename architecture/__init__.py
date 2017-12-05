# for query
QUERY_TYPE_NAMES = {1 : 'A', 2: 'NS', 5: 'CNAME', 15 : 'MX', 28: 'AAAA'}
# for answer
QUERY_CLASS_NAMES = {1  : 'IN'}

# for flags
MESSAGE_TYPES = {0 : 'query', 1 : 'response'}
OPCODES = { 0 : 'Standart query', 1 : 'Inverse query', 2 : 'Server status request'}
AUTHORITATIVE = {0 : 'Server is not an authorative for this domain', 1 : 'Server is an authorative for this domain'}
TRUNCATED = {0 : 'Message is not truncated', 1 : 'Message is truncated'}
RECURSION_DESIRED = {0 : 'Do query iteratively', 1 : 'Do query recursively'}
RECURSION_AVAILABLE = {0 : 'Server cannot do recursive queries', 1 : 'Server can do recursive queries'}
ANSWER_AUTHENTICATED = {0 : 'Answer/Authority portion was not authenticated by the server',
                        1 : 'Answer/Authority portion has been authenticated by the server according to the policies of that server'}
NON_AUTHENTICATED_DATA = {0 : 'Unacceptable', 1 : 'acceptable'}

RESPONSE_CODE_NAMES = {0 : 'No error', 1 : 'Format error', 2 : 'Server failure', 3 : 'Name error', 4 : 'Not implemented', 5: 'Refused'}

