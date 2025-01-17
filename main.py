'''
author:zhujunwen
Guangdong University of Technology
'''
import argparse
import logging
import torch
import matplotlib.pyplot as plt
import math
from torch.utils.data import DataLoader
from torch import autograd, optim
from UNet import Unet,resnet34_unet
from attention_unet import AttU_Net
from channel_unet import myChannelUnet
from r2unet import R2U_Net
from segnet import SegNet
from unetpp import NestedUNet
from fcn import get_fcn8s
from dataset import *
from metrics import *
from torchvision.transforms import transforms
from plot import loss_plot
from plot import metrics_plot
from torchvision.models import vgg16
def getArgs():
    parse = argparse.ArgumentParser()
    parse.add_argument('--deepsupervision', default=0)
    parse.add_argument("--action", type=str, help="train/test/train&test", default="train&test")
    parse.add_argument("--epoch", type=int, default=21)
    parse.add_argument('--arch', '-a', metavar='ARCH', default='resnet34_unet',
                       help='UNet/resnet34_unet/unet++/myChannelUnet/Attention_UNet/segnet/r2unet/fcn32s/fcn8s')
    parse.add_argument("--batch_size", type=int, default=1)
    parse.add_argument('--dataset', default='driveEye',  # dsb2018_256
                       help='dataset name:liver/esophagus/dsb2018Cell/corneal/driveEye/isbiCell/kaggleLung')
    # parse.add_argument("--ckp", type=str, help="the path of model weight file")
    parse.add_argument("--log_dir", default='result/log', help="log dir")
    parse.add_argument("--threshold",type=float,default=None)
    args = parse.parse_args()
    return args

def getLog(args):
    dirname = os.path.join(args.log_dir,args.arch,str(args.batch_size),str(args.dataset),str(args.epoch))
    filename = dirname +'/log.log'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    logging.basicConfig(
            filename=filename,
            level=logging.DEBUG,
            format='%(asctime)s:%(levelname)s:%(message)s'
        )
    return logging

def getModel(args):
    if args.arch == 'UNet':
        model = Unet(3, 3).to(device)
    if args.arch == 'resnet34_unet':
        model = resnet34_unet(3,pretrained=False).to(device)
    if args.arch == 'unet++':
        args.deepsupervision = True
        model = NestedUNet(args,3,3).to(device)
    if args.arch =='Attention_UNet':
        model = AttU_Net(3,3).to(device)
    if args.arch == 'segnet':
        model = SegNet(3,3).to(device)
    if args.arch == 'r2unet':
        model = R2U_Net(3,3).to(device)
    # if args.arch == 'fcn32s':
    #     model = get_fcn32s(1).to(device)
    if args.arch == 'myChannelUnet':
        model = myChannelUnet(3,3).to(device)
    if args.arch == 'fcn8s':
        model = get_fcn8s(3).to(device)
    if args.arch == 'cenet':
        from cenet import CE_Net_
        model = CE_Net_(3).to(device)
    return model

