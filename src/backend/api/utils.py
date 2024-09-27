import uuid
from fastapi import HTTPException

has_api_terms= ["api",'key','token']

def has_api_terms(word):
    return "api" in word and ('key' in word or ('token' in word and 'tokens' not in word))

def remove_api_keys(flow):
    if flow.get("data") and flow['data'].get('nodes'):
        for node in flow ['data']['nodes']:
            node_data= node.get('data').get('node')
            template = node_data.get('template')
            for value in template.values():
                if isinstance(value,dict) and has_api_terms(value['name']) and value.get('password'):
                    value['value']= None

    return flow


def validate_is_component(flows:list[Flow]):
    for flow in flows:
        if not flow.data or flow.is_component is not None:
            continue
        is_component = get_is_component_from_data(flow.data)

        if is_component is not None:
            flow.is_component = is_component
        else:
            flow.is_component = len(flow.data.get('nodes', []))==1
    return flows

def get_is_component_from_data(data:dict):
    return data.get('is_component')