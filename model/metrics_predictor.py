from dataloader import NetDataModule
from routenet import RouteNet
import pytorch_lightning as pl
import torch

DATASET = 'demo'
TRAINED_DS_MODEL = 'nsfnet'
METRICS = ['delay'] #, 'jitter']
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

if __name__ == "__main__":

    for metric in METRICS:
        MODEL_NAME = f'{TRAINED_DS_MODEL}-{metric}.ckpt'

        dm = NetDataModule(f'./dataset/{DATASET}', metric)
        # model = RouteNet(32, 32, 128, 4)
        model = RouteNet.load_from_checkpoint(f'saved_models/{MODEL_NAME}',
                                              map_location=DEVICE,
                                              dim_link=32, dim_path=32, dim_linear=128, t=4)
        model.eval()
        test_data = dm.test_dataloader()
        for batch_idx, (inputs, targets) in enumerate(test_data):
            for k in inputs.keys():
                inputs[k] = inputs[k].to(DEVICE)
            print(f'{metric}/{batch_idx} :: Predicted:{torch.mean(model(inputs)):.5f} Actual:{torch.mean(targets.to(DEVICE)):.5f}')
