function CreateGfileWrap(dataset)

%inpath = ['C:\HAR_complete\_act_desc_v3\' dataset '\'];
inpath = ['/home/jishnu/Desktop/BTP/_act_desc_v3/' dataset '/' act_name '/']

folders = [];
folders = [folders dir(inpath)];

for i = 1:length(folders)
    if ~isempty(regexp(folders(i).name, '[\w]+', 'once'))
        CreateGfile(dataset, folders(i).name);
    end
end
combineGfile(dataset);
end