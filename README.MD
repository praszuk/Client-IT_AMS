# Client application for Cisco - IT Assets Management System.

It will helps to handle with multiple hardware check-in/checkout and generates protocols. 

## Installation
1. Download the newest version using git clone:

    ```
    git clone https://github.com/praszuk/Client-IT_AMS.git
    ```
    or from [here](https://github.com/praszuk/Client-IT_AMS/archive/master.zip).

2. Install python, packet manager, virtualenv:
    - Python3.6 (with [tkinter](https://tkdocs.com/tutorial/install.html)). 
    - Package manager i.e. PIP.
    - It's recommended to use virtual environment i.e. to use [virtualenv](https://pypi.org/project/virtualenv/).

3. Install requirements:

    ```
    pip install -r requirements.txt
    ```
 
## Configuration
Start application using:

    python Main.py
    
It should generate empty config file _.config.txt_:
```
[GENERAL]
template_file_path=<path to .docx document>
[API]
url=<your url to hardware API>
token=<api token with "Bearer" >
[PRODUCT_INFO_API]
grant_type=client_credentials
client_id=<client_id>
client_secret=<client_secret>
```

1. _template_file_path_ - path to .docx file see [this file](Util/DocumentGenerator.py) for more information.
2. _url_ -  ip or url to your [Snipe-It](https://github.com/snipe/snipe-it) system (without slash as last character) i.e. ```snipe-it.example.com```.
3. _token_ is from snipe-it app i.e. ```Bearer your-secret-token``` it can be obtained from [here](https://snipe-it.readme.io/v4.6.3/reference#generating-api-tokens).
4. _grant_type_ - it's default auth type for Cisco API. Don't change this if you don't need.
5. _client_id_ - it's required to Product info API to use Auto-Add function. You need verified account (as partner account or employee account) at [developer cisco](https://developer.cisco.com/docs/support-apis/#!product-information).
6. _client_secret_ - same as above.


## How to use
1. Launch application.
![Main view](https://user-images.githubusercontent.com/23036224/45760760-1c58d700-bc2b-11e8-8c81-3999038d2038.png)
2. Use _Edit_ button to launch input data and fill with serial numbers, then press ok.
![image](https://user-images.githubusercontent.com/23036224/45761703-0a783380-bc2d-11e8-9faa-4761e544998f.png)
    
    Application will try to connect to internal snipe-it system first:
![image](https://user-images.githubusercontent.com/23036224/45761808-43b0a380-bc2d-11e8-9df4-5b39a3be428b.png)
    
    If you don't have assets in your system yet. App will try to connect to Cisco Product Info API.
    If serial number is unique and asset exists in Cisco API database. You should get something like this:
![image](https://user-images.githubusercontent.com/23036224/45762264-48298c00-bc2e-11e8-895c-05e836c65b00.png)
    
    Then you can use Auto-add feature. Select asset with status "READY_TO_ADD" and auto-add button should be active.
![image](https://user-images.githubusercontent.com/23036224/45762500-c7b75b00-bc2e-11e8-9483-c8024fc6601c.png)

    If you press Auto-add button, app will try add this to your internal system.   
3. Use _Generate_ button to generate docx protocol of this data.
You can use your own template. Check [this file](Util/DocumentGenerator.py) for more information.
![image](https://user-images.githubusercontent.com/23036224/45762993-e79b4e80-bc2f-11e8-923d-41e6e2ddaecb.png)
![image](https://user-images.githubusercontent.com/23036224/45763405-abb4b900-bc30-11e8-96dd-80cbbe219a5f.png)

4. Use _Check-in all_ button to check-in deployed assets.