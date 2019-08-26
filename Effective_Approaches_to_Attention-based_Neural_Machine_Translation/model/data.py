import pandas as pd
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from typing import List, Tuple


class NMTCorpus(Dataset):
    def __init__(self, filepath, src_transform_fn, tgt_transform_fn):
        self._corpus = pd.read_csv(filepath, sep='\t')
        self._src_transform = src_transform_fn
        self._tgt_transform = tgt_transform_fn

    def __len__(self):
        return len(self._corpus)

    def __getitem__(self, idx):
        list_of_source = torch.tensor(self._src_transform(self._corpus.iloc[idx]['ko']))
        list_of_indices_bos, list_of_indices_eos = [torch.tensor(elm) for elm in
                                                    self._tgt_transform(self._corpus.iloc[idx]['en'])]
        return list_of_source, list_of_indices_bos, list_of_indices_eos


def batchify(data: List[Tuple[torch.Tensor]]) -> Tuple[torch.tensor]:
    source_mb, target_bos_mb, target_eos_mb = zip(*data)
    source_mb = pad_sequence(source_mb, batch_first=True, padding_value=1)
    target_bos_mb = pad_sequence(target_bos_mb, batch_first=True, padding_value=1)
    target_eos_mb = pad_sequence(target_eos_mb, batch_first=True, padding_value=1)
    return source_mb, target_bos_mb, target_eos_mb
