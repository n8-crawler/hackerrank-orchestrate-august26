from pathlib import Path

from code.services.dataloader import DataLoader
from pipeline.stateclass import NotificationState
from pipeline.pipeline import graph_compile
import pandas as pd

results = []

for message in DataLoader().messages:

    state = NotificationState(

        message_id=message.message_id

    )

    result = graph_compile.invoke(state)

    results.append(result["decision"])

rows = [decision.model_dump() for decision in results]
df = pd.DataFrame(rows)

print(df.head())

file_path = Path(__file__).parent.parent/"dataset"/"output.csv"

df.to_csv(str(file_path), index=False)
