## National Weather Service API


Find all current alerts in Colorado.

```nws
    >>> from pyapix.apis import nws
    >>> endpoint, verb = '/alerts/active', 'get'
    >>> params = dict(area='CO')
    >>> response = nws.call(endpoint, verb, params)
    >>> response.status_code
    200
    >>> response.is_success
    True
    >>> list(response.json())
    ['@context', 'type', 'features', 'title', 'updated']
    >>> len(response.json()['features'])
    8
    >>> for alert in response.json()['features']:
    ...     print(alert['properties']['headline'])
    ...     
    High Wind Warning issued February 7 at 8:10AM MST until February 7 at 5:00PM MST by NWS Pueblo CO
    High Wind Warning issued February 7 at 8:10AM MST until February 7 at 5:00PM MST by NWS Pueblo CO
    Red Flag Warning issued February 7 at 3:42AM MST until February 7 at 6:00PM MST by NWS Pueblo CO
    Winter Weather Advisory issued February 7 at 2:56AM MST until February 8 at 7:00AM MST by NWS Grand Junction CO
    Wind Advisory issued February 7 at 2:52AM MST until February 7 at 6:00PM MST by NWS Grand Junction CO
    Winter Weather Advisory issued February 7 at 2:45AM MST until February 8 at 7:00AM MST by NWS Denver CO
    Winter Weather Advisory issued February 7 at 2:45AM MST until February 8 at 7:00AM MST by NWS Denver CO
    Winter Weather Advisory issued February 7 at 2:45AM MST until February 8 at 7:00AM MST by NWS Denver CO
```

Florida has no current alerts.

```nws
    >>> params = dict(area='FL')
    >>> response = nws.call(endpoint, verb, params)
    >>> for alert in response.json()['features']:
    ...     print(alert['properties']['headline'])
    ...     
    >>> 
```


Virginia current alerts.

```nws
    >>> params = dict(area='VA')
    >>> response = nws.call(endpoint, verb, params)
    >>> for alert in response.json()['features']:
    ...     print(alert['properties']['headline'])
    ...     
    Flood Watch issued February 7 at 1:47PM EST until February 9 at 4:00AM EST by NWS Charleston WV
    Winter Weather Advisory issued February 7 at 1:46PM EST until February 8 at 6:00PM EST by NWS Wakefield VA
    Winter Weather Advisory issued February 7 at 12:54PM EST until February 8 at 6:00PM EST by NWS Baltimore MD/Washington DC
    Winter Weather Advisory issued February 7 at 12:54PM EST until February 8 at 7:00PM EST by NWS Baltimore MD/Washington DC
    Winter Weather Advisory issued February 7 at 12:54PM EST until February 9 at 12:00AM EST by NWS Baltimore MD/Washington DC
    Winter Weather Advisory issued February 7 at 12:54PM EST until February 9 at 12:00AM EST by NWS Baltimore MD/Washington DC
    Flood Warning issued February 7 at 6:50AM EST until February 7 at 3:15PM EST by NWS Morristown TN
```
