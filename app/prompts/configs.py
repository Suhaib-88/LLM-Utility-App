from models.configs import ModelCatalog
import os
from  vector_stores.configs import LLMAppConfig
from prompts.resources import PromptState
from models.configs import _ModelRegistry
from models.models_config import global_default_prompt_catalog

class Prompt:

    """
    """

    def __init__(self, llm_name=None, model_card=None,account_name='app', llm_model=None,save_state=True,temperature=0.3,llm_api_key=None, prompt_catalog=None, prompt_id= None):

        self.account_name=account_name
        self.model_card=model_card
        self.llm_model=None
        self.llm_model_api_key=llm_api_key
        self.llm_model_card=None

        if model_card:
            if "model_name" in model_card:
                self.llm_model= ModelCatalog().load_model(model_card['model_name'], api_key= llm_api_key)
                self.llm_model_card= model_card

        if llm_name:
            self.llm_model= ModelCatalog().load_model(llm_name, api_key= llm_api_key)

        self.temperature = temperature

        if prompt_id:
            PromptState(self).load_state(prompt_id)
            self.prompt_id= prompt_id

        else:
            new_prompt_id= PromptState(self).issue_new_prompt_id()
            self.prompt_id= PromptState(self).initiate_new_state_session(new_prompt_id)


        self.save_prompt_state= save_state
        self.interaction_history= []
        self.dialog_tracker= []
        self.llm_state_vars= ["llm_response",'prompt', 'instruction','prompt_id']

        if prompt_catalog:
            self.pc= prompt_catalog

        else:
            self.pc= PromptCatalog()

        self.prompt_catalog= self.pc.get_all_prompts()

        self.source_materials= []

        self.batch_separator= '\n'
        self.query_results= None
        self.model_catalog= ModelCatalog()

        if not os.path.exists(LLMAppConfig.get_llmapp_path()):
            LLMAppConfig.setup_llmapp_workspace()

        self.prompt_path= LLMAppConfig.get_prompt_path()
        if not os.path.exists(self.prompt_path):
            os.mkdir(self.prompt_path)
            os.chmod(self.prompt_path, '0077')

        
class PromptCatalog:
    def __init__(self):
        self.prompt_catalog= global_default_prompt_catalog
        self.prompt_wrappers= _ModelRegistry().prompt_wrappers 
        self.prompt_wrapper_lookup= _ModelRegistry().get_wrapper_list()
        self.prompt_list= self.list_all_prompts()

    def list_all_prompts(self):
        prompt_list= []
        for prompt in self.prompt_catalog:
            if "prompt_name" in prompt:
                prompt_list.append(prompt["prompt_name"])
        return prompt_list

    def get_all_prompts(self):
        return self.prompt_catalog
    
    