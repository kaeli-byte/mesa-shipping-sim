"""Minimal random activation scheduler."""


class RandomActivation:
    def __init__(self, model: object) -> None:
        self.model = model
        self._agents: list[object] = []

    def add(self, agent: object) -> None:
        self._agents.append(agent)

    def step(self) -> None:
        agents = list(self._agents)
        self.model.random.shuffle(agents)
        for agent in agents:
            agent.step()
