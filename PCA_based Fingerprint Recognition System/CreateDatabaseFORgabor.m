clc
close all
clear all
%%
%%%%%%%%%%%%%%%%%%%%%%%% File management
TrainFiles = dir('TrainDatabase\');
Train_Number = 0;

for i = 1:size(TrainFiles,1)
    if not(strcmp(TrainFiles(i).name,'.')|strcmp(TrainFiles(i).name,'..')|strcmp(TrainFiles(i).name,'Thumbs.db'))
        Train_Number = Train_Number + 1 % Number of all images in the training database
    end
end

%%
for i = 1:Train_Number
    strname = strcat('TrainDatabase\', num2str(i), '.jpg');
    x = imread(strname);
    img = imresize(x,[512 512]);
    gaborArray = gaborFilterBank(5,8,39,39);  % Generates the Gabor filter bank
    featureVector(:,i) = gaborFeatures(img,gaborArray,4,4);
end
save('DB_of_gabor_file.mat','featureVector')