#   Copyright 2020 Frances M. Skinner, Christian Hill
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re

def ensure_https(url):
    if url.startswith('https'):
        return url
    if url.startswith('http'):
        return 'https' + url[4:]
    return 'https://' + url

def canonicalize_doi(doi):
    """Remove https://dx.doi.org/ etc. from start of string doi."""
    patt = '^https?:\/\/(?:dx\.)?doi\.org/'
    return re.sub(patt, '', doi)

def add_optional_kv(d, key_name, obj, attr=None, func=None):
    if obj is None:
        return
    if attr is None:
        attr = key_name.replace('-', '_')

    val = getattr(obj, attr)
    if val is not None and val != '':
        if func:
            val = getattr(val, func)()
        d[key_name] = val
    return d
