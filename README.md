# YS-FS-Add-Ons-Auto-Installer

Python script for correctly install 3rd-party add-ons into YSFlight folder.

> This script covers majority of the add-on packages I downloaded from the web. It assumes that the user data is under `User` or `user` sub-directory somewhere in the .zip file.
> 
> Windows doesn't care about capitalization, but Linux and macOS do.
> 
> Therefore, this script looks into .lst files and correct capitalization if the file name in the .lst file does not match the capitalization of the actual file.
> 
> Now at least I can test that the program does not crash or freeze if I install add-on packages in a batch!
> 
> Of course you need to have Python installed on your system to use this script.
> 
> This script has been tested with Python 3.6.  It may run with Python 2.x, but I haven't tested.
> 
> BSD License.  Free for re-distribution.  Please feel free to customize for your own add-on package and bundle with package.
> 
> Usage:
> 
> ```
> $ python install_addon.py package_zip_file.zip
> ```
> or
> ```
> $ python install_addon.py package_zip_file.zip install_directory
> ```
> 
> If you do not specify the install_directory, the script installs to the default YSFLIGHT user directory (`~/Documents/YSFLIGHT.COM/YSFLIGHT`)

## CREDITS

```
install_addon.py
Copyright (c) 2018 Soji Yamakawa.  All rights reserved.
http://www.ysflight.com

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS 
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
