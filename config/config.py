import motor.motor_asyncio
import yaml

yaml_file = open("config/config.yaml",)
data = yaml.load(yaml_file, Loader = yaml.FullLoader)
db_url = data["database"]
client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = client['personal_detail']

#Initiate db
# tbl_user = db['user']
trx_collection = db['trx_collection']
# log_command = db['log_command']