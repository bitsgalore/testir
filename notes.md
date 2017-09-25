
## XMLLint

    xmllint --xpath ]/*[local-name()='GetRecord']/*[local-name()='record']/*[local-name()='metadata']/*[local-name()='nl_didl_combined']/*[local-name()='nl_didl_norm']/*[local-name()='DIDL']/*[local-name()='Item']/*[local-name()='Component']/*[local-name()='Resource']/@ref" didl.xml
    
    
Result:

    ref="https://dspace.library.uu.nl/bitstream/1874/86/1/HFST3.PS"
    
    
Expected result: ref attribute of *all* Resource elements, not only the first one!



## Content-Disposition

    curl -D headers.txt https://dspace.library.uu.nl/bitstream/1874/86/8/HFST1.PDF > /dev/null
    
Resultaat:

    HTTP/1.1 301 Moved Permanently
    Date: Thu, 21 Sep 2017 16:12:03 GMT
    Server: Apache-Coyote/1.1
    X-Cocoon-Version: 2.2.0
    location: /bitstream/handle/1874/86/HFST1.PDF;jsessionid=1924770D8804B591DC22C2F192DDFAF9?sequence=8
    Content-Language: en-US
    Set-Cookie: JSESSIONID=1924770D8804B591DC22C2F192DDFAF9; Path=/; HttpOnly
    Content-Length: 0
    Connection: close
    Content-Type: application/pdf

Four Tips for Setting up HTTP File Downloads:

<https://blog.httpwatch.com/2010/03/24/four-tips-for-setting-up-http-file-downloads/>
    
Suggests filename either set by URL or Content-Disposition. 