cd ~/llama-mcp

python3 -m llama_cpp.server --model /home/nik/llama-mcp/models/qwen2.5-coder-1.5b-q8_0.gguf --n_gpu_layers=-1 --n_ctx=4096 --port 8012
