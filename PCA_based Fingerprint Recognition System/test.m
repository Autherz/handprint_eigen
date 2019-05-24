clc
close all
clear all
%%
%%%%%%%%%%%%%%%%%%%%%% File management
TrainFiles = dir('TrainDatabase\');
Train_Number = 0;

for ii = 1:size(TrainFiles,1)
    if not(strcmp(TrainFiles(ii).name,'.')|strcmp(TrainFiles(ii).name,'..')|strcmp(TrainFiles(ii).name,'Thumbs.db'))
        Train_Number = Train_Number + 1; % Number of all images in the training database
    end
end

%%
img = imresize(imread('TestDatabase\2.jpg'),[512 512]);
gaborArray = gaborFilterBank(5,8,39,39);  % Generates the Gabor filter bank
ProjectedTestImage = gaborFeatures(img,gaborArray,4,4);

%%
load('DB_of_gabor_file.mat')
%%
ProjectedImages = featureVector;

Euc_dist = [];
for i = 1 : Train_Number
    q = ProjectedImages(:,i);
    temp = ( norm( ProjectedTestImage - q ) )^2;
    Euc_dist = [Euc_dist temp];
end

[Euc_dist_min , Recognized_index] = min(Euc_dist);
% OutputName = strcat(int2str(Recognized_index),'.jpg');