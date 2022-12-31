# %%
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# %%
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import random