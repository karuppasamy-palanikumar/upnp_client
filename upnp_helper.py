from flask import session
import upnpy
from upnpy.ssdp.SSDPDevice import SSDPDevice
from upnpy.soap import SOAP

upnp = upnpy.UPnP()

def discover():
    try:
        devices = upnp.discover()
        return devices
    except:
        print('Discover Error')
        return None
    

def media(device,id='0',action_str="Browse"):
    if not device:
        return None
    service = None
    action = None
    if not service:
        for _service in device.get_services():
            if _service.type_ == "ContentDirectory":
                service = _service
                for _action in _service.get_actions():
                    if _action.name == action_str:
                        action = _action
                        break
                break
    if service and action:
        browse_params = {
            'ObjectID': id,
            'BrowseFlag': 'BrowseDirectChildren',  # or 'BrowseMetadata', etc.
            'Filter': '*',
            'StartingIndex': '0',
            'RequestedCount': '1000',
            'SortCriteria': ''
        }

        # Invoke the 'Browse' action
        try:
            response = action(**browse_params)
            print(response)
            print(SOAP._parse_response(response=response['Result'],action_name=action_str))
        except Exception as e:
            print(f"Error: {e}")
        # parameters = {'ObjectID':id, 'BrowseFlag':'BrowseDirectChildren', 'Filter':'', 'StartingIndex':0, 'RequestedCount':1000, 'SortCriteria':''}
        # print(SOAP.send(action,parameters))


def get_device():
    device_address = session["device_address"]
    device_response = session["device_response"]
    return SSDPDevice(device_address,device_response)