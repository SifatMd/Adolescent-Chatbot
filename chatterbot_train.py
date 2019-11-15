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


if __name__=="__main__":
    filename = "general.txt"
    train(filename=filename)