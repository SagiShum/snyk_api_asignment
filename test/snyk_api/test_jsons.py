from snyk_api.code_utils import CodeLocation

test_thread_flow = {'locations':
                        [{'location': {'id': 0,
                                       'physicalLocation': {'artifactLocation': {
                                           'uri': 'a',
                                           'uriBaseId': 'b'},
                                           'region': {'startLine': 1,
                                                      'endLine': 1,
                                                      'startColumn': 1,
                                                      'endColumn': 2}}}}
                         ]}

test_thread_flow_locations = {CodeLocation('a', 'b', 0, 0, 0, 1)}

test_thread_flow_merge = {'locations':
                              [{'location': {'id': 0,
                                             'physicalLocation': {'artifactLocation': {
                                                 'uri': 'a',
                                                 'uriBaseId': 'b'},
                                                 'region': {'startLine': 1,
                                                            'endLine': 1,
                                                            'startColumn': 1,
                                                            'endColumn': 2}}}},
                               {'location': {'id': 1,
                                             'physicalLocation': {'artifactLocation': {
                                                 'uri': 'a',
                                                 'uriBaseId': 'b'},
                                                 'region': {'startLine': 1,
                                                            'endLine': 1,
                                                            'startColumn': 1,
                                                            'endColumn': 3}}}}
                               ]}

test_thread_flow_merge_locations = {CodeLocation('a', 'b', 0, 0, 0, 2)}
