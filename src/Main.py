from GameEngine import Engine

engine = Engine()
while engine.state_RUNNING:
    engine.state_PLAYING = True
    engine.loop()
