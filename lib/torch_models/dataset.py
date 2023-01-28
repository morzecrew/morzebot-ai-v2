from torch.utils.data import Dataset, DataLoader
import torch
class Data(Dataset):
    def __init__(self,X_train,Y_train):
        self.x=torch.Tensor(X_train)
        self.y=torch.from_numpy(Y_train)
        self.len=self.x.shape[0]
    def __getitem__(self,index):
        return self.x[index], self.y[index]
    def __len__(self):
        return self.len