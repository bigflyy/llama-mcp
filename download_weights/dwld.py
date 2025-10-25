from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="ggml-org/Qwen2.5-Coder-1.5B-Q8_0-GGUF",
    filename="qwen2.5-coder-1.5b-q8_0.gguf",
    local_dir="./models"
)