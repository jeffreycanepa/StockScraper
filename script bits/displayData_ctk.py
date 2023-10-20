import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns; sns.set()
import pandas as pd
import customtkinter
import getCompanyData_ctk
import numDays_ctk

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-   object containing the stock data
#   ticker-    The stock ticker
#   window-    The tkinter window to plot the data to
#  
# Returns:
#
def plot_data(window):
    company_name = getCompanyData_ctk.company_name
    company = getCompanyData_ctk.stockData
    dates = numDays_ctk.dates
    fig, ax = plt.subplots(figsize=(13,8))
    sns.set_style('darkgrid')
    ax.set_title('Closing Prices', fontsize=20)

    # convert the regression line start date to ordinal
    x1 = pd.to_datetime(dates[0]).toordinal()

    # convert the datetime index to ordinal values, which can be used to plot a regression line
    company.index = company.index.map(pd.Timestamp.toordinal)
    data=company.loc[x1:].reset_index()

     # Add Closing price for stock as a line and as a linear regression (trend line)
    ax1 = sns.lineplot(data=company,x=company.index,y='Adj Close', color='blue', label=company_name)
    sns.regplot(data=company, x=company.index, y='Adj Close', color='black', scatter=False, ci=False)
   
    ax1.set_xlim(company.index[0], company.index[-1])

    # convert the axis back to datetime
    xticks = ax1.get_xticks()
    labels = [pd.Timestamp.fromordinal(int(label)).strftime('%b %d, \'%y') for label in xticks]
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(labels)
    ax.tick_params(axis='x', labelrotation=45)
    ax.tick_params(axis='both', labelsize=9)

    sns.despine()
    plt.title('{0} Closing Prices\n{1} - {2}'.format(company_name, dates[4], dates[5]), size='x-large', color='black')
    plt.ylabel('Stock Price $ (USD)')
    
    # Create canvas and add it to Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# plot_window()- A tk window for displaying the data plot from plot_data().  Quiting dialog
#               quits the app.
#
# Required:
#   company_data- The object returned by yfinance that contains the stock data
#   ticker-       The stock ticker used to do the lookup
#
# Returns:
#
def plot_window():
    # Create the window
    # print('Inside plot_window')
    plotWindow = customtkinter.CTk()
    plotWindow.title('Past ' + str(numDays_ctk.days) + ' Days')
    plotWindow.geometry('1000x880+200+40')

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # Using Matplotlib display company stock data
    plot_data(plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = customtkinter.CTkButton(plotWindow, text='Quit', command=plotWindow.quit, width=20, height=12)
    bt_1.pack(pady=10)

    plotWindow.mainloop() 