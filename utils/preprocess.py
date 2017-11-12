import os
from datetime import datetime
from loader import Loader
import numpy as np
from sklearn.preprocessing import normalize

files = os.listdir(os.path.join(os.path.dirname(__file__), '../data/'))
json_files = [file for file in files if 'json' in file]

# vote by our team
language_weight = {
    'C++': 6,
    'Pascal': 1,
    'C': 7,
    'TypeScript': 1,
    'Python': 7,
    'CSS': 1,
    'Shell': 1,
    'JavaScript': 1,
    'Go': 6,
    'TeX': 1,
    'HTML': 1,
    'Haskell': 2,
    'PHP': 1,
    'Others': 1
}


# 1. load repo metas and normalized values for each feature
metas = []
temp = []
for file in json_files:
    loader = Loader(os.path.join(os.path.dirname(
        __file__), '../data/' + file), type='json')
    repo_meta = loader.start()

    created_days = datetime.now() - \
        datetime.strptime(repo_meta['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    cold_days = datetime.now() - \
        datetime.strptime(repo_meta['updated_at'], '%Y-%m-%dT%H:%M:%SZ')

    meta = [repo_meta['id'], repo_meta['owner']
            ['login'].lower(), repo_meta['name'].lower()]
    metas.append(meta)
    v = [
        repo_meta['size'],
        repo_meta['stargazers_count'],
        repo_meta['watchers_count'],
        repo_meta['forks'],
        repo_meta['open_issues'],
        repo_meta['subscribers_count'],
        len(repo_meta['contributors']),
        language_weight['Others' if repo_meta['language']
                        == None else repo_meta['language']],
        created_days.days,
        cold_days.days,
        1  # open source
    ]
    temp.append(v)

META = np.array(metas, dtype=object)
X = np.array(temp, dtype=object)
X_normed = X / X.max(axis=0)
print(X_normed)


# 2. load all names and sentiment & prices
loader = Loader(os.path.join(os.path.dirname(
    __file__), '../data/Price_Sentiment_url.csv'), type='csv')
data = np.array(loader.start())
names = data[:, (0)]
labels = data[:, (2, 3)]
labels[labels == ''] = '-100'
print(labels.astype(float))