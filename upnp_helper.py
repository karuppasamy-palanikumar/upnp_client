from flask import session
import upnpy
from upnpy.ssdp.SSDPDevice import SSDPDevice
import xml.etree.ElementTree as ET

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
    if not id:
        id = '0'
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
            result = response['Result']
            if result:
                root = ET.fromstring(result)
                result_dict = xml_element_to_dict(root)
                try:
                    return result_dict
                except:
                    return []
        except Exception as e:
            print(f"Error: {e}")
        # parameters = {'ObjectID':id, 'BrowseFlag':'BrowseDirectChildren', 'Filter':'', 'StartingIndex':0, 'RequestedCount':1000, 'SortCriteria':''}
        # print(SOAP.send(action,parameters))

# Function to convert XML element to dictionary
def xml_element_to_dict(element):
    result = {}
    # tag = None
    # """The element's name."""

    # attrib = None
    # """Dictionary of the element's attributes."""

    # text = None
    result = []
    containers = element.findall('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}container')
    if containers:
        for container in containers:
            container_dict = {}
            container_dict['id'] = container.attrib.get('id')
            container_dict['parentID'] = container.attrib.get('parentID')
            container_dict['restricted'] = container.attrib.get('restricted')
            container_dict['searchable'] = container.attrib.get('searchable')
            container_dict['childCount'] = container.attrib.get('childCount')
            container_dict['title'] = container.find('{http://purl.org/dc/elements/1.1/}title').text
            container_dict['class'] = container.find('{urn:schemas-upnp-org:metadata-1-0/upnp/}class').text
            container_dict['storageUsed'] = container.find('{urn:schemas-upnp-org:metadata-1-0/upnp/}storageUsed').text
            result.append(container_dict)
    items = element.findall('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item')
    if items:
        for item in items:
            item_dict = {}
            item_dict['id'] = item.attrib.get('id')
            item_dict['parentID'] = item.attrib.get('parentID')
            item_dict['class'] = item.find('{urn:schemas-upnp-org:metadata-1-0/upnp/}class').text
            item_dict['title'] = item.find('{http://purl.org/dc/elements/1.1/}title').text
            for res in item.findall('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res'):
                try:
                    if item_dict['res'] != None:
                        item_dict['res_1'] = res.text
                    else:
                        item_dict['res'] = res.text
                except:
                    item_dict['res'] = res.text
            
            result.append(item_dict)
    return result

def get_device():
    device_address = session["device_address"]
    device_response = session["device_response"]
    return SSDPDevice(device_address,device_response)