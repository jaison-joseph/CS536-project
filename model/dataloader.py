import pickle
import os
from turtledemo.clock import setup
from typing import Optional
import torch
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from tqdm import tqdm

class NetDataset(Dataset):
    def __init__(self, sample_list, label_str):
        super().__init__()
        self.sample_list = sample_list
        self.label_str = label_str

    def __getitem__(self, index):
        s = self.sample_list[index]
        y = torch.FloatTensor(s[self.label_str])
        return s, y
    
    def __len__(self):
        return len(self.sample_list)

class NetDataModule(pl.LightningDataModule):
    def __init__(self, data_path, label_str):
        super().__init__()
        self.train_path = f"{data_path}/process/train"
        self.eval_path = f"{data_path}/process/eval"
        if not label_str in ['delay', 'jitter', 'packet_loss']:
            print("[dataloader.py]: input wrong label_str. label_str should be one of [delay / jitter / packet_loss]")
            exit(0)
        self.label_str = label_str
    
    def process_data(self, data_path):
        _, _, data_file = next(os.walk(data_path))
        data_type = data_path.split('/')[-1]
        sample_list = []
        with tqdm(data_file) as t:
            for file in t:
                t.set_description(f"{data_type} data loading")
                with open(os.path.join(data_path, file), 'rb') as f:
                    data_list = pickle.load(f)
                sample_list.extend(data_list)
        return sample_list

    def setup(self, stage: Optional[str] = None):
        if stage == 'fit' or stage is None:
            train_list = self.process_data(self.train_path)
            eval_list = self.process_data(self.eval_path)
            self.train, self.eval = NetDataset(train_list, self.label_str), NetDataset(eval_list, self.label_str)
        
        if stage == 'test' or stage == 'validate':
            eval_list = self.process_data(self.eval_path)
            self.eval = NetDataset(eval_list, self.label_str)

    def train_dataloader(self):
        return DataLoader(self.train, batch_size=1)
    
    def val_dataloader(self):
        return DataLoader(self.eval, batch_size=1)
    
    def test_dataloader(self):
        if not hasattr(self, 'eval'):
            self.setup(stage='test')
        return DataLoader(self.eval, batch_size=1)

if __name__ == "__main__":
    dm = NetDataModule('./dataset/nsfnet', 'jitter')
    dm.setup(stage='fit')
    for x, y in dm.train_dataloader():
       print(y)
    for x, y in dm.test_dataloader():
        print(y)
