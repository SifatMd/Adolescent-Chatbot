from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


bot = ChatBot(
    'SQLMemoryTerminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'default_response': 'chatterbot failed'
        }
    ],
    database_uri='sqlite:///chatterbot_database.db',
    read_only=True
)


def train(filename):

    f = open(filename, "r", encoding="utf-8")
    corpus = []
    for line in f:
        if line.strip() == "*****************************************************************************************************":
            break
        corpus.append(line.strip())
        
    samples = []
    for i in range(0, len(corpus)-1, 2):
        dialog = []
        dialog.append(corpus[i])
        dialog.append(corpus[i+1])
        samples.append(dialog)

    trainer = ListTrainer(bot)
    for dialog in samples:
        trainer.train(dialog)



def get_chatterbot_response(fb_messenger, user_text, user_id):
    response = bot.get_response(user_text)

    if response.confidence < 0.5:
        return False

    fb_messenger.send_text_message(user_id, response.text)
    return True


def debug(user_text):
    response = bot.get_response(user_text)
    return response