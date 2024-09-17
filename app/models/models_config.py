global_registered_models= [
    {"model_name": 'all-MiniLM-L6-v2',"model_category":'embedding','link':'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2', "hf_repo":'sentence-transformers/all-MiniLM-L6-v2'},
    {"model_name": 'llama-3.1-70b-versatile',"model_category":'generative-api',"model_family":'GroqAIModels'},
    {"model_name": 'gemini-flash-1.5',"model_category":'generative-api',"model_family":'GoogleGenAIModels'},

]


global_model_finetuning_prompt_wrappers_lookup = {

        #   each wrapper can consist of up to 5 elements to represent common segments of the prompt
        #   1.  optional - "system_start" and "system_stop"
        #   2.  required - "main_start" and "main_stop"
        #   3.  required - "start_llm_response"

        "human_bot": {"main_start": "<human>: ", "main_stop": "\n", "start_llm_response": "<bot>:"},

        "<INST>": {"main_start": "<INST>", "main_stop": "</INST>", "start_llm_response": ""},

        "hf_chat": {"system_start": "<|im_start|>system\n", "system_stop": "<|im_end|>\n",
                    "main_start": "<|im_start|>user", "main_stop": "<|im_end|>\n",
                    "start_llm_response": "<|im_start|>assistant"},

        "open_chat": {"main_start": "GPT4 User: ", "main_stop": "<|endofturn|>",
                      "start_llm_response": "GPT4 Assistant:"},

        "alpaca": {"main_start": "### Instruction: ", "main_stop": "\n",
                   "start_llm_response": "### Response: "},

        "chat_ml": {"system_start": "<|im_start|>system", "system_stop":"<|im_end|>\n",
                    "main_start":"<|im_start|>user", "main_stop":"<|im_end|>\n",
                    "start_llm_response":"<|im_start|>assistant"},

        "phi_3": {"system_start": "<|system|>\n", "system_stop": "<|end|>\n",
                  "main_start": "<|user|>\n", "main_stop": "<|end|>\n", "start_llm_response": "<|assistant|>"},

        "llama_3_chat": {"system_start": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n",
                         "system_stop": "<|eot_id|>",
                         "main_start": "<|start_header_id|>user>|end_header_id|>\n",
                         "main_stop": "<|eot_id|>",
                         "start_llm_response": "<|start_header_id|>assistant<|end_header_id|>\n"},

        "tiny_llama_chat": {"system_start": "<|system|>", "system_stop": "</s>",
                            "main_start": "<|user|>", "main_stop": "</s>",
                            "start_llm_response": "<|assistant|>"},

        "stablelm_zephyr_chat": {"system_start": "", "system_stop": "",
                                 "main_start": "<|user|>", "main_stop": "<|endoftext|>\n",
                                 "start_llm_response": "<|assistant|>"},

        "google_gemma_chat": {"system_start": "", "system_stop": "",
                              "main_start": "<bos><start_of_turn>user\n",
                              "main_stop": "<end_of_turn>\n",
                              "start_llm_response": "<start_of_turn>model"},

        "vicuna_chat": {"system_start": "", "system_stop": "",
                        "main_start": "USER: ", "main_stop": "",
                        "start_llm_response": " ASSISTANT:"}

}

""" Global default prompt catalog consists of a set of prebuilt useful prompt instructions across a wide range
of models.   Unlike prompt_wrappers, which tend to be an attribute of the model, the prompt catalog can be invoked
on a 'prompt-by-prompt' basis to drive different behavior from a model.   Note:  not all models will support
 very complex open-ended instructions or respond in a consistent manner. """



