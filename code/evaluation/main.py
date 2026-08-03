from pathlib import Path
from services.dataloader import DataLoader
from pipeline.stateclass import NotificationState
from pipeline.pipeline import graph_compile
import pandas as pd

def run_agents():

    for message in DataLoader().messages:

        state = NotificationState(
            message_id=message.message_id
        )

        result = graph_compile.invoke(state)
        print("AI output>>>>>>>>>",result['decision'])

        file_path = Path(__file__).parent.parent.parent / "dataset" / "output.csv"

        df = pd.DataFrame([state.decision.model_dump()])

        df.to_csv(file_path,mode="a",index=False,header=not file_path.exists())

if __name__ == "__main__":
    run_agents()
