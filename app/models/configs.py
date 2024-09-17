from models.models_config import global_registered_models, global_model_finetuning_prompt_wrappers_lookup
from utils.exceptions import LLMAppException
import os, importlib
from vector_stores.configs import LLMAppConfig

class _ModelRegistry:
    registered_models= global_registered_models
    model_classes= {
        "GroqAIModels":{'module':'app.models.configs', 'open_source':False},
        "GoogleGenAIModels":{'module':'app.models.configs', 'open_source':False},
    }
    prompt_wrappers = ["alpaca", "human_bot", "chatgpt", "<INST>", "open_chat", "hf_chat", "chat_ml", "phi_3",
                       "llama_3_chat","tiny_llama_chat","stablelm_zephyr_chat", "google_gemma_chat",
                       "vicuna_chat"]
    registered_wrappers= global_model_finetuning_prompt_wrappers_lookup

    @classmethod
    def get_model_list(cls):
        return cls.registered_models
    
    @classmethod
    def get_model_classes(cls):
        return cls.model_classes

    @classmethod
    def add_model_classes(cls,new_class,module='app.models.configs',open_source=False):
        cls.model_classes.update({new_class:{"module":module, "open_source":open_source}})

    @classmethod
    def get_wrapper_list(cls):
        return cls.registered_wrappers


