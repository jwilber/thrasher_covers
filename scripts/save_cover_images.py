import os
import requests

import pandas as pd


if __name__ == '__main__':

	cover_df = pd.read_csv("../data/thrasher_covers.csv")

	for index, row in cover_df.iterrows():
	    print(row['month'], row['year'])
	    img_data = requests.get(row['cover_url']).content
	    path = "{}{}.jpg".format(row['month'], str(row['year']))
	    print(path)
	    with open(os.path.join("data", "cover_images", path).replace("\\","/"), 'wb') as handler:
	        handler.write(img_data)
