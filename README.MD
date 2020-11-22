# DNS-client

## What already does

- Specifying your DNS server instead of the standard one (standard 8.8.8.8)
- Selection of the type of information to be obtained. Records such as A, NS and AAAA are already supported
- The port through which the client will access the server
- Support for both recursive and iterative regimes
- Setting timeouts - time between attempts to request the server
- TCP or UDP

## Dependencies

- Python >= 3

## Package structure

- Client: `dns-client.py`
- Internal: `architecture/`
- tests: `tests/`

Modules in `architecture/` have tests and can be found in `/tests`. The line coverage is 91%

You can use `runtest.sh` (you need `bash`, `coverage3`) to run the tests.

```bash

Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
architecture/__init__.py          12      0   100%
architecture/flags.py             55     12    78%   85, 89-99
architecture/record_types.py      40      3    92%   45, 50, 53
architecture/request.py           67      2    97%   32, 49
architecture/response.py         112     24    79%   29-30, 32-33, 37-46, 80, 87-93, 116, 120
architecture/utils.py             24      0   100%
tests/test_flags.py               28      0   100%
tests/test_record_types.py        28      0   100%
tests/test_request.py             50      0   100%
tests/test_response.py            45      0   100%
tests/test_utils.py               17      0   100%
------------------------------------------------------------
TOTAL                            478     41    91%

```

## How to run

Help: `./dns-client.py --help`

Example: `./dns-client.py yandex.ru`

## Details

All the necessary modules can be found in `architecture/` . The basic functionality is provided by `client.py` - this is where the DNS query is configured. The files `flags.py`, `record_types.py`, `request.py`, `response.py` and `utils.py` describe the structure of the DNS query and are responsible for processing, encoding and decoding it.

All details of the DNS protocol can be read in [RFC1035](http://www.ietf.org/rfc/rfc1035) .