def getDataset(args):
    train_dataloaders, val_dataloaders ,test_dataloaders= None,None,None
    if args.dataset =='liver':  
        train_dataset = LiverDataset(r"train", transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = LiverDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataloaders = val_dataloaders
    if args.dataset =="esophagus":
        train_dataset = esophagusDataset(r"train", transform=x_transforms,target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = esophagusDataset(r"val", transform=x_transforms,target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataloaders = val_dataloaders
    if args.dataset == "dsb2018Cell":
        train_dataset = dsb2018CellDataset(r"train", transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = dsb2018CellDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataloaders = val_dataloaders
    if args.dataset == 'corneal':
        train_dataset = CornealDataset(r'train',transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = CornealDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataset = CornealDataset(r"test", transform=x_transforms, target_transform=y_transforms)
        test_dataloaders = DataLoader(test_dataset, batch_size=1)
    if args.dataset == 'driveEye':
        train_dataset = DriveEyeDataset(r'train', transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = DriveEyeDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataset = DriveEyeDataset(r"test", transform=x_transforms, target_transform=y_transforms)
        test_dataloaders = DataLoader(test_dataset, batch_size=1)
    if args.dataset == 'isbiCell':
        train_dataset = IsbiCellDataset(r'train', transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = IsbiCellDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataset = IsbiCellDataset(r"test", transform=x_transforms, target_transform=y_transforms)
        test_dataloaders = DataLoader(test_dataset, batch_size=1)
    if args.dataset == 'kaggleLung':
        train_dataset = LungKaggleDataset(r'train', transform=x_transforms, target_transform=y_transforms)
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataset = LungKaggleDataset(r"val", transform=x_transforms, target_transform=y_transforms)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataset = LungKaggleDataset(r"test", transform=x_transforms, target_transform=y_transforms)
        test_dataloaders = DataLoader(test_dataset, batch_size=1)

    if args.dataset == 'dacon':
        train_dataset = DaconDataset('train')
        val_dataset = DaconDataset('val')
        test_dataset = DaconDataset('val')
        
        train_dataloaders = DataLoader(train_dataset, batch_size=args.batch_size)
        val_dataloaders = DataLoader(val_dataset, batch_size=1)
        test_dataloaders = DataLoader(test_dataset, batch_size=1)
        
    return train_dataloaders,val_dataloaders,test_dataloaders

def rmse_score(true, pred):
    score = math.sqrt(np.mean((true-pred)**2))
    return score

def psnr_score(true, pred, pixel_max):
    score = 20*np.log10(pixel_max/rmse_score(true, pred))
    return score

def val(model,best_iou,val_dataloaders):
    model= model.eval()
    with torch.no_grad():
        i=0 
        miou_total = 0
        hd_total = 0
        dice_total = 0
        score_total = 0
        num = len(val_dataloaders)  
        for x, label,pic,mask in val_dataloaders:
            x = x.to(device)
            y = model(x)
            if args.deepsupervision:
                img_y = torch.squeeze(y[-1]).cpu().numpy()
            else:
                img_y = torch.squeeze(y).cpu().numpy()  
            
            score = psnr_score(img_y*255.0,label.float().detach().cpu().numpy()*255.0, 255)
            score_total += score
            #hd_total += get_hd(mask[0], img_y)
            #miou_total += get_iou(mask[0],img_y) 
            #dice_total += get_dice(mask[0],img_y)
            if i < num:i+=1  
        #aver_iou = miou_total / num
        #aver_hd = hd_total / num
        #aver_dice = dice_total/num
        aver_psnr = score_total/num
        #print('Miou=%f,aver_hd=%f,aver_dice=%f' % (aver_iou,aver_hd,aver_dice))
        print('psnr score=%f' % (aver_psnr))
        logging.info('psnr score = %f' % (aver_psnr))
        #if aver_iou > best_iou:
        #    print('aver_iou:{} > best_iou:{}'.format(aver_iou,best_iou))
        #    logging.info('aver_iou:{} > best_iou:{}'.format(aver_iou,best_iou))
        #    logging.info('===========>save best model!')
        #    best_iou = aver_iou
        #    print('===========>save best model!')
        #    torch.save(model.state_dict(), r'./saved_model/'+str(args.arch)+'_'+str(args.batch_size)+'_'+str(args.dataset)+'_'+str(args.epoch)+'.pth')
        return aver_psnr

def train(model, criterion, optimizer, train_dataloader,val_dataloader, args):
    best_iou,aver_iou,aver_dice,aver_hd = 0,0,0,0
    num_epochs = args.epoch
    threshold = args.threshold
    loss_list = []
    iou_list = []
    dice_list = []
    hd_list = []
    psnr_list = []
    for epoch in range(num_epochs):
        model = model.train()
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        logging.info('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)
        dt_size = len(train_dataloader.dataset)
        epoch_loss = 0
        step = 0
        for x, y,_,mask in train_dataloader:
            step += 1
            inputs = x.to(device)
            labels = y.to(device)
            # zero the parameter gradients
            optimizer.zero_grad()
            if args.deepsupervision:
                outputs = model(inputs)
                loss = 0
                for output in outputs:
                    loss += criterion(output, labels)
                loss /= len(outputs)
            else:
                output = model(inputs)
                loss = criterion(output, labels)
            if threshold!=None:
                if loss > threshold:
                    loss.backward()
                    optimizer.step()
                    epoch_loss += loss.item()
            else:
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            print("%d/%d,train_loss:%0.3f, psnr : %0.4f" % (step, (dt_size - 1) // train_dataloader.batch_size + 1, loss.item(), psnr_score(x.float().detach().numpy()*255.0, y.float().detach().numpy()*255.0, 255)))
            logging.info("%d/%d,train_loss:%0.3f, psnr : %0.4f" % (step, (dt_size - 1) // train_dataloader.batch_size + 1, loss.item(), psnr_score(x.float().detach().numpy()*255.0, y.float().detach().numpy()*255.0, 255)))
        loss_list.append(epoch_loss)

        #best_iou,aver_iou,aver_dice,aver_hd = val(model,best_iou,val_dataloader)
        aver_psnr = val(model,best_iou,val_dataloader)
        #iou_list.append(aver_iou)
        #dice_list.append(aver_dice)
        #hd_list.append(aver_hd)
        psnr_list.append(aver_psnr)
        print("epoch %d loss:%0.3f" % (epoch, epoch_loss))
        logging.info("epoch %d loss:%0.3f" % (epoch, epoch_loss))
        torch.save(model.state_dict(), './saved_model/'+str(args.arch)+'_'+str(args.batch_size)+'_'+str(args.dataset)+'_'+str(epoch)+'.pth')
    loss_plot(args, loss_list)
    #metrics_plot(args, 'iou&dice',iou_list, dice_list)
    #metrics_plot(args,'hd',hd_list)
    metrics_plot(args, 'psnr', psnr_list)
    return model

def test(val_dataloaders,save_predict=False):
    logging.info('final test........')
    if save_predict ==True:
        dir = os.path.join(r'./saved_predict',str(args.arch),str(args.batch_size),str(args.epoch),str(args.dataset))
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            print('dir already exist!')
    model.load_state_dict(torch.load(r'./saved_model/'+str(args.arch)+'_'+str(args.batch_size)+'_'+str(args.dataset)+'_'+str(args.epoch)+'.pth', map_location='cpu'))
    model.eval()


    with torch.no_grad():
        i=0  
        miou_total = 0
        hd_total = 0
        dice_total = 0
        num = len(val_dataloaders) 
        for pic,_,pic_path,mask_path in val_dataloaders:
            pic = pic.to(device)
            predict = model(pic)
            if args.deepsupervision:
                predict = torch.squeeze(predict[-1]).cpu().numpy()
            else:
                predict = torch.squeeze(predict).cpu().numpy() 

            iou = get_iou(mask_path[0],predict)
            miou_total += iou
            hd_total += get_hd(mask_path[0], predict)
            dice = get_dice(mask_path[0],predict)
            dice_total += dice

            fig = plt.figure()
            ax1 = fig.add_subplot(1, 3, 1)
            ax1.set_title('input')
            plt.imshow(Image.open(pic_path[0]))
            #print(pic_path[0])
            ax2 = fig.add_subplot(1, 3, 2)
            ax2.set_title('predict')
            plt.imshow(predict,cmap='Greys_r')
            ax3 = fig.add_subplot(1, 3, 3)
            ax3.set_title('mask')
            plt.imshow(Image.open(mask_path[0]), cmap='Greys_r')
            #print(mask_path[0])
            if save_predict == True:
                if args.dataset == 'driveEye':
                    saved_predict = dir + '/' + mask_path[0].split('\\')[-1]
                    saved_predict = '.'+saved_predict.split('.')[1] + '.tif'
                    plt.savefig(saved_predict)
                else:
                    plt.savefig(dir +'/'+ mask_path[0].split('\\')[-1])
            #plt.pause(0.01)
            print('iou={},dice={}'.format(iou,dice))
            if i < num:i+=1   
        #plt.show()
        print('Miou=%f,aver_hd=%f,dv=%f' % (miou_total/num,hd_total/num,dice_total/num))
        logging.info('Miou=%f,aver_hd=%f,dv=%f' % (miou_total/num,hd_total/num,dice_total/num))
        #print('M_dice=%f' % (dice_total / num))

if __name__ =="__main__":
    x_transforms = transforms.Compose([
        transforms.ToTensor(),  # -> [0,1]
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])  # ->[-1,1]
    ])

    y_transforms = transforms.ToTensor()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    args = getArgs()
    logging = getLog(args)
    print('**************************')
    print('models:%s,\nepoch:%s,\nbatch size:%s\ndataset:%s' % \
          (args.arch, args.epoch, args.batch_size,args.dataset))
    logging.info('\n=======\nmodels:%s,\nepoch:%s,\nbatch size:%s\ndataset:%s\n========' % \
          (args.arch, args.epoch, args.batch_size,args.dataset))
    print('**************************')
    model = getModel(args)
    train_dataloaders,val_dataloaders,test_dataloaders = getDataset(args)
    criterion = torch.nn.BCELoss()
    optimizer = optim.Adam(model.parameters())
    if 'train' in args.action:
        train(model, criterion, optimizer, train_dataloaders,val_dataloaders, args)
    if 'test' in args.action:
        test(test_dataloaders, save_predict=True)
