import pandas
import numpy
import io
from starlette.responses import StreamingResponse

from app.utils.file_extraction_utility import download_public_s3_file

def dataframe_to_csv(df):
    
    """
    Converts a Pandas DataFrame into a CSV file and returns a StreamingResponse
    suitable for returning to a web client.

    :param df: A Pandas DataFrame object
    :return: A StreamingResponse containing the CSV file data
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    # Return CSV file response
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=equipment_monitor.csv"}
    )

def start_stop_detection(url:str, significance_threshold:int):
    """
    Downloads a CSV file from the given S3 URL and applies the detection logic as follows:
    - If pressure_1 increases by more than significance_threshold and pressure_2 does not increase and temperature decreases, flag equipment_stop as True.
    - If pressure_1 decreases and temperature increases, flag equipment_restart as True.
    - Create stop_time and restart_time columns with the timestamp of the corresponding event.
    - Drop all rows where both stop_time and restart_time are NaN.
    - Return the resulting DataFrame as a CSV file.
    """    
    csv_data = download_public_s3_file(url)
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