global_default_prompt_catalog = [

    {"prompt_name": "just_the_facts",
     "prompt_description": "Closed Context - read passage, answer question, stick to the facts.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": " Please answer the question: ",
     "instruction": "In providing the answer, please only use facts contained in the text.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {}},

    {"prompt_name": "answer_or_not_found",
     "prompt_description": "Closed Context - read passage, answer question, provide 'Not Found' if no answer in text.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": " Please answer the question: ",
     "instruction": "Please only use facts in the text.  If the text does not provide the answer, then please "
                    "respond with: {{not_found_response}}",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {"not_found_response": "'Not Found.'"}},

    {"prompt_name": "number_or_none",
     "prompt_description": "Closed Context - read passage, answer question, provide 'Not Found' if no answer in text.",
     "run_order": ["blurb1", "$context", "blurb2", "$query","instruction"],
     "blurb1" : "Please read the following text: ",
     "blurb2" : " Please answer the question: ",
     "instruction": "Please provide a specific number as an answer from the text.  "
                    "If the text does not provide a specific numerical answer, then please respond "
                    "with: {{not_found_response}}",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {"not_found_response": "'Not Found.'"}},

    {"prompt_name": "summarize_with_bullets",
     "prompt_description": "Basic summarization with open ended number of bullet points.",
     "run_order": ["blurb1", "$context", "instruction"],
     "blurb1": "Please read the following text: ",
     "instruction": "Please summarize with bulletpoints.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {}},

    {"prompt_name": "summarize_with_numbered_bullets",
     "prompt_description": "Summarization with specified number of bullet points.",
     "run_order": ["blurb1", "$context", "instruction"],
     "blurb1": "Please read the following text: ",
     "instruction": "Please summarize the text with approximately {{number_of_bulletpoints}} numbered bulletpoints.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {"number_of_bulletpoints": 5}},

    {"prompt_name": "xsummary",
     "prompt_description": "Xtreme summarization with specified number of words.",
     "run_order": ["blurb1", "$context", "instruction"],
     "blurb1": "Please read the following text: ",
     "instruction": "Please summarize the text in no more than {{number_of_words}} words.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {"number_of_words": 25}},

    {"prompt_name": "completion",
     "prompt_description": "Open context text generation to complete starting point provided in prompt.",
     "run_order": ["blurb1", "$query", "instruction"],
     "blurb1": "Here is the starting point of a longer text: ",
     "instruction": "Please complete this text in the style provided in the text.",
     "system_message": "You are a helpful assistant who is a good creative writer.",
     "user_vars": {}},

    {"prompt_name": "dialog_summary",
     "prompt_description": "General summarization of a conversation text with specified number of bullet points.",
     "run_order": ["blurb1", "$context", "instruction"],
     "blurb1": "Please read the following discussion between two parties: ",
     "instruction": "Please summarize the key points from the conversation using less "
                    "than {{number_of_bulletpoints}} bulletpoints.",
     "system_message": "You are a helpful assistant.",
     "user_vars": {"number_of_bulletpoints": 10}},

    {"prompt_name": "not_found_classifier",
     "prompt_description": "Not Found Response classifier - used to ask a model to classify a particular response "
                           "as 'not found' - very useful in RAG applications.",
     "run_order": ["blurb1", "blurb2", "$context", "instruction"],
     "blurb1": "Here are several examples of a 'not found' response: "
               "Not Found \n"
               "The text does not provide an answer. \n"
               "The answer is not clear. \n"
               "Sorry, I could not find a definitive answer. \n"
               "The answer is not provided in the information given. \n"
               "The text does not specify the answer to this question. \n",
     "blurb2": "Here is a new example: ",
     "instruction": "Please respond 'Yes' or 'No' if this new example is a 'Not Found' response.",
     "system_message": "You are a helpful assistant.",
     "user_vars": {}},

    {"prompt_name": "top_level_select",
     "prompt_description": "Select the best answer among choices provided.",
     "run_order": ["blurb1", "$query", "blurb2","$context", "instruction"],
     "blurb1": "We are trying to answer the following question: ",
     "blurb2": "Which of the following selections best answers the question?",
     "instruction": "Please respond with the best answer among these selections.  "
                    "If more than one answer is useful, please summarize with bulletpoints.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {}},

    {"prompt_name": "answer_question_in_role",
     "prompt_description": "Answer a question with a specific role or point of view.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Please answer the following question: ",
     "instruction": "In providing an answer to the question, please assume the perspective of a {{role}} and "
                    "write in that style.",
     "system_message": "You are a helpful assistant.",
     "user_vars": {"role": "business analyst"}},

    {"prompt_name": "editor_in_role",
     "prompt_description": "Edit a passage with a specific role or point of view.",
     "run_order": ["blurb1", "$context", "instruction"],
     "blurb1": "Please read the following text: ",
     "instruction": "Our task is to edit and improve the language of the text from the perspective of a business analyst.",
     "system_message": "You are a helpful editor and writer who reads text and improves the writing.",
     "user_vars": {"role": "business analyst"}},

    {"prompt_name": "yes_no",
     "prompt_description": "Answer a question with 'Yes' or 'No'.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Based on these materials, please answer the question: ",
     "instruction": "Please answer this question with 'Yes' or 'No'.  If the text does not provide an answer,"
                    "then please respond with 'Not Found.'",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words.",
     "user_vars": {}},

    {"prompt_name": "multiple_choice",
     "prompt_description": "Answer a question using a set of pre-defined choices provided.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Based on these materials, please answer the question: ",
     "instruction": "Please select from the choices provided.  If the text does not provide an answer,"
                    "then please respond with 'Not Found.'",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words."},

    {"prompt_name": "default_with_context",
     "prompt_description": "Default simple prompt when a question and context are passed.",
     "run_order": ["blurb1", "$context", "blurb2", "$query"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Based on this text, please answer the question: ",
     "instruction": "",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words."},

    {"prompt_name": "default_no_context",
     "prompt_description": "Default simple prompt when only a question is passed.",
     "run_order": ["blurb1","$query"],
     "blurb1": "Please discuss the following: ",
     # "blurb2": "Based on this text, please answer the question: ",
     "instruction": "",
     "system_message": "You are a helpful assistant who likes to answer questions."},

    {"prompt_name": "summarize_with_bullets_w_query",
     "prompt_description": "Summarization of a text with a specific question being posed.",
     "run_order": ["blurb1", "$context", "blurb2","$query","instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Please read the following question: ",
     "instruction": "Please summarize with bulletpoints an analysis of the question.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words."},

    {"prompt_name": "summarize_with_references_w_query",
     "prompt_description": "Summarization with text with guidance to provide reference to specific "
                           "information in the text passage.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Please read the following question: ",
     "instruction": "Please provide an analysis of the question using information and specific clauses "
                    "in the text.",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words."},

    {"prompt_name": "write_poem",
     "prompt_description": "Write a poem prompt - note: results may vary greatly by model.",
     "run_order": ["instruction", "$query"],
     "instruction": "Please write a poem using the following prompt: ",
     "system_message": "You are a helpful assistant who is a creative writer and can rhyme words easily."},

    {"prompt_name": "ten_words",
     "prompt_description": "Xtreme summarization to answer question from a text in 10 words of less.",
     "run_order": ["instruction", "$query", "$context"],
     "blurb1": "Please read the following text: ",
     "blurb2": "Please read the following question: ",
     "instruction": "In no more than ten words, please give concise answer to the following question, using the "
                    "text as evidence to support",
     "system_message": "You are a helpful assistant who speaks with facts and no wasted words."},

    {"prompt_name": "explain_child",
     "prompt_description": "Standard simplified answer prompt - note: results may vary greatly by model.",
     "run_order": ["instruction", "$query", "$context"],
     "instruction": "Please explain to a child the following question using the provided text: ",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "make_joke",
     "prompt_description": "Standard joke prompt - note:  results may vary greatly by model.",
     "run_order": ["instruction", "$query"],
     "instruction": "Please be funny and tell a joke on the subject of: ",
     "system_message": "You are a helpful assistant with a good sense of humor."},

    {"prompt_name": "tell_story",
     "prompt_description": "Standard tell a story prompt - note: results may vary greatly by model.",
     "run_order": ["instruction", "$query"],
     "instruction": "Please write the start of a story on the topic of: ",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "write_headline",
     "prompt_description": "Generate a headline from a question and context.",
     "run_order": ["instruction", "$query", "$context"],
     "instruction": "Please write the headline only in a few words in capitalization to answer the question below, "
                    "using the materials provided. ",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "facts_only",
     "prompt_description": "Basic 'facts only' Q&A prompt.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please use the following materials- ",
     "blurb2": "Please answer the following question - ",
     "instruction": "In answering the question, please only use information contained in the provided materials.",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "top_bulletpoints",
     "prompt_description": "Summarization with question and answer in 5 bullet points.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the text below -  ",
     "blurb2": "Please read the following question - ",
     "instruction": "Please answer the question using the text, and write no more than 5 bulletpoints.",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "report_title",
     "prompt_description": "Generate title of report given context passage.",
     "run_order": ["instruction", "$context"],
     "instruction": "Please write the title to a report with the following information:  ",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "marketing_slogan",
     "prompt_description": "Generate marketing style slogan given context passage.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following materials- ",
     "blurb2": "Please answer the following question - ",
     "instruction": "Please write a marketing slogan for the following offering using the following information as "
                    "background source materials.",
     "system_message": "You are a helpful assistant."},

    {"prompt_name": "top_level_summary",
     "prompt_description": "Summarization prompt intended for 'second-level' summaries of materials.",
     "run_order": ["blurb1", "$context", "blurb2", "$query", "instruction"],
     "blurb1": "Please read the following materials- ",
     "blurb2": "Please answer the following question - ",
     "instruction": "In answering the question, please write no more than five bulletpoints, and reference the most "
                    "important facts in the source materials.",
     "system_message": "You are a helpful assistant."},

]


