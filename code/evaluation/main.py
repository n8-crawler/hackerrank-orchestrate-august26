from pathlib import Path

from services.dataloader import DataLoader
from pipeline.stateclass import NotificationState
from pipeline.pipeline import graph_compile
import pandas as pd

def run_agents():
    processed_messages = []

    for message in DataLoader().new_messages:
        if message.message_id in processed_messages or message.notification is not None:
            continue
        else:
            processed_messages.append(message.message_id)

            state = NotificationState(
                message_id=message.message_id
            )

            result = graph_compile.invoke(state)            

            file_path = Path(__file__).parent.parent.parent / "dataset" / "output.csv"

            decision = result['decision'].model_dump(mode="json")
            print("AI output>>>>>>>>>",decision)
            df = pd.read_csv(file_path,dtype=str)
            row = df['message_id']==decision['message_id']
            for key,value in decision.items():

                if isinstance(value,list):
                    value = ','.join(value)
                if isinstance(value,float):
                    value = str(value)
                
                df.loc[row,key]=value

            df.to_csv(file_path,index=False)
        
if __name__ == "__main__":
    run_agents()
