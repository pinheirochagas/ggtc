

%%
addpath(genpath('/Users/pinheirochagas/Pedro/Stanford/code/gpx_tools/'))
addpath(genpath('/Users/pinheirochagas/Pedro/Stanford/code/lbcn_preproc'))
activities = readtable('/Users/pinheirochagas/Downloads/strava_export/activities.xlsx');
activities.ActivityDate = datetime(activities.ActivityDate, 'InputFormat', 'MMM d yyyy HH:mm:ss a');
date = activities.ActivityDate;

activities.ActivityType(contains(activities.ActivityType, 'Ride')) = {'Ride'};
activities.ActivityType(contains(activities.ActivityType, 'Workout')) = {'Strenght'};
activities.ActivityType(contains(activities.ActivityType, 'Weight Training')) = {'Strenght'};


activities.date = activities.ActivityDate;
activities.months = date.Month;
activities.days = date.Day;

activities.weeks = weeknum(date);


idx_year = date.Year==2022;
activities = activities(idx_year,:);

%% Plot strava year in sports metrics

date.Year==2022;

days_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

metrics_interest = {'Distance', 'Calories', 'RelativeEffort', 'AverageHeartRate'}

cmaps = {'Blues', 'PuRd', 'Greens', 'Reds'};

for mi = 1:length(metrics_interest)
    metric_interest = metrics_interest{mi};
    
    data_summary = table;
    count = 1;
    for i = 1:12
        month = activities(activities.months==i, :);
        unique_days = unique(month.days);
        for ii = 1:size(unique_days)
            day = month(month.days==unique_days(ii),:);
            if strcmp(metric_interest(mi), 'AverageHeartRate')
                metric = sum(day.(metric_interest))/size(day,1);
            else
                metric = sum(day.(metric_interest));
            end
            data_summary.month(count) = i;
            data_summary.day(count) = unique_days(ii);
            data_summary.metric(count) = metric;
            count = count + 1;
        end
    end
    data_summary = data_summary(data_summary.metric>0,:);

%     figure('units', 'normalized', 'outerposition', [0 0 .3 .75]) % [0 0 .6 .3]
    min_clim = prctile(data_summary.metric,5);
    max_clim = prctile(data_summary.metric,95);

    [col_idx,cols] = colorbarFromValues(data_summary.metric, cmaps{mi},[min_clim, max_clim],false)
    col_idx(col_idx==0) = 1;

    for ifix = 1:12
        hold on
        plot(repmat(ifix,days_months(ifix),1), 1:days_months(ifix), '.', 'Color', 'w')
    end

    for idim = 1:size(data_summary,1)
        plot(data_summary.month(idim), data_summary.day(idim), '.', MarkerSize=50, Color=cols((col_idx(idim)),:))
    end


    set(gcf,'color', [.5 .5 .5]);
    set(gca,'color', [.5 .5 .5]);
    axis off
    title(metric_interest)

%     save2pdf([metric_interest, '.pdf'], gcf, 600)
    close
    max_vals(mi) = max(data_summary.metric)

end





%% Plot strava year in sports stacked
tblstats = grpstats(activities,["weeks","ActivityType"],'sum', 'DataVars','ElapsedTime');
actypes = {'Swim','Ride',  'Run', 'Strenght'};

for i = 1:max(tblstats.weeks)
        tbl_tmp = tblstats(tblstats.weeks == i,:);

    for ii = 1:length(actypes)
        hrs = tbl_tmp.sum_ElapsedTime(contains(tbl_tmp.ActivityType, actypes{ii}))/60/60
        if isempty(hrs)
           count_hours(i,ii) = 0;
        else
           count_hours(i,ii) = hrs;
        end

    end
end




subplot(1,6,1:5)
bar_handle = bar(count_hours, 'stacked');
bar_handle(1).FaceColor = [106,165,200]/255;
bar_handle(2).FaceColor = [201,59,43]/255;
bar_handle(3).FaceColor = [103,163,109]/255;
bar_handle(4).FaceColor = [.5 .5 .5];
xticks(4:4:max(tblstats.weeks))
% yline(5); yline(10); yline(15); yline(20)
set(gca,'color','w');
set(gcf,'color','w');
set(gca,'fontsize',20)
xlabel('Week of the year')
ylabel('Hours')

xline(activities.weeks(contains(activities.ActivityName, 'Bay')))
xline(activities.weeks(contains(activities.ActivityName, 'Marin')))
xline(activities.weeks(strcmp(activities.ActivityName, 'Santa Cruz 70.3 run')))
xline(activities.weeks(contains(activities.ActivityName, '50K')))

subplot(1,6,6)
s_count_hours = round(sum(count_hours));
bar_handle2 = bar(1,s_count_hours, 'stacked')
hold on
for i = 1:length(s_count_hours)
    hr = num2str(s_count_hours(i))
    if i == 1
    text(1,s_count_hours(i)/2, hr, 'HorizontalAlignment', 'center', VerticalAlignment='middle', FontSize=30, Color='w')
    else
        text(1,(s_count_hours(i)/2)+sum(s_count_hours(1:i-1)), hr, 'HorizontalAlignment', 'center', VerticalAlignment='middle', FontSize=30, Color='w')

    end
end
bar_handle2(1).FaceColor = [106,165,200]/255;
bar_handle2(2).FaceColor = [201,59,43]/255;
bar_handle2(3).FaceColor = [103,163,109]/255;
bar_handle2(4).FaceColor = [.5 .5 .5];
set(gca,'color','w');
set(gcf,'color','w');
set(gca,'fontsize',20)
xticklabels('Total')
ylabel('Hours')

