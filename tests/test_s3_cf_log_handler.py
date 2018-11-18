from lambdas.s3_handler.s3_cf_log_handler import *

def _cf_log() -> [str]:
    lines = []
    with open('logs/cf-logs.txt', 'r') as f:
        for line in f:
            lines.append(line)
    return lines

def _log_line() -> str:
    return '2018-11-10\t00:16:26\tDEN50-C1\t887\t65.154.226.109\tGET\td313bttlbsfoy.cloudfront.net\t/\t403\t-\tMozilla/4.0%2520(compatible;%2520MSIE%25208.0;%2520Windows%2520NT%25206.1;%2520WOW64;%2520Trident/4.0;%2520SLCC2;%2520.NET%2520CLR%25202.0.50727;%2520.NET%2520CLR%25203.5.30729;%2520.NET%2520CLR%25203.0.30729;%2520Media%2520Center%2520PC%25206.0;%2520.NET4.0C;%2520.NET4.0E;%2520InfoPath.2)\t-\t-\tError\tOuhTpC1iLajIPb2jeR9_rUEFEyboP9LI2YECBzkUrbefHicnvFIM5A==\twww.example.com\thttp\t479\t0.001\t-\t-\t-\tError\tHTTP/1.1\t-\t-\n'

def test_filter_lines():
    assert filter_lines(_cf_log()) == ['2018-11-10\t00:16:26\tDEN50-C1\t887\t65.154.226.109\tGET\td313bttlbsfoy.cloudfront.net\t/\t403\t-\tMozilla/4.0%2520(compatible;%2520MSIE%25208.0;%2520Windows%2520NT%25206.1;%2520WOW64;%2520Trident/4.0;%2520SLCC2;%2520.NET%2520CLR%25202.0.50727;%2520.NET%2520CLR%25203.5.30729;%2520.NET%2520CLR%25203.0.30729;%2520Media%2520Center%2520PC%25206.0;%2520.NET4.0C;%2520.NET4.0E;%2520InfoPath.2)\t-\t-\tError\tOuhTpC1iLajIPb2jeR9_rUEFEyboP9LI2YECBzkUrbefHicnvFIM5A==\twww.example.com\thttp\t479\t0.001\t-\t-\t-\tError\tHTTP/1.1\t-\t-\n']

def test_process_line():
    assert process_line(_log_line()) == {'date': '2018-11-10', 'time': '00:16:26', 'x-edge-location': 'DEN50-C1', 'sc-bytes': '887', 'c-ip': '65.154.226.109', 'cs-method': 'GET', 'cs-host': 'd313bttlbsfoy.cloudfront.net', 'cs-uri-stem': '/', 'sc-status': '403', 'cs-referer': '-', 'cs-user-agent': 'Mozilla/4.0%2520(compatible;%2520MSIE%25208.0;%2520Windows%2520NT%25206.1;%2520WOW64;%2520Trident/4.0;%2520SLCC2;%2520.NET%2520CLR%25202.0.50727;%2520.NET%2520CLR%25203.5.30729;%2520.NET%2520CLR%25203.0.30729;%2520Media%2520Center%2520PC%25206.0;%2520.NET4.0C;%2520.NET4.0E;%2520InfoPath.2)', 'cs-uri-query': '-', 'cs-cookie': '-', 'x-edge-result-type': 'Error', 'x-edge-request-id': 'OuhTpC1iLajIPb2jeR9_rUEFEyboP9LI2YECBzkUrbefHicnvFIM5A==', 'x-host-header': 'www.example.com', 'cs-protocol': 'http', 'cs-bytes': '479', 'time-taken': '0.001', 'x-forwarded-for': '-', 'ssl-protocol': '-', 'ssl-cipher': '-', 'x-edge-response-result-type': 'Error', 'cs-protocol-version': 'HTTP/1.1', 'fle-status': '-', 'fle-encrypted-fields': '-'}

