cd ~/llama-mcp

python3 -m llama_cpp.server --model ./models/functionary-small-v3.2.Q4_0.gguf --n_gpu_layers=-1 --chat_format chatml-function-calling --n_ctx=32000
