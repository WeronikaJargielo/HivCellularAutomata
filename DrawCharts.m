clear all; close all; clc;
basePath = '../../';
folders = {'v1'; 'v2'; 'v3'; 'v4'; 'v5'};

for i = 1:length(folders)
	fileprefix = [basePath folders{i} '/HIVCellularAutomata/results_Of_Simulation/'];

    files = dir('*.txt');

    for j = 1:length(files)
        file = [fileprefix files{j}]
    end
end