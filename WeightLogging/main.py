import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

height = 5 * 12 + 10.5
BMI_Indices = {"Healthy": 18, "Overweight": 25, "Obese": 30, "Extremely Obese": 40 }
WeightClasses = {"Healthy": 18 * (height * height) / 703, "Overweight": 25 * (height * height) / 703,
                 "Obese": 30 * (height * height) / 703, "Extremely Obese": 40 * (height * height) / 703}
Months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7,
          'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

def BMI_Calculator(weight, height):
    # INPUT: weight (lbs), height (inches)
    # OUTPUT: BMI (index)
    return 703 * weight / (height * height)


def processRunningData():
    f = open("RunningData.csv", "r")
    rnlogs = []
    dtlogs = []
    for line in f.readlines():
        line = line.strip('\n')
        log = line.split(",")
        date = log[0].split("-")
        year = date[2].split(" ")[0]
        dtlogs.append(dt.date(year=int(year), month=Months[date[1]], day=int(date[0])))
        rnlogs.append(float(log[2]))

    ts = pd.Series(rnlogs, index=dtlogs)

    rnlist = []
    mtlist = []
    i = 0
    sumlg, mtlogs = 0, 0
    curr_year, curr_month = ts.index.tolist()[0].year, ts.index.tolist()[0].month
    for dtlog in ts.index.tolist():
        prev_year, prev_month = curr_year, curr_month
        curr_year, curr_month = dtlog.year, dtlog.month
        if curr_year == prev_year and curr_month == prev_month:
            sumlg += ts.values.tolist()[i]
            mtlogs += 1
        else:
            rnlist.append(sumlg)
            sumlg = 0
            mtlogs = 0
            mtlist.append(dt.date(year=prev_year, month=prev_month, day=15))
        i += 1

    f.close()
    return mtlist, rnlist


def processWeightLogs():
    f = open("Health Data.csv", "r")
    wtlogs = []
    dtlogs = []
    for line in f.readlines():
        line = line.strip('\n')
        log = line.split(",")
        date = log[0].split("-")
        year = date[2].split(" ")[0]
        dtlog = dt.date(year=int(year), month=Months[date[1]], day=int(date[0]))
        wtlog = float(log[2])
        if wtlog != 0:
            wtlogs.append(wtlog)
            dtlogs.append(dtlog)

    f.close()
    return pd.Series(wtlogs, index=dtlogs)


if __name__ == '__main__':
    dates_arr, monthly_avgs = processRunningData()
    ts = processWeightLogs()

    fig, axs = plt.subplots(2, figsize=(9,7), gridspec_kw={'height_ratios': [3, 1]})
    axs[0].plot(ts)
    axs[0].axhline(y=WeightClasses["Overweight"], color='k', linestyle='--',
                label="Overweight (> {} lbs)".format(int(WeightClasses["Overweight"])))
    axs[0].axhline(y=WeightClasses["Obese"], color='r', linestyle='dashed',
                label="Obese (> {} lbs)".format(int(WeightClasses["Obese"])))
    axs[0].legend()
    axs[1].bar(dates_arr, monthly_avgs, width=20)
    axs[0].title.set_text('Weight Logs')
    axs[0].set_ylabel('Weight (lbs)')
    axs[1].title.set_text('Running Logs')
    axs[1].set_xlabel('Dates')
    axs[1].set_ylabel('Miles (mi)')

    plt.show()




