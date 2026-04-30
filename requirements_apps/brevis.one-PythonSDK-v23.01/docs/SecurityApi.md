# swagger_client.SecurityApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**signin_post**](SecurityApi.md#signin_post) | **POST** /signin | Exchange a username and password with a bearer token

# **signin_post**
> TokenSigninResponse signin_post(body)

Exchange a username and password with a bearer token

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecurityApi()
body = swagger_client.TokenSigninPayload() # TokenSigninPayload | 

try:
    # Exchange a username and password with a bearer token
    api_response = api_instance.signin_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityApi->signin_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TokenSigninPayload**](TokenSigninPayload.md)|  | 

### Return type

[**TokenSigninResponse**](TokenSigninResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

