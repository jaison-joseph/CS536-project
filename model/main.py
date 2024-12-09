from dataloader import NetDataModule
from routenet import RouteNet
import pytorch_lightning as pl

if __name__ == "__main__":
    dm = NetDataModule('./dataset/nsfnet', 'delay')
    model = RouteNet(32, 32, 128, 4)
    trainer = pl.Trainer(max_epochs=2, accelerator="gpu")
    trainer.fit(model, dm)