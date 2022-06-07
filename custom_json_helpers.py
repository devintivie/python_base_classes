import json
import re

camel_pat = re.compile(r'([A-Z])')

def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

snake_pat = re.compile(r'_([a-z])')
def underscore_to_camel(name):
    return snake_pat.sub(lambda x: x.group(1).upper(), name)
class custom_json_encoder(json.JSONEncoder):
    def default(self, obj):
        return self.convertJSON(obj.__dict__)

    def selected_conversion(self, currentKey):
        return currentKey

    def convertJSON(self, j):
        out = {}
        for k in j:
            newK = self.selected_conversion(k)
            if isinstance(j[k],dict):
                out[newK] = self.convertJSON(j[k])
            elif isinstance(j[k],list):
                out[newK] = self.convertArray(j[k])
            else:
                out[newK] = j[k]
        return out

    def convertArray(self, a):
        newArr = []
        for i in a:
            if isinstance(i,list):
                newArr.append(self.convertArray(i))
            elif isinstance(i, dict):
                newArr.append(self.convertJSON(i))
            else:
                newArr.append(i)
        return newArr

class camel_case_encoder(custom_json_encoder):
    def selected_conversion(self, currentKey):
        return underscore_to_camel(currentKey)

class snake_case_encoder(custom_json_encoder):
    def selected_conversion(self, currentKey):
        return camel_to_underscore(currentKey)


        