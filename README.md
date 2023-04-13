# Diabotical WER Discord Bot

### To Build

docker build --pull --rm -f "dockerfile" -t "iampgr4/diabotical-wer-discord-bot:1.0.0.0" "."

### To Push

docker push iampgr4/diabotical-wer-discord-bot:1.0.0.0

### To Run the Container with a volume

docker run -v "db-data" "iampgr4/diabotical-wer-discord-bot:1.0.0.0"
