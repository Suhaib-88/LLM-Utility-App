import os ,uuid, json
from datetime import datetime
import random
from vector_stores.configs import LLMAppConfig 
class PromptState:
    def __init__(self, prompt= None):
        self.prompt= prompt
        self.prompt_state_base_name= 'prompt_'
        self.prompt_state_format= '.jsonl'

        if not os.path.exists(LLMAppConfig.get_llmapp_path()):
            LLMAppConfig.setup_llmapp_workspace()

        self.prompt_path= LLMAppConfig.get_prompt_path()
        self.output_path= LLMAppConfig.get_prompt_path()

        if not os.path.exists(self.prompt_path):
            os.mkdir(self.prompt_path)
            os.chmod(self.prompt_path, '00777')

        self.prompt_collection= None
        self.write_to_db= False

    def issue_new_prompt_id(self, custom_id=None, mode= 'uuid'):
        if custom_id:
            self.prompt.prompt_id= custom_id
        else:
            if mode== "time_stamp":
                self.prompt.prompt_id= str(datetime.now().timestamp())
            elif mode=="uuid":
                self.prompt.prompt_id= str(uuid.uuid4())
            elif mode =='random_number':
                self.prompt.prompt_id= str(random.randint(0, 1000000))

    def initiate_new_state_session(self, prompt_id=None):
        if not prompt_id:
            prompt_id= self.issue_new_prompt_id()

        self.prompt.llm_history= []
        self.prompt.prompt_id= prompt_id
        return prompt_id
    
    def load_state(self, prompt_id, prompt_path=None, clear_current_state=None):
        output= None
        if not prompt_path:
            prompt_path= self.prompt_path

        fn= self.get_prompt_state_fn_from_id(prompt_id)
        fp= os.path.join(prompt_path,fn)
        try:
            if clear_current_state:
                self.prompt_path.interaction_history=[]
            my_file= open(fp, 'r', encoding='utf-8')
            for lines in my_file:
                new_row= json.loads(lines)
                self.prompt.interaction_history.append(new_row)
                self.prompt.prompt_id= prompt_id
                output= self.prompt.interaction_history
        except:
            print(f"Could not find prompt interaction state {prompt_id}")
            output=None

        return output
    
    def get_prompt_state_fn_from_id(self,prompt_id):
        fn= self.prompt_state_base_name +str(prompt_id)+ self.prompt_state_format 
        return fn