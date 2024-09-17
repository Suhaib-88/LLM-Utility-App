from vector_stores.configs import LLMAppConfig
import importlib
from utils.exceptions import LLMAppException, DependencyNotInstalledException
from utils.logger import Logger
import os, tempfile, time
from prompts.configs import PromptCatalog

logger= Logger()
class BaseModel:
    def __init__(self, **kwargs):
        self.base_model_keys= InferenceHistory().get_base_model_keys()
        self.time_stamp=None
        self.model_class=None
        self.model_category=None
        for keys in self.base_model_keys:
            if keys in kwargs:
                setattr(self, keys, kwargs[keys])
            else:
                setattr(self,keys,None)

    def to_state_dict(self):
        state_dict={}
        for keys in self.base_model_keys:
            if hasattr(self,keys):
                state_dict.update({keys:getattr(self,keys)})
        return state_dict
    
    def method_resolver(self,config_name):
        process_class= ''
        process_method= ''
        state_dict=self.to_state_dict()
        process= LLMAppConfig().get_config(config_name)
        process_module= process['module']
        
        if 'class' in process:
            process_class= process_class['class']

        if 'method' in process:
            process_method= process_method['method']

        module_exec= importlib.import_module(process_module)

        if process_class:
            if hasattr(module_exec, process_class):
                class_exec= getattr(module_exec, process_class)()
                if process_method:
                    if hasattr(class_exec, process_method):
                        method_exec= getattr(class_exec, process_method)
        else:
            if hasattr(module_exec, process_method):
                method_exec= getattr(module_exec, process_method)

        if method_exec:
            success= method_exec(state_dict)
            if isinstance(success,dict):
                for k, v in success.items():
                    setattr(self,k,v)
        return True
    
    def post_init(self):
        return self.method_resolver('model_post_init')
    
    def register(self):
        return self.method_resolver('model_register')
    
    def validate(self):
        return self.method_resolver('model_validate')
    
    def preview(self):
        return self.method_resolver('model_preview')
    


class GoogleGenAIModels(BaseModel):
    def __init__(self, model_name, api_key= None, temperature= 0.7,**kwargs):
        super().__init__(**kwargs)
        self.model_class= "GoogleGenAIModels"
        self.model_catehory= 'generative'
        self.llm_response=None
        self.final_prompt= None
        self.api_key= api_key
        self.model_name= model_name
        self.model= None
        self.error_message= "Unable to connect, Please try again later..."
        self.prompt= ""
        self.post_init()

    def set_api_key(self, api_key, env_var="GOOGLE_API_KEY"):
        os.environ[env_var]= api_key
        logger.log(f"update: added and stored api key in {env_var}")
        return self
    
    def _get_api_key(self, env_var="GOOGLE_API_KEY"):
        self.api_key= os.getenv(env_var)
        return self.api_key


    def prompt_engineer(self, query, context, inference_dict= None):
        if not self.add_prompt_engineering:
            if context:
                select_prompt= "default_with_context"
            else:
                select_prompt= "default_without_context"

        else:
            selected_prompt= self.add_prompt_engineering

        prompt_dict= PromptCatalog().build_core_prompt(prompt_name= selected_prompt, separator= self.separator, query= query, context= context, inference_dict= inference_dict)
        if prompt_dict:
            prompt_engineered= prompt_dict['core_prompt']
        else:
            prompt_engineered= "Please read the following text: " + context +"and answer the question: "+ query

        return prompt_engineered

    def inference(self, prompt, add_context=None, add_prompt_engineering=None, inference_dict=None, api_key= None):
        self.prompt= prompt
        if add_context:
            self.add_context= add_context
        if add_prompt_engineering:
            self.add_prompt_engineering= add_prompt_engineering
        if inference_dict:
            if "temperature" in inference_dict:
                self.temperature= inference_dict['temperature']

            if "max_tokens" in inference_dict:
                self.temperature= inference_dict['max_tokens']
        self.preview()
        try:
            import google.generativeai as genai
        except ImportError:
            raise DependencyNotInstalledException('google-gemini-model')

        if api_key:
            self.api_key= api_key

        if not self.api_key:
            self._get_api_key(api_key)

        if not self.api_key:
            logger.log('error: invoking Google Generative model with no api_key')

        prompt_enriched= self.prompt_engineer(self.prompt, self.add_context, inference_dict=inference_dict)

        self.target_requested_output_tokens= 2000
        time_start= time.time()
        try:
            google_json_credentials= self.api_key_to_json()
            os.environ['']= google_json_credentials
            self.model=genai.GenerativeModel("gemini-1.5-flash") 
            response = self.model.generate_content(prompt_enriched)
            
            input_count=len(prompt_enriched)
            output_count= len(response.text)

            usage = {"input": input_count, "output": output_count, "total": input_count + output_count,
                     "metric": "characters","processing_time": time.time() - time_start}

        except Exception as e:
            response= "/**** Error ****/"
            usage = {"input":0, "output":0, "total":0, "metric": "characters",
                     "processing_time": time.time() - time_start}
            logger.log(f"error: Google model inference produced error: {e}")

        finally:
            os.remove(google_json_credentials)
        
        output_reponse= {"llm_response": response.text, "usage": usage}

        self.llm_response= response.text
        self.usage= usage
        self.logits= None
        self.output_tokens= None
        self.final_prompt= prompt_enriched

        self.register()
        return output_reponse


    def api_key_to_json(self):
        temp_json_path= tempfile.NamedTemporaryFile(prefix= "googlecreds", delete= False).name
        with open(temp_json_path, 'w', encoding='utf-8') as f:
            f.write(self.api_key.replace('\n', "\\n"))
        return temp_json_path




















class InferenceHistory:
    base_model_keys = ["llm_response", "usage", "logits", "output_tokens", "prompt", "add_context","final_prompt",
                       "model_name", "model_card", "temperature", "add_prompt_engineering",
                       "model_class", "model_category", "prompt_wrapper", "time_stamp"
                       ]
    inference_history= []
    global_inference_counter= 0
    save= True

    @classmethod
    def get_base_model_keys(cls):
        return cls.base_model_keys
    
    @classmethod
    def add_base_model_key(cls, new_key):
        if new_key not in cls.base_model_keys:
            cls.base_model_keys.append(new_key)
        return True
    
    @classmethod
    def delete_base_model_key(cls, keys_to_delete):
        if keys_to_delete in cls.base_model_keys:
            del cls.base_model_keys[keys_to_delete]
        return True
    
    @classmethod
    def get_transactions(cls):
        return cls.inference_history
    
    @classmethod
    def add_transaction(cls, model_state_dict):
        cls.inference_history.append(model_state_dict)
        return True
    
    @classmethod
    def get_global_inference_count(cls):
        return cls.global_inference_counter
    
    
    @classmethod
    def increment_global_inference_count(cls):
        cls.global_inference_counter+=1
        return cls.global_inference_counter
    
    @classmethod
    def reset_global_inference_count(cls):
        cls.global_inference_counter=0
        return cls.global_inference_counter
    
    @classmethod
    def get_save_status(cls):
        return cls.save
    
    @classmethod
    def set_save_status(cls,status):
        if isinstance(status, bool):
            cls.save=status
        else:
            raise LLMAppException(message="Exception: save status must be bool- True/False")
    