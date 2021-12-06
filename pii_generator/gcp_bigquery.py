from google.cloud import bigquery
from json import load as json_load
from google.oauth2 import service_account

try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION

  
if PRODUCTION:
    from .constants import BIG_QUERY_SCHEMA
    from .utils import is_json_path_valid
else:
    from constants import BIG_QUERY_SCHEMA
    from utils import is_json_path_valid


def get_bigquery_client(gcp_config_json: str):

  if is_json_path_valid(gcp_config_json):
      f = open(gcp_config_json)
      data = json_load(f)
      f.close()
      try:
        credential = service_account.Credentials.from_service_account_info(data)
        client = bigquery.Client(project=data["project_id"], credentials=credential)
        return [client, data.get("project_id", None), data.get("bq_dataset_name", None), data.get("bq_table_name", None)]
      except Exception as e:
        return f"message : {e}"

def remove(string):
    return string.replace(" ", "")
      
# submit the pii  data in 
def get_table_id_bq(ls: list):
  print(ls)
  result = []
  if ls[0] == None:
    project_id = input("Kindly enter the project id of gcp: ")
    result.append(project_id)
  else:
    result.append(ls[0])

  if ls[1] == None:
    dataset = input("Kindly enter the name of dataset of Gcp Bigquery: ")
    result.append(dataset)
  else:
     result.append(ls[1])
  if ls[2] == None:
    table = input("Kindly enter the name of table of Gcp Bigquery: ")
    result.append(table)
  else:
    result.append(ls[2])

  return ".".join(result)


def enter_pii_data_in_gcp_bigquery(config_path: str, dataframe):
  data = get_bigquery_client(config_path)
  if type(data) == list:
    bq_client = data[0]
    table_id = get_table_id_bq(data[1:])
    print(table_id)
    try:
      job_config = bigquery.LoadJobConfig(schema=BIG_QUERY_SCHEMA)
      load_job = bq_client.load_table_from_dataframe(
                                  dataframe,
                                  table_id, 
                                  job_config=job_config)
      print(load_job)

      load_job.result()  # Waits for the job to complete.

      destination_table = bq_client.get_table(table_id)
      print("Loaded {} rows.".format(destination_table.num_rows))
      return True
    except Exception as e:
      return f"message: {e}"
  else:
    return data
