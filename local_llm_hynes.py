import mlx_lm
import os
os.environ['MLXLM_USE_MODELSCOPE'] = 'True'
from mlx_lm import load, generate

print(os.getcwd)
model, tokenizer = client.post("mlx-community/Codestral-22B-v0.1-4bit")
os.getcws
prompt = "hello"


base_url = "http://localhost:1234"

chat_endpoint = "/v1/chat/completions"
response_endpoint  = "/v1/chat/completions"
agent_endpoint = "/v1/agent/create agent"



if tokenizer.chat_template is not None:
    messages = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

response = generate(model, tokenizer, prompt=prompt, verbose=True)




# # Load library
# from LLMlight import LLMlight

# local_model='qwen/qwen3-coder-30b'

# base_url="http://localhost:1234"
# chat_endpoint='/v1/chat/completions'

# # Initialize with default settings
# client = LLMlight(
#     model=local_model,
#     endpoint="http://localhost:1234/v1/chat/completions"
# )









# # res_1 = client.prompt('can you see this message? it has no context or anything.')
# # url2=


# # # Add multiple PDF files to the database
# # url = 'https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf'
# # pdf_text = client.read_pdf(url)


# # # Create response
# # for temp in [0.99, 0.99, 0.99, 0.1, 0.1, 0.1]:
# #     response = client.prompt('Summarize how layers are used in an attention network in combination to the increasing complexity.',
# #                              context=pdf_text,
# #                              instructions='You are a helpfull assistant. Keep your answer brief.',
# #                              temperature=temp,
# #                              )

# #     print(f'Temperature: {temp}\n\n{response}')