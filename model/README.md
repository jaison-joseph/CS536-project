# Routenet Model

Requirements:
```
Networkx
Pytorch
Pandas
```

The trained pytorch model files are provided in the [`saved_models`](saved_models) folder.

### Setting up the Environmen:
Create a virtual environment and activate it. From the virtual environment install dependencies from the `requirements.txt` using the below command:
```bash
pip install -r requirements.txt
```

### Training the model:
- First generate the dataset
- Place and organize each simulation in the dataset folder as the following hierarchy
  ```
  dataset/
      ├── <DATASET=[nsfnet, geant, etc.]>/
      │   ├── results_1/
      │   │   ├── Routing.txt
      │   │   └── simulationResults.csv
      │   ├── results_2/
      │   │   ├── Routing.txt
      │   │   └── simulationResults.csv
      │   ├── .........
      │   └── graph_attr.txt
  ```
- Now generate the tensor files:
    ```bash
    python process_raw_data.py
    ```
  This will also split the dataset into two partitions train and test. The process folder will have the processed data
- Finally, start training the model:
    ```bash
    python main.py
    ```

### Evaluating the model:
- Organize the dataset like the training section
- Now generate the tensor files:
    ```bash
    python process_raw_data.py
    ```
- Finally, evaluate the model:
    ```bash
    python evaluate_model.py
    ```

