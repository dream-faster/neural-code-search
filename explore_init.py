from multiprocessing.util import get_logger
import os

import pandas as pd

from code_embeddings import CodeEmbeddings
from constants import Const, DFCols
from utils import get_logger
from cosine_similarity import CosineSimilarity_Search


def ce_init():
    ce = CodeEmbeddings()

    data_fn = f"{Const.root_data_processed}/data_embedded.parquet"
    if not os.path.exists(data_fn):
        raise FileNotFoundError(f"{data_fn} not found")
    df = pd.read_parquet(data_fn)

    print("Calculating TF-IDF...")

    ce.tfidf_init(df[DFCols.processed_feature.value])

    return ce, df


if __name__ == "__main__":
    logger = get_logger()
    ce, df = ce_init()
    code = 'def hello_s(s: str):\n    print(f"Hello s")'
    logger.info(f"Code: {code}")
    tokens_str = ce.extract_tokens_str(code)
    logger.info(f"Tokens: {tokens_str}")
    e = ce.get_doc_embedding(tokens_str)
    logger.info(f"Doc e embedding dim1: {e[0]}")

    cos_search = CosineSimilarity_Search(library=df)
    result = cos_search.get_similarity(e)
