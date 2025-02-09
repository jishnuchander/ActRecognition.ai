function CreateGfile(dataset, act_name)

%inpath = ['C:\HAR_complete\_act_desc_v3\' dataset '\' act_name '\']; % input data stored in _act_desc_v3 folder
inpath = ['/home/jishnu/Desktop/BTP/_act_desc_v3/' dataset '/' act_name '/']

if strcmp(dataset, 'ME')    
        no_of_lines = 10;
else    no_of_lines = str2num(perl('countlines.pl', [inpath 'frames.txt']));
end
 
%outpath = ['C:\HAR_complete\HAR_v3.1\_results_v4\' dataset '\'];       % output stored in _results_v4 folder 
outpath = ['/home/jishnu/Desktop/BTP/HAR_v3.1/results_new/' dataset '/'];

fn = [outpath act_name '_ExtC9_cw.txt']; 
fExtC9cw = fopen(fn, 'a');
fn = [outpath act_name '_ExtC9_c.txt']; 
fExtC9c = fopen(fn, 'a');
fn = [outpath act_name '_ExtC9_w.txt']; 
fExtC9w = fopen(fn, 'a');
ffile = fopen([inpath 'frames.txt'], 'r');


for i = 1:no_of_lines
%     filename = input('Enter the file name: ','s');
%     no_of_frames = input('Enter the number of frames ');

    line = fgetl(ffile);
    [fname,fstr] = strtok(line, ':');
    [~,f] = strtok(fstr, ' ');
    no_of_frames = str2num(f);
    if strcmp(dataset, 'ME')    
            filename = [inpath fname '.txt'];
    else    filename = [inpath fname];
    end
    
    currExample = readExample(filename, no_of_frames);

    docExtC9c = [];
    docExtC9w = [];
    
    for j = 1 : currExample.length
        docExtC9c = [docExtC9c currExample.qExtC9{j,1}.c ' '];
        docExtC9w = [docExtC9w currExample.qExtC9{j,1}.w ' '];
    end
    
    fprintf(fExtC9cw, '%d\t%s\t%s\n', currExample.length, docExtC9c, docExtC9w);
    fprintf(fExtC9c, '%d\t%s\n', currExample.length, docExtC9c);
    fprintf(fExtC9w, '%d\t%s\n', currExample.length, docExtC9w);
end
disp('Done');
fclose('all');
end