import os
from utils.exceptions import ConfigKeyException, HomePathDoesNotExistException


class LLMAppConfig:
    """
    LLMApp Global configuration object use set/get to update paths 
    """
    _base_filepath= {"home_path":os.getenv("HOME_PATH"),
                     "llmapp_path_name": os.getenv("llmapp_data")+os.sep}
    
    _filepath= {"library_file_path": "accounts" + os.sep, "model_repo_path_name":'model_repo' +os.sep, 'input_path_name':'input_channel'+os.sep, "parser_path_name": "parser_history"+os.sep,
                "prompt_path_name":'prompt_history' + os.sep}
    
    @classmethod
    def get_config(cls,name):
        if name in cls._conf:
            return cls._conf[name]
        raise ConfigKeyException(name)
    
    @classmethod
    def set_config(cls,name, value):
        cls._conf[name] = value

    @classmethod
    def get_home(cls):
        return cls._base_filepath["home_path"]


    @classmethod
    def set_home(cls,new_value):
        cls._base_filepath["home_path"]=new_value

    @classmethod
    def set_llmapp_path(cls,new_value):
        cls._base_filepath["llmapp_path_name"]=new_value


    @classmethod 
    def get_fp_name(cls,file_path):
        if file_path in cls._filepath:
            return cls._filepath[file_path]
        raise ConfigKeyException(file_path)
        
    @classmethod 
    def set_fp_name(cls,file_path, new_value):
        if file_path in cls._filepath:
            cls._filepath.update({file_path,new_value})

    @classmethod
    def get_llmapp_path(cls):
        return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'])

    @classmethod
    def get_library_path(cls):
        return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'],cls._filepath["library_file_path"])
    
    @classmethod
    def get_model_repo_path(cls):
        return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'], cls._filepath['model_repo_path_name'])
    
    @classmethod
    def get_input_path(cls):
        return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'], cls._filepath['input_path_name'])
                                                                               

    @classmethod
    def get_parser_path(cls):
        return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'], cls._filepath['parser_path_name'])
    
    @classmethod
    def get_prompt_path(cls):
         return os.path.join(cls._base_filepath['home_path'],cls._base_filepath['llmapp_path_name'], cls._filepath['prompt_path_name'])


    @classmethod
    def setup_llmapp_workspace(cls):
        home_path= cls._base_filepath['home_path']
        if not os.path.exists(home_path):
            raise HomePathDoesNotExistException(home_path)
        
        llmapp_path = cls.get_llmapp_path()
        if not os.path.exists(llmapp_path):
            os.mkdir(llmapp_path)

        library_path = cls.get_library_path()
        if not os.path.exists(library_path):
            os.mkdir(library_path)
        
        model_repo_path = cls.get_model_repo_path()
        if not os.path.exists(model_repo_path):
            os.mkdir(model_repo_path)

        input_path = cls.get_input_path()
        if not os.path.exists(input_path):
            os.mkdir(input_path)

        parser_path = cls.get_parser_path()
        if not os.path.exists(parser_path):
            os.mkdir(parser_path)


class PineconeConfig:
    """ 
    Configuration object for pinecone
    """

    _conf = {
        "pinecone_api_key": os.getenv(""),
        "pinecone_cloud": os.getenv(""),
        "pinecone_region": os.getenv("")
    }

    @classmethod
    def get_config(cls,name):
        if name in cls._conf:
            return cls._conf[name]
        raise ConfigKeyException
    
    @classmethod
    def set_config(cls,name,value):
        cls._conf[name] = value


class MilvusConfig:
    """ 
    Configuration object for milvus
    """

    _conf = {
        "host": os.getenv("MILVUS_HOST", "localhost"),
        "port": os.getenv("MILVUS_PORT",19530),
        "db_name": os.getenv("MILVUS_DB",'default'),
        "partitions":[],
        'lite':False,
        'lite_folder_path': LLMAppConfig().get_library_path(),
        "lite_name":'milvus_lite.db'
    }

    @classmethod 
    def get_config(cls,name):
        if name in cls._conf:
            return cls._conf[name]
        raise "Keys not found"
    

    @classmethod 
    def set_config(cls,name,value):
        cls._conf[name] = value


class ChromaDBConfig:
    """ 
    Configuration object for chromadb
    """
    _conf = {
        'persistent_path': LLMAppConfig().get_library_path(),
        'host':os.getenv("CHROMA_HOST",None),
        'port': os.getenv("CHROMA_PORT",8000),
        'ssl':os.getenv("CHROMA_SSL",False),
        'headers':os.getenv("CHROMA_HEADERS",{}),
        'auth_provider':os.getenv("CHROMA_SERVER_AUTH_PROVIDER",None),
        "auth_credentials_provider": os.getenv("",None),
        'user':os.getenv("CHROMA_USERNAME",'admin'),
        'password':os.getenv("CHROMA_PASSWORD",'admin'),
        "auth_credentials_file":os.getenv("CHROMA_SERVER_AUTH_CREDENTIALS_FILE",'server.htpasswrd'),
        "auth_credentials":os.getenv("CHROMA_SERVER_AUTH_CREDENTIALS",None),
        "auth_token_transport_header": os.getenv("CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER",None)
        }
    
    @classmethod
    def get_db_configs(cls):
        configs={}
        for keys,values in cls._conf.items():
            configs.update({keys:values})
        return configs
    
    @classmethod
    def get_configs(cls,name):
        if name in cls._conf:
            return cls._conf[name]
        raise "Keys not found"
    
    @classmethod
    def set_configs(cls,name,value):
        cls._conf[name] = value

    @classmethod
    def get_user_name(cls):
        return cls._conf['user']
    
    @classmethod
    def get_db_pw(cls):
        return cls._conf['password']
    
    @classmethod
    def get_auth_provider(cls):
        return cls._conf['auth_provider']
    
    @classmethod
    def get_auth_credentials_provider(cls):
        return cls._conf['auth_credentials_provider']
    
    @classmethod
    def get_auth_credentials_file(cls):
        return cls._conf['auth_credentials_file']
    
    @classmethod
    def get_auth_credentials(cls):
        return cls._conf['auth_credentials']
    
    @classmethod
    def get_auth_token_transport_header(cls):
        return cls._conf['auth_token_transport_header']
    