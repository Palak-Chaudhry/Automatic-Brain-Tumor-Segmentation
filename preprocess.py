from torch.utils.data import Dataset
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
import numpy as np
import pickle

from PIL import Image

import os
import random


class TumorDataset(Dataset):
    """ Returns a TumorDataset class object which represents our tumor dataset.
    TumorDataset inherits from torch.utils.data.Dataset class.
    """

    def __init__(self, root_dir, transform=True, DEBUG=False):
        """ Constructor for our TumorDataset class.
        Parameters:
            root_dir(str): Directory with all the images.
            transform(bool): Flag to apply image random transformation.
            DEBUG(bool): To switch to debug mode for image transformation.

        Returns: None
        """
        self.root_dir = root_dir
        self.transform = {'hflip': TF.hflip,
                          'vflip': TF.vflip,
                          'rotate': TF.rotate}
        self.default_transformation = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((512, 512))
        ])
        self.DEBUG = DEBUG
        if not transform:
            self.transform = None

    def __getitem__(self, index):
        """ Overridden method from inheritted class to support
        indexing of dataset such that datset[I] can be used
        to get Ith sample.
        Parameters:
            index(int): Index of the dataset sample

        Return:
            sample(dict): Contains the index, image, mask torch.Tensor.
                        'index': Index of the image.
                        'image': Contains the tumor image torch.Tensor.
                        'mask' : Contains the mask image torch.Tensor.
        """
        image_name = os.path.join(self.root_dir, str(index)+'.png')
        mask_name = os.path.join(self.root_dir, str(index)+'_mask.png')

        image = Image.open(image_name)
        mask = Image.open(mask_name)

        image = self.default_transformation(image)
        mask = self.default_transformation(mask)

        # Custom transformations
        if self.transform:
            image, mask = self._random_transform(image, mask)

        image = TF.to_tensor(image)
        mask = TF.to_tensor(mask)

        sample = {'index': int(index), 'image': image, 'mask': mask}
        return sample

    def _random_transform(self, image, mask):
        """ Applies a set of transformation in random order.
        Each transformation has a probability of 0.5
        """
        choice_list = list(self.transform)
        for _ in range(len(choice_list)):
            choice_key = random.choice(choice_list)
            if self.DEBUG:
                print(f'Transform choose: {choice_key}')
            action_prob = random.randint(0, 1)
            if action_prob >= 0.5:
                if self.DEBUG:
                    print(f'\tApplying transformation: {choice_key}')
                if choice_key == 'rotate':
                    rotation = random.randint(15, 75)
                    if self.DEBUG:
                        print(f'\t\tRotation by: {rotation}')
                    image = self.transform[choice_key](image, rotation)
                    mask = self.transform[choice_key](mask, rotation)
                else:
                    image = self.transform[choice_key](image)
                    mask = self.transform[choice_key](mask)
            choice_list.remove(choice_key)

        return image, mask

    def __len__(self):
        """ Overridden method from inheritted class so that
        len(self) returns the size of the dataset.
        """
        error_msg = 'Part of dataset is missing!\nNumber of tumor and mask images are not same.'
        total_files = len(os.listdir(self.root_dir))

        assert (total_files % 2 == 0), error_msg
        return total_files//2

def get_indices(length, new=False):
    """ Gets the Training & Testing data indices for a
    paticular "DATASET_USED".Stores the indices and returns
    them back when the same dataset is used.
    Parameters:
        length(int): Length of the dataset used.
        new(bool): Discard the saved indices and get new ones.
    Return:
        train_indices(list): Array of indices used for training purpose.
        test_indices(list): Array of indices used for testing purpose.
    """
    # Pickle file location of the indices.
    file_path = os.path.join('dataset','split_indices_png_dataset.p')
    data = dict()
    if os.path.isfile(file_path) and not new:
        # File found.
        with open(file_path,'rb') as file :
            data = pickle.load(file)
            return data['train_indices'], data['test_indices']
    else:
        # File not found or fresh copy is required.
        indices = list(range(length))
        np.random.shuffle(indices)
        split = int(np.floor(0.2 * length))
        train_indices , test_indices = indices[split:], indices[:split]
        # Indices are saved with pickle.
        data['train_indices'] = train_indices
        data['test_indices'] = test_indices
        with open(file_path,'wb') as file:
            pickle.dump(data,file)
    return train_indices, test_indices