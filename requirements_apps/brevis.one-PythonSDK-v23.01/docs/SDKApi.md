# swagger_client.SDKApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sdk_download_lang_get**](SDKApi.md#sdk_download_lang_get) | **GET** /sdk/download/{lang} | Download swagger client sdk for the passed language.

# **sdk_download_lang_get**
> str sdk_download_lang_get(lang)

Download swagger client sdk for the passed language.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SDKApi()
lang = 'lang_example' # str | The following language have been tested.`csharp`, `java`, `php`, `python`. But you can pass any of the supported languages by swagger-codegen <a href=\"https://github.com/swagger-api/swagger-codegen#overview\">Read more</a>          

try:
    # Download swagger client sdk for the passed language.
    api_response = api_instance.sdk_download_lang_get(lang)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SDKApi->sdk_download_lang_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lang** | **str**| The following language have been tested.&#x60;csharp&#x60;, &#x60;java&#x60;, &#x60;php&#x60;, &#x60;python&#x60;. But you can pass any of the supported languages by swagger-codegen &lt;a href&#x3D;\&quot;https://github.com/swagger-api/swagger-codegen#overview\&quot;&gt;Read more&lt;/a&gt;           | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

