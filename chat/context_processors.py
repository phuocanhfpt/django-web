from .models import ChatConfig

def chat_config(request):
    config = ChatConfig.get_config()
    print("DEBUG context processor: config =", config, "is_enabled =", getattr(config, 'is_enabled', None))
    return {
        'chat_config': config
    } 