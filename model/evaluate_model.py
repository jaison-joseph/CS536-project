from dataloader import NetDataModule
from routenet import RouteNet
import pytorch_lightning as pl
import torch

DATASET = 'nsfnetbw1'
TRAINED_DS_MODEL = 'nsfnet'
METRICS = ['delay', 'jitter']
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

if __name__ == "__main__":

    for metric in METRICS:
        MODEL_NAME = f'{TRAINED_DS_MODEL}-{metric}.ckpt'

        dm = NetDataModule(f'./dataset/{DATASET}', metric)
        model = RouteNet.load_from_checkpoint(f'saved_models/{MODEL_NAME}',
                                              map_location=DEVICE,
                                              dim_link=32, dim_path=32, dim_linear=128, t=4)
        trainer = pl.Trainer(max_epochs=5, accelerator="gpu")
        # trainer.fit(model, dm)
        print(':::::', metric, ':::::')
        trainer.test(model, dataloaders=dm.test_dataloader())
