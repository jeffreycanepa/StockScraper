# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-  a list of company objects containing stock data
#   linestyle-   a list of strings that are linestyle used by Matplotlib
#   window-   a tkinter window 
# Returns:
#
def plot_data(company, linestyle, window):
    # Create plot using matplotlib
    fig = plt.figure(figsize=(13, 7))
    sns.set_style('darkgrid')
    
    # convert the regression line start date to ordinal
    x1 = pd.to_datetime(dates[0]).toordinal()

    for cmp, lstyle in zip(company,linestyle):
        # convert the datetime index to ordinal values, which can be used to plot a regression line
        cmp.index = cmp.index.map(pd.Timestamp.toordinal)
        data=cmp.loc[x1:].reset_index()

        # Add Closing price for stock as a line and as a linear regression (trend line)
        ax1 = sns.lineplot(data=cmp,x=cmp.index,y="Close",color=lstyle[0],linestyle=lstyle[1], label=cmp.name)
        sns.regplot(data=data, x=cmp.index, y='Close', color=lstyle[0], scatter=False, ci=False)

        ax1.set_xlim(cmp.index[0], cmp.index[-1])

        # convert the axis back to datetime
        xticks = ax1.get_xticks()
        labels = [pd.Timestamp.fromordinal(int(label)).date() for label in xticks]
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(labels)

    sns.despine()
    plt.title('Closing Prices\n{0} - {1}'.format(dates[2], dates[3]), size='x-large', color='black')
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
