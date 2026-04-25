from env import FraudDetectionEnv
from models import FraudAction

env = FraudDetectionEnv('hard_multi_step')

for scenario in range(5):
    env.reset()
    print(f'=== Scenario {scenario+1} ===')
    for sub in range(3):
        result = env.step(FraudAction(action=1))
        print(f'  Sub-step {sub+1}: {result.info["obs_explanation"]}')
        print(result.info["explanation_text"])
