import os
from modelscope.hub.snapshot_download import snapshot_download

# save_dir是模型保存到本地的目录
save_dir="./models"

snapshot_download("Shanghai_AI_Laboratory/internlm2-chat-7b",
                  cache_dir=save_dir,
                  revision='v1.1.0')
