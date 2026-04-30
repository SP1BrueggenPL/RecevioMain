# swagger_client.UserApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**user_me_get**](UserApi.md#user_me_get) | **GET** /user/me | Get information about the current signed in user

# **user_me_get**
> CurrentUser user_me_get()

Get information about the current signed in user

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
api_instance = swagger_client.UserApi(swagger_client.ApiClient(configuration))

try:
    # Get information about the current signed in user
    api_response = api_instance.user_me_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->user_me_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CurrentUser**](CurrentUser.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

