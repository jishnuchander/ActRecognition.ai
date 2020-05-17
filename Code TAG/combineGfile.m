function combineGfile(dataset)

%activitylist = ['C:\HAR_complete\_act_desc_v3\' dataset '\'];
%inpath = ['C:\HAR_complete\HAR_v3.1\_results_v4\' dataset '\'];
%outpath = [inpath '\Combined\'];

activitylist = ['/home/jishnu/Desktop/BTP/_act_desc_v3/' dataset '/' act_name '/']
inpath = ['/home/jishnu/Desktop/BTP/_act_desc_v3/' dataset '/' act_name '/']
outpath = [inpath '/Combined/'];

activity = [];
activity = [activity dir(activitylist)];

fn = [outpath '_ExtC9_cw.txt'];cfExtC9cw = fopen(fn, 'a');
fn = [outpath '_ExtC9_c.txt']; cfExtC9c = fopen(fn, 'a');
fn = [outpath '_ExtC9_w.txt']; cfExtC9w = fopen(fn, 'a');
flist = fopen([outpath 'actlist.txt'], 'a');

total = 0;
for i = 1:length(activity)
    if ~isempty(regexp(activity(i).name, '[\w]+', 'once'))
        fn = [inpath activity(i).name '_ExtC9_cw.txt'];%fExtC9cw = fopen(fn, 'r');
        num = str2num(perl('countlines.pl', fn));
        total = total + num;
    end
end
%fclose(fExtC9cw);

fprintf(cfExtC9cw, '%d\n', total);
fprintf(cfExtC9w, '%d\n', total);
fprintf(cfExtC9c, '%d\n', total);

for i = 1:length(activity)
    if ~isempty(regexp(activity(i).name, '[\w]+', 'once'))
        fn = [inpath activity(i).name '_ExtC9_cw.txt'];fExtC9cw = fopen(fn, 'r');
        fn = [inpath activity(i).name '_ExtC9_c.txt']; fExtC9c = fopen(fn, 'r');
        fn = [inpath activity(i).name '_ExtC9_w.txt']; fExtC9w = fopen(fn, 'r');
        
        num = str2num(perl('countlines.pl', fn));
        
        fprintf(flist, '%s\t%d\n', activity(i).name, num);
        
        for j = 1:num
            line = fgets(fExtC9cw);
            fprintf(cfExtC9cw, '%s', line);
            line = fgets(fExtC9w);
            fprintf(cfExtC9w, '%s', line);
            line = fgets(fExtC9c);
            fprintf(cfExtC9c, '%s', line);
        end
        
%         total = total + num;
    end
end
% disp(total);
fclose('all');
end