class ModelCatalog:
    def __init__(self):
        self.model_classes= _ModelRegistry().get_model_classes()
        self.global_model_list= _ModelRegistry().get_model_list() 

        self.api_key= None
        self.selected_model= None
        self.custom_loader= None

    def lookup_model_card(self,selected_model_name):
        model_card=None
        for models in self.global_model_list:
            if models['model_name']== selected_model_name or models['display_name']== selected_model_name:
                model_card= models['model_card']
                model_card.update({'standard':True})
                break
        return model_card
    
    def _instantiate_model_class_from_string(self, model_class, model_name,model_card, api_key=None,api_endpoint=None, **kwargs):
        my_model= None
        embedding_dims=None
        if "embedding_dims" in model_card:
            embedding_dims= model_card["embedding_dims"]
        if model_class in self.model_classes:
            module= self.model_classes[model_class]["module"]
            model_module = importlib.import_module(module)
            if hasattr(model_module, model_class):
                model_class= getattr(model_module, model_class)
                my_model= model_class(model_name= model_name, api_key= api_key, model_card= model_card, embedding_dims= embedding_dims, **kwargs)

        else: 
            raise LLMAppException(message= f"Exception {model_class} not found")
            
        return model_class



    def get_model_by_name(self,model_name,api_key= None,api_endpoint= None, **kwargs):
        my_model= None
        for models in self.global_model_list:
            if models['model_name'] == model_name or models['display_name']== model_name:
                selected_model= models
                my_model = self._instantiate_model_class_from_string(selected_model['model_family'], model_name, models, api_key= api_key, api_endpoint= api_endpoint, **kwargs)

        return my_model

    def load_model(self, selected_model, api_key= None, custom_loader=None,api_enpoint=None,**kwargs):
        self.selected_model= selected_model
        self.api_key= api_key
        self.custom_loader= custom_loader
        self.api_endpoints= api_enpoint
        selected_model= self.selected_model
        print(f"MODEL CATALOGUR- load_model- loading {selected_model}")

        model_card= self.lookup_model_card(self.selected_model)
        if not model_card:
            print(f'error model catalogue {self.selected_model}')
            raise ModuleNotFoundError(self.selected_model)

        my_model= self.get_model_by_name(model_card['model_name'], api_key= self.api_key, api_endpoint= self.api_endpoints, **kwargs)

        if not my_model:
            print(f'error model catalogue- couldnt identify: {self.selected_model}')
            raise ModuleNotFoundError(self.selected_model)
        
        if model_card['model_location'] == "app_repo" and not self.api_endpoints:
            loading_directions= self.prepare_local_model(model_card, custom_loader= self.custom_loader, api_key= self.api_key, **kwargs)
            my_model.load_model_for_interface(loading_directions, model_card= model_card, **kwargs)

        else:
            if api_key:
                my_model.set_api_key(api_key)
                os.environ[selected_model]= api_key

            my_model.model_name= selected_model

        return my_model
    
    def prepare_local_model(self, model_card, custom_loader=None, api_key= None, **kwargs):
        if custom_loader:
            return custom_loader(model_card, api_key= api_key)
        
        if "custom_model_repo" in model_card:
            custom_repo= model_card['custom_model_repo']

        else:
            custom_repo= None

        if custom_repo and os.path.exists(custom_repo):
            custom_local_path= self.check_custom_local_repo(model_card, api_key= api_key)
            if custom_local_path:
                return custom_local_path
            
        if not os.path.exists(LLMAppConfig.get_llmapp_path()):
            LLMAppConfig.setup_llmapp_workspace()

        if not os.path.exists(LLMAppConfig.get_model_repo_path()):
            os.mkdir(LLMAppConfig.get_model_repo_path())

        model_folder_name= model_card['model_name'].split('/')[-1]
        model_location= os.path.join(LLMAppConfig.get_model_repo_path(), model_folder_name)
        go_ahead=False

        if os.path.exists(model_location):
            go_ahead=True

            model_files= os.listdir(model_location)
            if 'validation_files' in model_card:
                for file in model_card['validation_files']:
                    if file not in model_files:
                        go_ahead=False
                        break
            if len(model_files)==0:
                go_ahead=False

            if go_ahead:
                return model_location
        
        if not go_ahead:
            fetch, fetch_method_name = self.fetch_resolve(model_card)
            if fetch and fetch_method_name:
                success= fetch(model_card, model_location, api_key= api_key, **kwargs)
                if isinstance(success, dict):
                    for k, v in success.items():
                        setattr(self,k,v)
                
                return model_location
            
            else:
                raise( LLMAppException(message="Models-load_model-selected model not found in path"))
            
    def fetch_resolve(self, model_card):
        fetch_module= None
        fetch_method= None
        fetch_class= None
        fetch_exec= None

        default_fetch= LLMAppConfig().get_config('model_fetch')
        if LLMAppConfig().get_config('apply_default_fetch_override'):
            fetch_module= default_fetch['module']
            if 'class' in default_fetch:
                fetch_class= default_fetch['class']
            if 'method' in default_fetch:
                fetch_method= default_fetch['method']
        
        else:
            if 'fetch_module' in model_card:
                if 'module' in model_card['fetch']:
                    fetch_module= model_card['fetch']['module']
                
                if "method" in model_card['fetch']:
                    fetch_method= model_card['fetch']['method']

                if 'class' in model_card['fetch']:
                    fetch_class= model_card['fetch']['class']
        if not fetch_module:
            fetch_module= default_fetch['module']
            if 'class' in default_fetch:
                fetch_class= default_fetch['class']
            if 'method' in default_fetch:
                fetch_method= default_fetch['method']
        module= importlib.import_module(fetch_module)

        if fetch_class:
            if hasattr(module, fetch_class):
                class_exec= getattr(module, fetch_class)()
                if hasattr(class_exec, fetch_method):
                    fetch_exec= getattr(class_exec, fetch_method)
        else:
            if hasattr(module, fetch_method):
                fetch_exec= getattr(module, fetch_method)

        return fetch_exec, fetch_method
    
    def check_custom_local_repo(self, model_card, api_key= None):
        if 'custom_local_repo' in model_card:
            if model_card['custom_local_repo']:
                if os.path.exists(model_card['custom_local_repo']):
                    if 'custom_model_files' in model_card:
                        if model_card['custom_model_files']:
                            if len(model_card['custom_local_repo']):
                                if os.path.exists(os.path.join(model_card['custom_model_repo'],model_card['custom_model_files'])):
                                    print (f"updated {model_card['custom_model_repo']}: {model_card['custom_model_files']}")

                                    return model_card['custom_model_repo']
                                
                else:
                    raise ModuleNotFoundError(f"Custom model repo path- {model_card['custom_model_repo']}")
                
        return None