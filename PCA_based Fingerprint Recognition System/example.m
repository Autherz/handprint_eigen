clear all
clc
close all
%%
% You can customize and fix initial directory paths
TrainDatabasePath = 'TrainDatabase\';
TestDatabasePath = 'TestDatabase\';

TestImage  = 'TestDatabase\21.jpg';
im = imresize(imread(TestImage),[512 512]);

T = CreateDatabase(TrainDatabasePath);
[m, A, Eigenfaces] = EigenfaceCore(T);
OutputName = Recognition(TestImage, m, A, Eigenfaces);

SelectedImage = strcat(TrainDatabasePath,'\',OutputName);
SelectedImage = imread(SelectedImage);

imshow(im)
title('Test Image');
figure,imshow(SelectedImage);
title('Equivalent Image');

str = strcat('Matched image is :  ',OutputName);
disp(str)
