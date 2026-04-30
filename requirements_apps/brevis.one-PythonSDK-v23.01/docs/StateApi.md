# swagger_client.StateApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**state_get**](StateApi.md#state_get) | **GET** /state | Get general information about the unit&#x27;s build
[**state_spec_json_get**](StateApi.md#state_spec_json_get) | **GET** /state/spec.json | Get the Restful API specs as JSON
[**state_spec_yml_get**](StateApi.md#state_spec_yml_get) | **GET** /state/spec.yml | Get the Restful API specs as yaml

# **state_get**
> StateResponse state_get()

Get general information about the unit's build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.StateApi(swagger_client.ApiClient(configuration))

try:
    # Get general information about the unit's build
    api_response = api_instance.state_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StateApi->state_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**StateResponse**](StateResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **state_spec_json_get**
> object state_spec_json_get()

Get the Restful API specs as JSON

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StateApi()

try:
    # Get the Restful API specs as JSON
    api_response = api_instance.state_spec_json_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StateApi->state_spec_json_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **state_spec_yml_get**
> str state_spec_yml_get()

Get the Restful API specs as yaml

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StateApi()

try:
    # Get the Restful API specs as yaml
    api_response = api_instance.state_spec_yml_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StateApi->state_spec_yml_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/x-yaml, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

