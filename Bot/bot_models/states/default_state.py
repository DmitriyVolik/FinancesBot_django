from Bot.bot_models.states.state import state

class default_state(state):
    def get_uid(self) -> str:
        return 'default'
