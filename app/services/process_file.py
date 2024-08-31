import pandas
import numpy
import io
from starlette.responses import StreamingResponse

from app.utils.file_extraction_utility import download_public_s3_file_to_dataframe

def dataframe_to_csv(df):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    # Return CSV file response
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=equipment_monitor.csv"}
    )

async def start_stop_detection(url:str, significance_threshold:int):
    csv_data = download_public_s3_file_to_dataframe(url)
    df = pandas.read_csv(csv_data)
    df.loc[((df["pressure_1"].diff() > significance_threshold) & (df["pressure_2"].diff() == 0) & (df["temperature"].diff() < 0)), 'equipment_stop'] = True
    df['equipment_stop'].fillna(False, inplace=True)
    df.loc[(df["pressure_1"].diff() < 0) & (df['temperature'].diff() > 1), "equipment_restart"] = True
    df['equipment_restart'].fillna(False, inplace=True)
    # df['stop_time'] = df.apply(lambda x: x['timestamp'] if x['equipment_stop'] else numpy.nan, axis=1)
    # df['restart_time'] = df.apply(lambda x: x['timestamp'] if x['equipment_restart'] else numpy.nan, axis=1)
    df['stop_time'] =  numpy.where(df['equipment_stop'], df['timestamp'], numpy.nan)
    df['restart_time'] =  numpy.where(df['equipment_restart'], df['timestamp'],  numpy.nan)
    df = df[["equipment_name", "stop_time", "restart_time"]].dropna(how="all", subset=["stop_time", "restart_time"])
    return dataframe_to_csv(df)

# url = "https://enfinite-public.s3.amazonaws.com/sample_data/sample_event_detection.csv"
